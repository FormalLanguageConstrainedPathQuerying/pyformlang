"""A stack symbol in a push-down automaton."""

from .symbol import Symbol
from ..formal_object import FormalObject


class StackSymbol(Symbol):
    """A stack symbol in a push-down automaton.

    Parameters
    ----------
    value:
        The value of the stack symbol.
    """

    def __repr__(self) -> str:
        """Gets a string representation of the stack symbol."""
        return f"StackSymbol({self})"

    def _is_equal_to(self, other: FormalObject) -> bool:
        return isinstance(other, StackSymbol) and self.value == other.value
