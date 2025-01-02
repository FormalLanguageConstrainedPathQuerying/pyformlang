"""A nondeterministic transition function of finite automaton."""

from typing import Dict, Set, Iterable, Tuple
from copy import deepcopy

from .transition_function import TransitionFunction
from ..objects.finite_automaton_objects import State, Symbol


class NondeterministicTransitionFunction(TransitionFunction):
    """A nondeterministic transition function of finite automaton.

    The difference with a deterministic transition is that the return value is
    a set of States.

    Attributes
    ----------
    _transitions:
        The transition function as a dictionary.

    Examples
    --------
    >>> transition = NondeterministicTransitionFunction()
    >>> transition.add_transition(State(0), Symbol("a"), State(1))

    Creates a transition function and adds a transition.
    """

    def __init__(self) -> None:
        """Creates an empty nondeterministic transition function."""
        self._transitions: Dict[State, Dict[Symbol, Set[State]]] = {}

    def add_transition(self,
                       s_from: State,
                       symb_by: Symbol,
                       s_to: State) -> int:
        """Adds the given transition to the function.

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

        Examples
        --------
        >>> transition = NondeterministicTransitionFunction()
        >>> transition.add_transition(State(0), Symbol("a"), State(1))
        """
        if s_from in self._transitions:
            if symb_by in self._transitions[s_from]:
                self._transitions[s_from][symb_by].add(s_to)
            else:
                self._transitions[s_from][symb_by] = {s_to}
        else:
            self._transitions[s_from] = {}
            self._transitions[s_from][symb_by] = {s_to}
        return 1

    def remove_transition(self,
                          s_from: State,
                          symb_by: Symbol,
                          s_to: State) -> int:
        """Removes the given transition from the function.

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
        1 if the transition was found, 0 otherwise.

        Examples
        --------
        >>> transition = NondeterministicTransitionFunction()
        >>> transition.add_transition(State(0), Symbol("a"), State(1))
        >>> transition.remove_transition(State(0), Symbol("a"), State(1))
        """
        if s_from in self._transitions and \
                symb_by in self._transitions[s_from] and \
                s_to in self._transitions[s_from][symb_by]:
            self._transitions[s_from][symb_by].remove(s_to)
            return 1
        return 0

    def get_number_transitions(self) -> int:
        """Gets the number of transitions described by the function.

        Returns
        -------
        The number of transitions described by the function.

        Examples
        --------
        >>> transition = NondeterministicTransitionFunction()
        >>> transition.add_transition(State(0), Symbol("a"), State(1))
        >>> transition.get_number_transitions()
        1
        """
        counter = 0
        for transitions in self._transitions.values():
            for s_to in transitions.values():
                counter += len(s_to)
        return counter

    def __call__(self, s_from: State, symb_by: Symbol) -> Set[State]:
        """Calls the transition function as a real function.

        Parameters
        ----------
        s_from:
            The source state.
        symb_by:
            The transition symbol.

        Returns
        -------
        A set of destination states.
        """
        if s_from in self._transitions:
            if symb_by in self._transitions[s_from]:
                return self._transitions[s_from][symb_by]
        return set()

    def get_transitions_from(self, s_from: State) \
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
        if s_from in self._transitions:
            for symb_by, states_to in self._transitions[s_from].items():
                for state_to in states_to:
                    yield symb_by, state_to

    def get_edges(self) -> Iterable[Tuple[State, Symbol, State]]:
        """Gets the edges of graph described by the function.

        Yields
        ------
        The edges as state and symbol tuples.
        """
        for s_from in self._transitions:
            for symb_by, s_to in self.get_transitions_from(s_from):
                yield s_from, symb_by, s_to

    def to_dict(self) -> Dict[State, Dict[Symbol, Set[State]]]:
        """Get the dictionary representation of the transition function.

        The keys of the dictionary are the source nodes. The items are
        dictionaries where the keys are the symbols of the transitions and
        the items are the set of target nodes.

        Returns
        -------
        The transitions as a dictionary.
        """
        return deepcopy(self._transitions)

    def is_deterministic(self) -> bool:
        """Whether the transition function is deterministic.

        Returns
        -------
        Whether the function is deterministic.

        Examples
        --------
        >>> transition = NondeterministicTransitionFunction()
        >>> transition.add_transition(State(0), Symbol("a"), State(1))
        >>> transition.is_deterministic()
        True
        """
        for transitions in self._transitions.values():
            for s_to in transitions.values():
                if len(s_to) > 1:
                    return False
        return True
