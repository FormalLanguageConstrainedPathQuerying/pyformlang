"""Representation of a nondeterministic finite automaton."""

from typing import Iterable, Hashable

from .epsilon_nfa import EpsilonNFA
from ..objects.finite_automaton_objects import Epsilon
from ..objects.finite_automaton_objects.utils import to_symbol


class NondeterministicFiniteAutomaton(EpsilonNFA):
    """Representation of a nondeterministic finite automaton.

    This class represents a nondeterministic finite automaton, where epsilon
    transition are forbidden.

    Parameters
    ----------
    states:
        A finite set of states.
    input_symbols:
        A finite set of input symbols.
    transition_function:
        A function that takes as arguments a state and an input symbol
        and returns a set of states.
    start_states:
        A set of start or initial states. It is a subset of states.
    final_states:
        A set of final or accepting states. It is a subset of states.

    Examples
    --------
    >>> nfa = NondeterministicFiniteAutomaton()

    Creates the NFA.

    >>> nfa.add_transitions([(0, "a", 1), (0, "a", 2)])

    Adds two transitions.

    >>> nfa.add_start_state(0)

    Adds a start state.

    >>> nfa.add_final_state(1)

    Adds a final state.

    >>> nfa.accepts(["a"])
    True

    >>> nfa.is_deterministic()
    False
    """

    def accepts(self, word: Iterable[Hashable]) -> bool:
        """Checks whether the nfa accepts a given word.

        Parameters
        ----------
        word:
            A sequence of input symbols.

        Returns
        -------
        Whether the word is accepted or not.

        Examples
        --------
        >>> nfa = NondeterministicFiniteAutomaton()
        >>> nfa.add_transitions([(0, "a", 1), (0, "a", 2)])
        >>> nfa.add_start_state(0)
        >>> nfa.add_final_state(1)
        >>> nfa.accepts(["a"])
        True
        """
        word = [to_symbol(x) for x in word]
        current_states = self._start_states
        for symbol in word:
            current_states = self._get_next_states_iterable(current_states,
                                                            symbol)
        return any(self.is_final_state(x) for x in current_states)

    def is_deterministic(self) -> bool:
        """Checks whether an automaton is deterministic.

        Returns
        -------
        Whether the automaton is deterministic.

        Examples
        --------
        >>> nfa = NondeterministicFiniteAutomaton()
        >>> nfa.add_transitions([(0, "a", 1), (0, "a", 2)])
        >>> nfa.add_start_state(0)
        >>> nfa.add_final_state(1)
        >>> nfa.is_deterministic()
        False
        """
        return len(self._start_states) <= 1 and \
            self._transition_function.is_deterministic()

    def add_transition(self,
                       s_from: Hashable,
                       symb_by: Hashable,
                       s_to: Hashable) -> int:
        """Adds the given transition to the NFA.

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
        Always 1.

        Raises
        ------
        InvalidEpsilonTransitionError
            When trying to add an epsilon transition.
        """
        symb_by = to_symbol(symb_by)
        if symb_by == Epsilon():
            raise InvalidEpsilonTransitionError
        return super().add_transition(s_from, symb_by, s_to)

    def copy(self) -> "NondeterministicFiniteAutomaton":
        """Copies the current NFA.

        Returns
        -------
        The copy of current finite automaton.
        """
        return self._copy_to(NondeterministicFiniteAutomaton())

    @classmethod
    def from_epsilon_nfa(cls, enfa: EpsilonNFA) \
            -> "NondeterministicFiniteAutomaton":
        """Builds NFA equivalent to the given Epsilon NFA.

        Parameters
        ----------
        enfa:
            A nondeterministic finite automaton with epsilon transitions.

        Returns
        -------
        An equivalent automaton without epsilon transitions.
        """
        nfa = NondeterministicFiniteAutomaton()
        for state in enfa.start_states:
            nfa.add_start_state(state)
        for state in enfa.final_states:
            nfa.add_final_state(state)
        start_eclose = enfa.eclose_iterable(enfa.start_states)
        for state in start_eclose:
            nfa.add_start_state(state)
        for state in enfa.states:
            eclose = enfa.eclose(state)
            for e_state in eclose:
                if e_state in enfa.final_states:
                    nfa.add_final_state(state)
                for symb in enfa.symbols:
                    for next_state in enfa(e_state, symb):
                        nfa.add_transition(state, symb, next_state)
        return nfa


class InvalidEpsilonTransitionError(Exception):
    """An exception signaling of invalid epsilon transition.

    Raised when an epsilon transition is created in non-epsilon NFA.
    """
