""" A StackSymbol in a pushdown automaton """

from .symbol import Symbol
from ..formal_object import FormalObject


class StackSymbol(Symbol):
    """ A StackSymbol in a pushdown automaton

    Parameters
    ----------
    value : any
        The value of the state

    """

    def __repr__(self) -> str:
        return f"StackSymbol({self})"

    def _is_equal_to(self, other: FormalObject) -> bool:
        return isinstance(other, StackSymbol) and self.value == other.value
