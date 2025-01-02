"""A state in a finite automaton."""

from .finite_automaton_object import FiniteAutomatonObject
from ..formal_object import FormalObject


class State(FiniteAutomatonObject):
    """A state in a finite automaton.

    Parameters
    ----------
    value:
        The value of the state.

    Examples
    --------
    >>> from pyformlang.finite_automaton import State
    >>> State("A")
    A
    """

    def __repr__(self) -> str:
        """Gets a string representation of the state."""
        return f"State({self})"

    def _is_equal_to(self, other: FormalObject) -> bool:
        return isinstance(other, State) and self.value == other.value
