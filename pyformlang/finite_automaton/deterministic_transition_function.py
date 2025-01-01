"""A deterministic transition function."""

from typing import Optional

from .nondeterministic_transition_function import \
    NondeterministicTransitionFunction
from .nondeterministic_finite_automaton import InvalidEpsilonTransitionError
from ..objects.finite_automaton_objects import State, Symbol, Epsilon


class DeterministicTransitionFunction(NondeterministicTransitionFunction):
    """A deterministic transition function in a finite automaton.

    Attributes
    ----------
    _transitions:
        A dictionary which contains the transitions of a finite automaton.

    Examples
    --------
    >>> transition = TransitionFunction()
    >>> transition.add_transition(State(0), Symbol("a"), State(1))

    Creates a transition function and adds a transition.
    """

    def add_transition(self,
                       s_from: State,
                       symb_by: Symbol,
                       s_to: State) -> int:
        """Adds a new transition to the function.

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
        DuplicateTransitionError
            If the transition already exists.

        Examples
        --------
        >>> transition = TransitionFunction()
        >>> transition.add_transition(State(0), Symbol("a"), State(1))
        """
        if symb_by == Epsilon():
            raise InvalidEpsilonTransitionError()
        s_to_old = self.get_next_state(s_from, symb_by)
        if s_to_old is not None and s_to_old != s_to:
            raise DuplicateTransitionError(s_from,
                                           symb_by,
                                           s_to,
                                           s_to_old)
        return super().add_transition(s_from, symb_by, s_to)

    def get_next_state(self, s_from: State, symb_by: Symbol) -> Optional[State]:
        """Makes a call of deterministic transition function.

        Parameters
        ----------
        s_from:
            A state to make a transition from.
        symb_by:
            A symbol to make a transition with.

        Returns
        -------
        The next state defined by the transition function.
        """
        next_state = self(s_from, symb_by)
        return list(next_state)[0] if next_state else None

    def is_deterministic(self) -> bool:
        """Checks whether the transition function is deterministic.

        Returns
        -------
        Whether the transition function is deterministic.
        """
        return True


class DuplicateTransitionError(Exception):
    """Signals of a duplicated transition.

    Parameters
    ----------
    s_from:
        The source state.
    symb_by:
        The transition symbol.
    s_to:
        The wanted new destination state.
    s_to_old:
        The old destination state.
    """

    def __init__(self,
                 s_from: State,
                 symb_by: Symbol,
                 s_to: State,
                 s_to_old: State) -> None:
        """Creates an instance of duplicate transition exception."""
        super().__init__("Transition from " + str(s_from) +
                         " by " + str(symb_by) +
                         " goes to " + str(s_to_old) + " not " + str(s_to))
        self.s_from = s_from
        self.symb_by = symb_by
        self.s_to = s_to
        self.s_to_old = s_to_old
