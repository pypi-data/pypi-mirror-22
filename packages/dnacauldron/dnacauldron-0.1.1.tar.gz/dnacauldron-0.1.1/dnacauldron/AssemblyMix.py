"""
"""

import itertools as itt
from copy import deepcopy

import networkx as nx
import numpy as np
from Bio import Restriction
from Bio.Alphabet import DNAAlphabet

from .StickyEndsSeq import (StickyEndsSeqRecord, StickyEndsSeq, StickyEnd,
                            digest_seqrecord_with_sticky_ends)
from .Filter import NoRestrictionSiteFilter, TextSearchFilter
from .tools import annotate_record

class AssemblyError(Exception):
    pass

class FragmentsChain:
    """Class to represent a set of DNA fragments that can assemble into
    a linear or circular construct.

    Parameters
    ----------

    fragments
      A list of fragments that can be assembled into a linear/cicular construct.

    is_standardized
      Indicates whether the fragment is in standardized form, which saves time
      by avoiding to standardize the fragment more than once.

    is_cycle
      Indicates whether the fragments are expected to assemble circularly

    Note
    ----
    Importantly these objects are not meant to be modified inplace as their
    hashes are cached to accelerate computations
    """

    def __init__(self, fragments, is_standardized=False, is_cycle=False):
        self.fragments = fragments
        self.is_standardized = is_standardized
        self.is_cycle = is_cycle
        self._hash = None

    def reverse_complement(self):
        return FragmentsChain([f.reverse_fragment
                              for f in self.fragments][::-1],
                              is_cycle=self.is_cycle)

    def standardized(self):
        """Return a standardized version of the cycle.

        Useful for spotting cycles that may look different but are just
        two representations of a same circular DNA construct.

        For instance, a cycle with fragments A-B-C represents the same
        construct as C-A-B, or even rev(C)-rev(B)-rev(A) (reverse complement).

        The standardization works as follows:

        - If more than half of the fragments in the cycle are
          "reverse complement" fragments, consider the reverse version of
          the cycle. This way all standardized cycles have less than 50%
          rev-complement fragments
        - If the chaing is a cycle it is "rotated" so that the first fragment
          of the cycle is the largest fragment. If there are several fragments
          of same largest size we choose the first one in alphabetical order of
          the sequence.
        """

        if self.is_standardized:
            # Note: return a copy but don't use deepcopy here
            # it's a computing bottleneck
            new_chain = FragmentsChain(self.fragments, self.is_standardized,
                                       is_cycle=self.is_cycle)
            new_chain._hash = self._hash
            return new_chain

        reverse_proportion = (sum(len(f)
                                  for f in self.fragments
                                  if f.is_reverse) /
                              float(sum(len(f) for f in self.fragments)))
        if reverse_proportion == 0.5:
            f1, f2 = ["%s%s%s" % (f.seq.left_end, f.seq, f.seq.right_end)
                      for f in [self.fragments[0], self.fragments[-1]]]
            if f1 > f2:
                std_fragments = self.reverse_complement().fragments
            else:
                std_fragments = self.fragments
        if (reverse_proportion > 0.5):
            std_fragments = self.reverse_complement().fragments
        else:
            std_fragments = self.fragments


        if self.is_cycle:
            sequences = ["%s%s%s" % (f.seq.left_end, f.seq, f.seq.right_end)
                         for f in std_fragments]
            len_sequences = [len(sequence) for sequence in sequences]
            index = min(range(len(sequences)),
                        key=lambda i: (-len_sequences[i], sequences[i]))
            std_fragments = std_fragments[index:] + std_fragments[:index]

        return FragmentsChain(std_fragments, is_standardized=True,
                              is_cycle=self.is_cycle)

    def __hash__(self):
        """The hash of the cycle is the hash of the concatenation of the
        fragments in the standardized version of the cycle."""

        if self._hash is None:
            self._hash = hash("".join([
                "%s%s%s" % (f.seq.left_end, f.seq, f.seq.right_end)
                for f in self.standardized().fragments
            ]))
        return self._hash


class AssemblyMix:
    """General class for assembly mixes.

    The subclasses (RestrictionLigationMix and GibsonAssemblyMix) implement
    their own version of how the original constructs are broken into
    fragments, when two fragments will clip together, etc.
    """

    def compute_connections_graph(self):
        """Compute a graph where nodes are fragments and edges indicate
        which fragments can clip together.

        The graph (stored in self.connection_graph) is directed, an edge
        f1->f2 indicating that fragments f1 and f2 will clip in this order.
        """

        all_fragments = self.fragments + self.reverse_fragments
        items = list(enumerate(all_fragments))
        self.fragments_dict = dict(items)
        self.connections_graph = nx.DiGraph()
        for (i1, fragment1), (i2, fragment2) in itt.combinations(items, 2):
            if self.will_clip_in_this_order(fragment1, fragment2):
                self.connections_graph.add_edge(i1, i2)
            if self.will_clip_in_this_order(fragment2, fragment1):
                self.connections_graph.add_edge(i2, i1)

    def compute_filtered_connections_graph(self, fragments_filters):
        graph = nx.DiGraph(self.connections_graph)
        graph.remove_nodes_from([
            node for node in graph.nodes()
            if not all([fl(self.fragments_dict[node])
                        for fl in fragments_filters])
        ])
        return graph

    def compute_reverse_fragments(self):
        """Precompute self.reverse_fragments.

        This method also marks all "direct" fragments in the mix as
        `fragment.is_reverse=True` and all "reverse" fragments as
        `fragment.is_reverse=False`.
        """
        self.reverse_fragments = []
        for fragment in self.fragments:
            fragment.is_reverse = False
            new_fragment = fragment.reverse_complement()
            new_fragment.is_reverse = True
            new_fragment.reverse_fragment = fragment
            fragment.reverse_fragment = new_fragment
            new_fragment.original_construct = fragment.original_construct
            self.reverse_fragments.append(new_fragment)

    def initialize(self):
        """Precompute the fragments and connections graph of the mix."""
        if self.constructs is not None:
            for construct in self.constructs:
                if not hasattr(construct, "linear"):
                    construct.linear = True  # assumed linear by default
        if not hasattr(self, "fragments") or self.fragments is None:
            self.compute_fragments()
        self.compute_reverse_fragments()
        self.compute_connections_graph()

    def compute_circular_fragments_sets(self, fragments_sets_filters=(),
                                        fragments_filters=(),
                                        randomize=False,
                                        randomization_staling_cutoff=100):
        """Return an iterator over all the lists of fragments [f1, f2, f3...fn]
        that can assemble into a circular construct.

        This means that fragment f1 will clip with f2 (in this order),
        f2 with f3... and fn with f1.

        Examples
        --------

        >>>

        Parameters
        ----------

        fragments_sets_filters
          A list of test functions of the form (set->True/False) where "set" is
          a list of fragments from the mix (which assemble into a circular
          construct). Only circular fragments sets passing all these tests
          will be returned

        fragments_filters
          A list of test functions of the form (fragment->True/False) where
          fragment is a fragment of the mix (potentially with sticky ends)
          Only fragments passing all these tests are considered. Filtering
          out fragments can dramatically decrease computing times. Use it.

        randomize
          If set to False, the circular fragments sets will be returned one by
          one until the last one, in an order implemented by
          networkx.simple_cycles.
          True, the circular sets returned will be drawn randomly
          (a circular set will only be returned once). This is very practical
          to obtain a sample out of a combinatorial assembly mix. However this
          feature is a bit experimental, and the iteration will certainly stale
          before all cycles have been found, because the randomizer can't find
          any new cycle.

        randomization_staling_cutoff
          If randomize is True, the randomizer will throw an error if the
          latest C cycles it has drawn had already been seen before, where C
          is the randomization staling cutoff.

        """
        graph = self.compute_filtered_connections_graph(fragments_filters)

        if randomize:
            def circular_fragments_sets_generator():
                """Return random cycles from the connections graph.

                The randomness is introduced by permuting the nodes names,
                running `networkx.circular_paths` once, permuting the nodes
                names again, etc.
                """

                original_adj = deepcopy(graph.adj)
                seen_hashes = set()
                while True:
                    permutation = np.arange(len(self.connections_graph.nodes()))
                    np.random.shuffle(permutation)
                    antipermutation = np.argsort(permutation)
                    graph.adj = {
                        permutation[node]: {
                            permutation[n]: v
                            for n, v in children.items()
                        }
                        for node, children in original_adj.items()
                    }
                    counter = 0
                    for cycle in nx.simple_cycles(graph):
                        cycle = [antipermutation[i] for i in cycle]
                        fragments = [self.fragments_dict[i] for i in cycle]
                        cycle = FragmentsChain(fragments,
                                               is_cycle=True).standardized()
                        cycle_hash = hash(cycle)
                        if cycle_hash in seen_hashes:
                            counter += 1
                            if counter > randomization_staling_cutoff:
                                raise ValueError(
                                    "Randomization staled. Only randomize when"
                                    " the search space is huge."
                                )
                            continue
                        seen_hashes.add(cycle_hash)
                        if all(fl(cycle.fragments)
                               for fl in fragments_sets_filters):
                            yield cycle.fragments
                            break
                    else:
                        break
        else:
            def circular_fragments_sets_generator():
                """Iterate over all circular paths in the connexion graph
                using Networkx's `simple_paths`."""
                seen_hashes = set()
                for cycle in nx.simple_cycles(graph):
                    cycle = [self.fragments_dict[i] for i in cycle]
                    cycle = FragmentsChain(cycle, is_cycle=True).standardized()
                    cycle_hash = hash(cycle)
                    if cycle_hash in seen_hashes:
                        continue
                    seen_hashes.add(cycle_hash)
                    if all(fl(cycle.fragments)
                           for fl in fragments_sets_filters):
                        yield cycle.fragments

        return circular_fragments_sets_generator()



    def compute_circular_assemblies(self, fragments_sets_filters=(),
                                    fragments_filters=(),
                                    seqrecord_filters=(),
                                    annotate_homologies=False,
                                    randomize=False,
                                    randomization_staling_cutoff=100):

        def assemblies_generator():
            for fragments in self.compute_circular_fragments_sets(
                fragments_sets_filters=fragments_sets_filters,
                fragments_filters=fragments_filters,
                randomize=randomize,
                randomization_staling_cutoff=randomization_staling_cutoff
            ):
                construct = self.assemble(
                    fragments,
                    circularize=True,
                    annotate_homologies=annotate_homologies
                )
                if all(fl(construct) for fl in seqrecord_filters):
                    construct.fragments = fragments
                    yield construct
        return assemblies_generator()

    def compute_linear_assemblies(self,
                                  fragments_sets_filters=(),
                                  min_parts=2,
                                  fragments_filters=(),
                                  seqrecord_filters=(),
                                  annotate_homologies=False):
        self.compute_filtered_connections_graph(fragments_filters)
        seen_hashes = set()
        g = self.compute_filtered_connections_graph(fragments_filters)
        for source, targets in nx.shortest_path(g).items():
            for target, path in targets.items():
                if (len(path) < min_parts):
                    continue
                fragments = [self.fragments_dict[f] for f in path]
                if not all([fl(fragments) for fl in fragments_sets_filters]):
                    continue
                chain = FragmentsChain(fragments).standardized()
                chain_hash = hash(chain)
                if chain_hash in seen_hashes:
                    continue
                seen_hashes.add(chain_hash)
                fragments_assembly = self.assemble(
                    fragments, annotate_homologies=annotate_homologies)
                if all([fl(fragments_assembly) for fl in seqrecord_filters]):
                    yield(fragments_assembly)




class RestrictionLigationMix(AssemblyMix):
    """Assembly mix for an enzymatic Restriction Ligation assembly.

    This includes modern assembly techniques such as Golden Gate as well as
    classical enzyme-based assembly.

    Parameters
    ----------

    constructs
      List of Biopython Seqrecords. Each seqrecord should have an attribute
      `linear` set to true or false (for circular constructs). It is advised to
      use method `load_genbank(filename, linear=True)` from `dnacauldron.tools`
      to load the constructs.

    enzyme
      Name of the ligation enzyme to use, e.g. 'BsmBI'
    """

    def __init__(self, constructs=None, enzyme=None, fragments=None):

        self.constructs = deepcopy(constructs) if constructs else constructs
        self.fragments = deepcopy(fragments) if fragments else fragments
        self.enzyme = None if enzyme is None else Restriction.__dict__[enzyme]
        self.initialize()


    def compute_digest(self, construct):
        """Compute the fragments resulting from the digestion"""
        return digest_seqrecord_with_sticky_ends(
            construct, self.enzyme, linear=construct.linear)

    def compute_fragments(self):
        """Compute the (sticky-ended) fragments resulting from the digestion of
        the mix's constructs by the mix's enzyme.

        Note that all fragments receive an annotation (feature) of type
        "source" that will show in the genbank of final constructs.
        """
        self.fragments = []
        for construct in self.constructs:

            for fragment in self.compute_digest(construct):
                if not isinstance(fragment, StickyEndsSeqRecord):
                    continue
                fragment.original_construct = construct
                annotate_record(
                    fragment,
                    feature_type="misc_feature",
                    source=construct.name,
                    note="From " + construct.name,

                )
                self.fragments.append(fragment)

    @staticmethod
    def assemble(fragments, circularize=False, annotate_homologies=False):
        """Assemble sticky-end fragments into a single one (sticky or not).

        Parameters
        ----------

        fragments
          List of StickyEndsSeqRecord fragments

        circularize
          If True and if the two ends of the final assembly are compatible,
          circularize the construct, i.e. return a non-sticky record
          representing the circular assembly of the fragments.

        annotate_homologies
          If True, all homology regions that where formerly sticky ends will
          be annotated in the final record.
        """
        return StickyEndsSeqRecord.assemble(
            fragments,
            circularize=circularize,
            annotate_homologies=annotate_homologies
        )

    @staticmethod
    def will_clip_in_this_order(fragment1, fragment2):
        return fragment1.will_clip_in_this_order_with(fragment2)

class BASICLigationMix(RestrictionLigationMix):

    @staticmethod
    def find_adapter(record):
        for feature in record.features:
                label = feature.qualifiers.get("label", "")
                if isinstance(label, list):
                    label = label[0]
                if label == "adapter":
                    return (
                        int(feature.location.start),
                        int(feature.location.end),
                        feature.location.strand
                    )
        return None

    def compute_digest(self, construct):

        adapter = self.find_adapter(construct)
        if adapter:
            start, end, strand = adapter
            left_end = StickyEnd(str(construct[:start].seq), strand=1)
            right_end = StickyEnd(str(construct[end:].seq), strand=1)
            sequence = StickyEndsSeq(str(construct[start:end].seq),
                                     left_end=left_end,
                                     right_end=right_end)
            sequence.alphabet = DNAAlphabet()
            record = StickyEndsSeqRecord(seq=sequence)
            annotate_record(record, location=(0, len(sequence), 1),
                            label="adapter")
            return [record]
        else:
            # No feature shows that this is an adapter: use simple restriction
            return RestrictionLigationMix.compute_digest(self, construct)

    @staticmethod
    def assemble_constructs_and_linkers(records_list, enzyme="BsaI"):
        enzyme_filter = NoRestrictionSiteFilter(enzyme)
        def fragments_filter(fragment):
            return (BASICLigationMix.find_adapter(fragment) or
                    enzyme_filter(fragment))
        fragments = []
        for linker_left, part, linker_right in records_list:
            linker_left.linear = True
            linker_right.linear = True
            if not isinstance(part, list):
                part = [part]

            for p in part:
                mix = BASICLigationMix([linker_left, p, linker_right],
                                       enzyme="BsaI")
                mix.compute_linear_assemblies
                new_fragment = list(mix.compute_linear_assemblies(
                    fragments_sets_filters=(),
                    min_parts=3,
                    fragments_filters=[fragments_filter],
                    seqrecord_filters=[TextSearchFilter("adapter")],
                    annotate_homologies=False
                ))
                if len(new_fragment) != 1:
                    part_names = str([linker_left.name, p.name,
                                      linker_right.name])
                    raise ValueError(
                        "Something weird happened when trying to assemble "
                        "%s. %d assemblies found" % (
                            part_names, len(new_fragment)))
                new_fragment = new_fragment[0]
                new_fragment.original_construct = p
                fragments.append(new_fragment)
        final_mix = BASICLigationMix(fragments=fragments)
        final_mix.compute_reverse_fragments()
        return final_mix.compute_circular_assemblies()


class GibsonAssemblyMix(AssemblyMix):
    """In construction. Do not use."""

    def __init__(self, constructs, min_homology=15, max_homology=200):

        self.constructs = deepcopy(constructs)
        self.min_homology = min_homology
        self.max_homology = max_homology
        self.initialize()

    def compute_fragments(self):
        self.fragments = list(self.constructs)

    @staticmethod
    def assemble(fragments, circularize=False, annotate_homologies=False):
        return StickyEndsSeqRecord.assemble(
            fragments,
            circularize=False,
            annotate_homologies=annotate_homologies
        )
