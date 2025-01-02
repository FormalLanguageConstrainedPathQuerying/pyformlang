"""A general transition function representation."""

from typing import Dict, Set, Tuple, Iterable, Iterator
from abc import abstractmethod

from ..objects.finite_automaton_objects import State, Symbol


class TransitionFunction(Iterable[Tuple[State, Symbol, State]]):
    """A general transition function representation."""

    @abstractmethod
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
        """
        raise NotImplementedError

    @abstractmethod
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
        """
        raise NotImplementedError

    @abstractmethod
    def get_number_transitions(self) -> int:
        """Gets the number of transitions described by the function.

        Returns
        -------
        The number of transitions described by the function.
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """Gets the number of transitions described by the function."""
        return self.get_number_transitions()

    @abstractmethod
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
        raise NotImplementedError

    def __contains__(self, transition: Tuple[State, Symbol, State]) -> bool:
        """Checks if the given transition is present in the function.

        Parameters
        ----------
        transition:
            The transition to check containment of.

        Returns
        -------
        Whether the given transition is present in the function.
        """
        s_from, symb_by, s_to = transition
        return s_to in self(s_from, symb_by)

    @abstractmethod
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
        raise NotImplementedError

    def get_next_states_from(self, s_from: State) -> Set[State]:
        """Gets a set of states that are next to the given one.

        Parameters
        ----------
        s_from:
            A state to get next states from.

        Returns
        -------
        A set of next states defined by the transition function.
        """
        next_states = set()
        for _, next_state in self.get_transitions_from(s_from):
            next_states.add(next_state)
        return next_states

    @abstractmethod
    def get_edges(self) -> Iterable[Tuple[State, Symbol, State]]:
        """Gets the edges of graph described by the function.

        Yields
        ------
        The edges as state and symbol tuples.
        """
        raise NotImplementedError

    def __iter__(self) -> Iterator[Tuple[State, Symbol, State]]:
        """Yields the transitions described by the transition function."""
        yield from self.get_edges()

    @abstractmethod
    def to_dict(self) -> Dict[State, Dict[Symbol, Set[State]]]:
        """Get the dictionary representation of the transition function.

        The keys of the dictionary are the source nodes. The items are
        dictionaries where the keys are the symbols of the transitions and
        the items are the set of target nodes.

        Returns
        -------
        The transitions as a dictionary.
        """
        raise NotImplementedError

    @abstractmethod
    def is_deterministic(self) -> bool:
        """Whether the transition function is deterministic.

        Returns
        -------
        Whether the function is deterministic.
        """
        raise NotImplementedError
