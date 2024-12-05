""" Finite State Transducer """

from typing import Dict, List, Set, Tuple, Iterator, Iterable, Hashable
from copy import deepcopy
from json import dumps, loads

from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import write_dot

from .utils import StateRenaming
from ..objects.finite_automaton_objects import State, Symbol, Epsilon
from ..objects.finite_automaton_objects.utils import to_state, to_symbol

TransitionKey = Tuple[State, Symbol]
TransitionValue = Tuple[State, Tuple[Symbol, ...]]
TransitionValues = Set[TransitionValue]
TransitionFunction = Dict[TransitionKey, TransitionValues]

InputTransition = Tuple[Hashable, Hashable, Hashable, Iterable[Hashable]]
Transition = Tuple[TransitionKey, TransitionValue]


class FST(Iterable[Transition]):
    """ Representation of a Finite State Transducer"""

    def __init__(self) -> None:
        self._states: Set[State] = set()  # Set of states
        self._input_symbols: Set[Symbol] = set()  # Set of input symbols
        self._output_symbols: Set[Symbol] = set()  # Set of output symbols
        # Dict from _states x _input_symbols U {epsilon} into a subset of
        # _states X _output_symbols*
        self._delta: TransitionFunction = {}
        self._start_states: Set[State] = set()
        self._final_states: Set[State] = set()  # _final_states is final states

    @property
    def states(self) -> Set[State]:
        """ Get the states of the FST

        Returns
        ----------
        states : set of any
            The states
        """
        return self._states

    @property
    def input_symbols(self) -> Set[Symbol]:
        """ Get the input symbols of the FST

        Returns
        ----------
        input_symbols : set of any
            The input symbols of the FST
        """
        return self._input_symbols

    @property
    def output_symbols(self) -> Set[Symbol]:
        """ Get the output symbols of the FST

        Returns
        ----------
        output_symbols : set of any
            The output symbols of the FST
        """
        return self._output_symbols

    @property
    def start_states(self) -> Set[State]:
        """ Get the start states of the FST

        Returns
        ----------
        start_states : set of any
            The start states of the FST
        """
        return self._start_states

    @property
    def final_states(self) -> Set[State]:
        """ Get the final states of the FST

        Returns
        ----------
        final_states : set of any
            The final states of the FST
        """
        return self._final_states

    def get_number_transitions(self) -> int:
        """ Get the number of transitions in the FST

        Returns
        ----------
        n_transitions : int
            The number of transitions
        """
        return sum(len(x) for x in self._delta.values())

    def add_transition(self,
                       s_from: Hashable,
                       input_symbol: Hashable,
                       s_to: Hashable,
                       output_symbols: Iterable[Hashable]) -> None:
        """ Add a transition to the FST

        Parameters
        -----------
        s_from : any
            The source state
        input_symbol : any
            The symbol to read
        s_to : any
            The destination state
        output_symbols : iterable of Any
            The symbols to output
        """
        s_from = to_state(s_from)
        input_symbol = to_symbol(input_symbol)
        s_to = to_state(s_to)
        output_symbols = tuple(to_symbol(x) for x in output_symbols
                               if x != Epsilon())
        self._states.add(s_from)
        self._states.add(s_to)
        if input_symbol != Epsilon():
            self._input_symbols.add(input_symbol)
        self._output_symbols.update(output_symbols)
        head = (s_from, input_symbol)
        if head in self._delta:
            self._delta[head].add((s_to, output_symbols))
        else:
            self._delta[head] = {(s_to, output_symbols)}

    def add_transitions(self, transitions: Iterable[InputTransition]) -> None:
        """
        Adds several transitions to the FST

        Parameters
        ----------
        transitions_list : list of tuples
            The tuples have the form (s_from, in_symbol, s_to, out_symbols)
        """
        for s_from, input_symbol, s_to, output_symbols in transitions:
            self.add_transition(s_from,
                                input_symbol,
                                s_to,
                                output_symbols)

    def add_start_state(self, start_state: Hashable) -> None:
        """ Add a start state

        Parameters
        ----------
        start_state : any
            The start state
        """
        start_state = to_state(start_state)
        self._states.add(start_state)
        self._start_states.add(start_state)

    def add_final_state(self, final_state: Hashable) -> None:
        """ Add a final state

        Parameters
        ----------
        final_state : any
            The final state to add
        """
        final_state = to_state(final_state)
        self._final_states.add(final_state)
        self._states.add(final_state)

    def __call__(self, s_from: Hashable, input_symbol: Hashable) \
            -> TransitionValues:
        """ Calls the transition function of the FST """
        s_from = to_state(s_from)
        input_symbol = to_symbol(input_symbol)
        return self._delta.get((s_from, input_symbol), set())

    def __contains__(self, transition: InputTransition) -> bool:
        """ Whether the given transition is present in the FST """
        s_from, input_symbol, s_to, output_symbols = transition
        s_from = to_state(s_from)
        input_symbol = to_symbol(input_symbol)
        s_to = to_state(s_to)
        output_symbols = tuple(to_symbol(x) for x in output_symbols)
        return (s_to, output_symbols) in self(s_from, input_symbol)

    def __iter__(self) -> Iterator[Transition]:
        """ Gets an iterator of transitions of the FST """
        for key, values in self._delta.items():
            for value in values:
                yield key, value

    def translate(self,
                  input_word: Iterable[Hashable],
                  max_length: int = -1) -> Iterable[List[Symbol]]:
        """ Translate a string into another using the FST

        Parameters
        ----------
        input_word : iterable of any
            The word to translate
        max_length : int, optional
            The maximum size of the output word, to prevent infinite \
            generation due to epsilon transitions

        Returns
        ----------
        output_word : iterable of any
            The translation of the input word
        """
        # (remaining in the input, generated so far, current_state)
        input_word = [to_symbol(x) for x in input_word if x != Epsilon()]
        to_process: List[Tuple[List[Symbol], List[Symbol], State]] = []
        seen_by_state = {state: [] for state in self.states}
        for start_state in self._start_states:
            to_process.append((input_word, [], start_state))
        while to_process:
            remaining, generated, current_state = to_process.pop()
            if (remaining, generated) in seen_by_state[current_state]:
                continue
            seen_by_state[current_state].append((remaining, generated))
            if len(remaining) == 0 and current_state in self._final_states:
                yield generated
            # We try to read an input
            if len(remaining) != 0:
                for next_state, output_symbols in self(current_state,
                                                       remaining[0]):
                    to_process.append(
                        (remaining[1:],
                         generated + list(output_symbols),
                         next_state))
            # We try to read an epsilon transition
            if max_length == -1 or len(generated) < max_length:
                for next_state, output_symbols in self(current_state,
                                                       Epsilon()):
                    to_process.append((remaining,
                                       generated + list(output_symbols),
                                       next_state))

    def union(self, other_fst: "FST") -> "FST":
        """
        Makes the union of two fst
        Parameters
        ----------
        other_fst : :class:`~pyformlang.fst.FST`
            The other FST

        Returns
        -------
        union_fst : :class:`~pyformlang.fst.FST`
            A new FST which is the union of the two given FST

        """
        state_renaming = self._get_state_renaming(other_fst)
        union_fst = FST()
        # pylint: disable=protected-access
        self._copy_into(union_fst, state_renaming, 0)
        other_fst._copy_into(union_fst, state_renaming, 1)
        return union_fst

    def __or__(self, other_fst: "FST") -> "FST":
        """
        Makes the union of two fst
        Parameters
        ----------
        other_fst : :class:`~pyformlang.fst.FST`
            The other FST

        Returns
        -------
        union_fst : :class:`~pyformlang.fst.FST`
            A new FST which is the union of the two given FST

        """
        return self.union(other_fst)

    def _copy_into(self,
                   union_fst: "FST",
                   state_renaming: StateRenaming,
                   idx: int) -> None:
        self._add_extremity_states_to(union_fst, state_renaming, idx)
        self._add_transitions_to(union_fst, state_renaming, idx)

    def _add_transitions_to(self,
                            union_fst: "FST",
                            state_renaming: StateRenaming,
                            idx: int) -> None:
        for head, transition in self._delta.items():
            s_from, input_symbol = head
            for s_to, output_symbols in transition:
                union_fst.add_transition(
                    state_renaming.get_renamed_state(s_from, idx),
                    input_symbol,
                    state_renaming.get_renamed_state(s_to, idx),
                    output_symbols)

    def _add_extremity_states_to(self,
                                 union_fst: "FST",
                                 state_renaming: StateRenaming,
                                 idx: int) -> None:
        self._add_start_states_to(union_fst, state_renaming, idx)
        self._add_final_states_to(union_fst, state_renaming, idx)

    def _add_final_states_to(self,
                             union_fst: "FST",
                             state_renaming: StateRenaming,
                             idx: int) -> None:
        for state in self.final_states:
            union_fst.add_final_state(
                state_renaming.get_renamed_state(state, idx))

    def _add_start_states_to(self,
                             union_fst: "FST",
                             state_renaming: StateRenaming,
                             idx: int) -> None:
        for state in self.start_states:
            union_fst.add_start_state(
                state_renaming.get_renamed_state(state, idx))

    def concatenate(self, other_fst: "FST") -> "FST":
        """
        Makes the concatenation of two fst
        Parameters
        ----------
        other_fst : :class:`~pyformlang.fst.FST`
            The other FST

        Returns
        -------
        fst_concatenate : :class:`~pyformlang.fst.FST`
            A new FST which is the concatenation of the two given FST

        """
        state_renaming = self._get_state_renaming(other_fst)
        fst_concatenate = FST()
        self._add_start_states_to(fst_concatenate, state_renaming, 0)
        # pylint: disable=protected-access
        other_fst._add_final_states_to(fst_concatenate, state_renaming, 1)
        self._add_transitions_to(fst_concatenate, state_renaming, 0)
        other_fst._add_transitions_to(fst_concatenate, state_renaming, 1)
        for final_state in self.final_states:
            for start_state in other_fst.start_states:
                fst_concatenate.add_transition(
                    state_renaming.get_renamed_state(final_state, 0),
                    Epsilon(),
                    state_renaming.get_renamed_state(start_state, 1),
                    []
                )
        return fst_concatenate

    def __add__(self, other: "FST") -> "FST":
        """
        Makes the concatenation of two fst
        Parameters
        ----------
        other : :class:`~pyformlang.fst.FST`
            The other FST

        Returns
        -------
        fst_concatenate : :class:`~pyformlang.fst.FST`
            A new FST which is the concatenation of the two given FST

        """
        return self.concatenate(other)

    def _get_state_renaming(self, other_fst: "FST") -> StateRenaming:
        state_renaming = StateRenaming()
        state_renaming.add_states(self.states, 0)
        state_renaming.add_states(other_fst.states, 1)
        return state_renaming

    def kleene_star(self) -> "FST":
        """
        Computes the kleene star of the FST

        Returns
        -------
        fst_star : :class:`~pyformlang.fst.FST`
            A FST representing the kleene star of the FST
        """
        fst_star = FST()
        state_renaming = StateRenaming()
        state_renaming.add_states(self.states, 0)
        self._add_extremity_states_to(fst_star, state_renaming, 0)
        self._add_transitions_to(fst_star, state_renaming, 0)
        for final_state in self.final_states:
            for start_state in self.start_states:
                fst_star.add_transition(
                    state_renaming.get_renamed_state(final_state, 0),
                    Epsilon(),
                    state_renaming.get_renamed_state(start_state, 0),
                    []
                )
        for final_state in self.start_states:
            for start_state in self.final_states:
                fst_star.add_transition(
                    state_renaming.get_renamed_state(final_state, 0),
                    Epsilon(),
                    state_renaming.get_renamed_state(start_state, 0),
                    []
                )
        return fst_star

    def to_networkx(self) -> MultiDiGraph:
        """
        Transform the current fst into a networkx graph

        Returns
        -------
        graph :  networkx.MultiDiGraph
            A networkx MultiDiGraph representing the fst

        """
        graph = MultiDiGraph()
        for state in self._states:
            graph.add_node(state,
                           is_start=state in self.start_states,
                           is_final=state in self.final_states,
                           peripheries=2 if state in self.final_states else 1,
                           label=state)
            if state in self.start_states:
                graph.add_node("starting_" + str(state),
                               label="",
                               shape=None,
                               height=.0,
                               width=.0)
                graph.add_edge("starting_" + str(state),
                               state)
        for s_from, input_symbol in self._delta:
            for s_to, output_symbols in self._delta[(s_from, input_symbol)]:
                graph.add_edge(
                    s_from,
                    s_to,
                    label=(dumps(input_symbol) + " -> " +
                           dumps(output_symbols)))
        return graph

    @classmethod
    def from_networkx(cls, graph: MultiDiGraph) -> "FST":
        """
        Import a networkx graph into an finite state transducer. \
        The imported graph requires to have the good format, i.e. to come \
        from the function to_networkx

        Parameters
        ----------
        graph :
            The graph representation of the FST

        Returns
        -------
        enfa :
            A FST read from the graph

        TODO
        -------
        * Explain the format
        """
        fst = FST()
        for s_from in graph:
            for s_to in graph[s_from]:
                for transition in graph[s_from][s_to].values():
                    if "label" in transition:
                        in_symbol, out_symbols = transition["label"].split(
                            " -> ")
                        in_symbol = loads(in_symbol)
                        out_symbols = loads(out_symbols)
                        fst.add_transition(s_from,
                                           in_symbol,
                                           s_to,
                                           out_symbols)
        for node in graph.nodes:
            if graph.nodes[node].get("is_start", False):
                fst.add_start_state(node)
            if graph.nodes[node].get("is_final", False):
                fst.add_final_state(node)
        return fst

    def write_as_dot(self, filename: str) -> None:
        """
        Write the FST in dot format into a file

        Parameters
        ----------
        filename : str
            The filename where to write the dot file

        """
        write_dot(self.to_networkx(), filename)

    def to_dict(self) -> TransitionFunction:
        """Gives the transitions as a dictionary"""
        return deepcopy(self._delta)
