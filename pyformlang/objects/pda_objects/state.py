"""A State in a push-down automaton."""

from .pda_object import PDAObject
from ..formal_object import FormalObject


class State(PDAObject):
    """A State in a push-down automaton.

    Parameters
    ----------
    value:
        The value of the state.
    """

    def __repr__(self) -> str:
        """Gets a string representation of the state."""
        return f"State({self})"

    def _is_equal_to(self, other: FormalObject) -> bool:
        return isinstance(other, State) and self.value == other.value
