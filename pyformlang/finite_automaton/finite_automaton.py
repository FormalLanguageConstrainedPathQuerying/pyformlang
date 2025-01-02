"""A general finite automaton representation."""

from typing import Dict, List, Set, Tuple, \
    Iterable, Iterator, Optional, Hashable, Any, TypeVar
from abc import abstractmethod
from collections import deque
from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import write_dot

from pyformlang.fst import FST

from .transition_function import TransitionFunction
from ..objects.finite_automaton_objects import State, Symbol, Epsilon
from ..objects.finite_automaton_objects.utils import to_state, to_symbol

AutomatonT = TypeVar("AutomatonT", bound="FiniteAutomaton")


class FiniteAutomaton(Iterable[Tuple[State, Symbol, State]]):
    """A general finite automaton representation.

    Attributes
    ----------
    _states:
        A finite set of states.
    _input_symbols:
        A finite set of input symbols.
    _transition_function:
        A function that takes as arguments a state and an input symbol and
        returns a set of states.
    _start_states:
        A set of start or initial states. It is a subset of _states.
    _final_states:
        A set of final or accepting states. It is a subset of _states.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Initializes a finite automaton."""
        self._states: Set[State]
        self._input_symbols: Set[Symbol]
        self._transition_function: TransitionFunction
        self._start_states: Set[State]
        self._final_states: Set[State]

    @property
    def states(self) -> Set[State]:
        """Gets the states of the automaton."""
        return self._states

    @property
    def symbols(self) -> Set[Symbol]:
        """Gets the input alphabet of the automaton."""
        return self._input_symbols

    @property
    def start_states(self) -> Set[State]:
        """Gets the start states of the automaton."""
        return self._start_states

    @property
    def final_states(self) -> Set[State]:
        """Gets the final states of the automaton."""
        return self._final_states

    def add_transition(self,
                       s_from: Hashable,
                       symb_by: Hashable,
                       s_to: Hashable) -> int:
        """Adds the given transition to the automaton.

        Parameters
        ----------
        s_from:
            The source state.
        symb_by:
            The transition symbol.
        s_to:
            The destination state.

        Returns
        -------
        Always 1

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transition(0, "abc", 1)
        """
        s_from = to_state(s_from)
        symb_by = to_symbol(symb_by)
        s_to = to_state(s_to)
        temp = self._transition_function.add_transition(s_from, symb_by, s_to)
        self._states.add(s_from)
        self._states.add(s_to)
        if symb_by != Epsilon():
            self._input_symbols.add(symb_by)
        return temp

    def add_transitions(self, transitions_list: \
            Iterable[Tuple[Hashable, Hashable, Hashable]]) -> int:
        """Adds several transitions to the automaton.

        Parameters
        ----------
        transitions_list:
            A list of all the transitions represented as triples as they
            would be used in add_transition.

        Returns
        -------
        Always 1

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        """
        temp = 0
        for s_from, symb_by, s_to in transitions_list:
            temp = self.add_transition(s_from, symb_by, s_to)
        return temp

    def remove_transition(self,
                          s_from: Hashable,
                          symb_by: Hashable,
                          s_to: Hashable) -> int:
        """Removes a transition from the automaton.

        Parameters
        ----------
        s_from:
            The source state.
        symb_by:
            The transition symbol.
        s_to:
            The destination state.

        Returns
        -------
        1 if the transition existed, 0 otherwise.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transition(0, "abc", 1)
        >>> enfa.remove_transition(0, "abc", 1)
        """
        s_from = to_state(s_from)
        symb_by = to_symbol(symb_by)
        s_to = to_state(s_to)
        return self._transition_function.remove_transition(s_from,
                                                           symb_by,
                                                           s_to)

    def get_number_transitions(self) -> int:
        """Gets the number of transitions in the automaton.

        Returns
        -------
        The number of transitions in the automaton.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.get_number_transitions()
        3
        """
        return self._transition_function.get_number_transitions()

    def add_start_state(self, state: Hashable) -> int:
        """Adds an initial state to the automaton.

        Parameters
        ----------
        state:
            The initial state to add.

        Returns
        -------
        1 is correctly added.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        """
        state = to_state(state)
        self._start_states.add(state)
        self._states.add(state)
        return 1

    def remove_start_state(self, state: Hashable) -> int:
        """Removes an initial state from the automaton.

        Parameters
        ----------
        state:
            The initial state to remove.

        Returns
        -------
        1 is correctly removed.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.remove_start_state(0)
        """
        state = to_state(state)
        if state in self._start_states:
            self._start_states.remove(state)
            return 1
        return 0

    def add_final_state(self, state: Hashable) -> int:
        """Adds a new final state to the automaton.

        Parameters
        ----------
        state:
            A final state to add.

        Returns
        -------
        1 is correctly added.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        """
        state = to_state(state)
        self._final_states.add(state)
        self._states.add(state)
        return 1

    def remove_final_state(self, state: Hashable) -> int:
        """Removes a final state from the automaton.

        Parameters
        ----------
        state:
            A final state to remove.

        Returns
        -------
        0 if it was not a final state, 1 otherwise.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa.remove_final_state(1)
        """
        state = to_state(state)
        if self.is_final_state(state):
            self._final_states.remove(state)
            return 1
        return 0

    def __call__(self, s_from: Hashable, symb_by: Hashable) -> Set[State]:
        """Calls the transition function of the automaton.

        Parameters
        ----------
        state:
            The source state.
        symbol:
            The transition symbol.

        Returns
        -------
        The next states defined by the transition function.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa(0, "abc")
        [1]
        """
        s_from = to_state(s_from)
        symb_by = to_symbol(symb_by)
        return self._transition_function(s_from, symb_by)

    def __contains__(self,
                     transition: Tuple[Hashable, Hashable, Hashable]) -> bool:
        """Checks if the given transition is present in finite automaton."""
        s_from, symb_by, s_to = transition
        s_from = to_state(s_from)
        symb_by = to_symbol(symb_by)
        s_to = to_state(s_to)
        return (s_from, symb_by, s_to) in self._transition_function

    def get_transitions_from(self, s_from: Hashable) \
            -> Iterable[Tuple[Symbol, State]]:
        """Gets transitions from the given state.

        Parameters
        ----------
        s_from:
            A state to get transitions from.

        Yields
        ------
        Pairs of transition symbol and destination state.
        """
        s_from = to_state(s_from)
        return self._transition_function.get_transitions_from(s_from)

    def get_next_states_from(self, s_from: Hashable) -> Set[State]:
        """Gets a set of states that are next to the given one.

        Parameters
        ----------
        s_from:
            A state to get next states from.

        Returns
        -------
        A set of next states defined by the transition function.
        """
        s_from = to_state(s_from)
        return self._transition_function.get_next_states_from(s_from)

    def is_final_state(self, state: Hashable) -> bool:
        """Checks if a state is final in the automaton.

        Parameters
        -----------
        state:
            The state to check.

        Returns
        -------
        Whether the state is final or not.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa.is_final_state(1)
        True
        """
        state = to_state(state)
        return state in self._final_states

    def add_symbol(self, symbol: Hashable) -> None:
        """Adds the given symbol to the input alphabet.

        Parameters
        ----------
        symbol:
            The symbol to add.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_symbol("a")
        """
        symbol = to_symbol(symbol)
        self._input_symbols.add(symbol)

    def to_fst(self) -> FST:
        """Turns the finite automaton into a finite state transducer.

        The transducers accepts only the words in the language of the
        automaton and output the input word.

        Returns
        -------
        The equivalent FST.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> fst = enfa.to_fst()
        >>> fst.states
        {}
        """
        fst = FST()
        for start_state in self._start_states:
            fst.add_start_state(start_state)
        for final_state in self._final_states:
            fst.add_final_state(final_state)
        for s_from, symb_by, s_to in self._transition_function:
            fst.add_transition(s_from,
                               symb_by,
                               s_to,
                               [symb_by])
        return fst

    def is_acyclic(self) -> bool:
        """Checks if the automaton is acyclic.

        Returns
        -------
        Whether the automaton is acyclic or not.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa.is_acyclic()
        True
        """
        to_process = []
        for state in self._start_states:
            to_process.append((state, set()))
        while to_process:
            current, visited = to_process.pop()
            if current in visited:
                return False
            visited.add(current)
            for symbol in self._input_symbols:
                for state in self(current, symbol):
                    to_process.append((state, visited.copy()))
            # Epsilon
            for state in self(current, Epsilon()):
                to_process.append((state, visited.copy()))
        return True

    def to_networkx(self) -> MultiDiGraph:
        """Transforms the current automaton into a networkx graph.

        Returns
        -------
        A networkx MultiDiGraph representing the automaton.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> graph = enfa.to_networkx()
        """
        graph = MultiDiGraph()
        for state in self._states:
            graph.add_node(state.value,
                           is_start=state in self.start_states,
                           is_final=state in self.final_states,
                           peripheries=2 if state in self.final_states else 1,
                           label=state.value)
            if state in self.start_states:
                self.__add_start_state_to_graph(graph, state)
        for s_from, symbol, s_to in self._transition_function.get_edges():
            label_ = symbol.value
            if label_ == 'epsilon':
                label_ = 'ɛ'
            graph.add_edge(s_from.value, s_to.value, label=label_)
        return graph

    @classmethod
    @abstractmethod
    def from_networkx(cls, graph: MultiDiGraph) -> "FiniteAutomaton":
        """Import a networkx graph into an finite state automaton.

        The imported graph requires to have the good format, i.e. to come
        from the function `to_networkx`.

        Returns
        -------
        The imported finite automaton.
        """
        raise NotImplementedError

    def write_as_dot(self, filename: str) -> None:
        """Writes the automaton in dot format into a file.

        Parameters
        ----------
        filename:
            A name of the file to write the dot file to.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa.write_as_dot("enfa.dot")
        """
        write_dot(self.to_networkx(), filename)

    @abstractmethod
    def accepts(self, word: Iterable[Hashable]) -> bool:
        """Checks whether the finite automaton accepts a given word.

        Parameters
        ----------
        word:
            an iterable of input symbols.

        Returns
        -------
        Whether the given word is accepted or not.
        """
        raise NotImplementedError

    def get_accepted_words(self, max_length: Optional[int] = None) \
            -> Iterable[List[Symbol]]:
        """Gets words accepted by the finite automaton.

        Parameters
        ----------
        max_length:
            A max length of the generated words.

        Yields
        ------
        Words accepted by current automaton.
        """
        if max_length is not None and max_length < 0:
            return
        states_to_visit = deque((start_state, [])
                                for start_state in self.start_states)
        states_leading_to_final = self._get_states_leading_to_final()
        words_by_state = {state: set() for state in self.states}
        yielded_words = set()
        while states_to_visit:
            current_state, current_word = states_to_visit.popleft()
            if max_length is not None and len(current_word) > max_length:
                continue
            word_to_add = tuple(current_word)
            if not self.__try_add(words_by_state[current_state], word_to_add):
                continue
            transitions = self.get_transitions_from(current_state)
            for symbol, next_state in transitions:
                if next_state in states_leading_to_final:
                    temp_word = current_word.copy()
                    if symbol != Epsilon():
                        temp_word.append(symbol)
                    states_to_visit.append((next_state, temp_word))
            if self.is_final_state(current_state):
                if self.__try_add(yielded_words, word_to_add):
                    yield current_word

    def _get_states_leading_to_final(self) -> Set[State]:
        """Gets a set of states that lead to final ones from start.

        Returns
        -------
        A set of states that are on path from start state
        to one of the final states.
        """
        leading_to_final = self.final_states.copy()
        visited = set()
        states_to_process: deque[Any] = \
            deque((None, start_state) for start_state in self.start_states)
        delayed_states = deque()
        while states_to_process:
            previous_state, current_state = states_to_process.pop()
            if previous_state and current_state in leading_to_final:
                leading_to_final.add(previous_state)
                continue
            if current_state in visited:
                delayed_states.append((previous_state, current_state))
                continue
            visited.add(current_state)
            next_states = self.get_next_states_from(current_state)
            if next_states:
                states_to_process.append((previous_state, current_state))
                for next_state in next_states:
                    states_to_process.append((current_state, next_state))
        for previous_state, current_state in delayed_states:
            if previous_state and current_state in leading_to_final:
                leading_to_final.add(previous_state)
        return leading_to_final

    def _get_reachable_states(self) -> Set[State]:
        """Gets all states which are reachable in the automaton."""
        visited = set()
        states_to_process = deque(self.start_states)
        while states_to_process:
            current_state = states_to_process.popleft()
            visited.add(current_state)
            for next_state in self.get_next_states_from(current_state):
                if next_state not in visited:
                    states_to_process.append(next_state)
        return visited

    def __len__(self) -> int:
        """Gets the number of transitions in the automaton."""
        return len(self._transition_function)

    def __iter__(self) -> Iterator[Tuple[State, Symbol, State]]:
        """Yields the transitions described by the transition function."""
        yield from self._transition_function

    def to_dict(self) -> Dict[State, Dict[Symbol, Set[State]]]:
        """Get the dictionary representation of the transition function.

        The keys of the dictionary are the source nodes. The items are
        dictionaries where the keys are the symbols of the transitions and
        the items are the set of target nodes.

        Returns
        -------
        The transition function as a dictionary.

        Examples
        --------
        >>> enfa = EpsilonNFA()
        >>> enfa.add_transitions([(0, "abc", 1), (0, "d", 1), \
        (0, "epsilon", 2)])
        >>> enfa.add_start_state(0)
        >>> enfa.add_final_state(1)
        >>> enfa_dict = enfa.to_dict()
        """
        return self._transition_function.to_dict()

    @abstractmethod
    def copy(self: AutomatonT) -> AutomatonT:
        """Copies the current Finite Automaton instance.

        Returns
        -------
        The copy of current finite automaton.
        """
        raise NotImplementedError

    def __copy__(self: AutomatonT) -> AutomatonT:
        """Copies the current Finite Automaton instance."""
        return self.copy()

    def _copy_to(self, fa_to_copy_to: AutomatonT) -> AutomatonT:
        """Copies current automaton properties to the given one.

        Parameters
        ----------
        fa_to_copy_to:
            An automaton to copy current properties to.

        Returns
        -------
        The given automaton instance after copying.
        """
        for start in self._start_states:
            fa_to_copy_to.add_start_state(start)
        for final in self._final_states:
            fa_to_copy_to.add_final_state(final)
        for state in self._states:
            for symbol in self._input_symbols:
                states = self._transition_function(state, symbol)
                for state_to in states:
                    fa_to_copy_to.add_transition(state, symbol, state_to)
            states = self._transition_function(state, Epsilon())
            for state_to in states:
                fa_to_copy_to.add_transition(state, Epsilon(), state_to)
        return fa_to_copy_to

    @abstractmethod
    def is_deterministic(self) -> bool:
        """Checks if current automaton is deterministic.

        Returns
        -------
        Whether the automaton is deterministic or not.
        """
        raise NotImplementedError

    @staticmethod
    def __try_add(set_to_add_to: Set[Any], element_to_add: Any) -> bool:
        """Tries to add a given element to the given set.

        Returns
        -------
        True if element was added, otherwise False.
        """
        initial_length = len(set_to_add_to)
        set_to_add_to.add(element_to_add)
        return len(set_to_add_to) != initial_length

    @staticmethod
    def __add_start_state_to_graph(graph: MultiDiGraph, state: State) -> None:
        """Adds a starting node to a given graph."""
        graph.add_node("starting_" + str(state),
                       label="",
                       shape=None,
                       height=.0,
                       width=.0)
        graph.add_edge("starting_" + str(state),
                       state.value)
