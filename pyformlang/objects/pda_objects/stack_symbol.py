""" A StackSymbol in a pushdown automaton """

from typing import Any

from .symbol import Symbol
from ..cfg_objects import CFGConvertible
from ..formal_object import FormalObject


class StackSymbol(CFGConvertible, Symbol):
    """ A StackSymbol in a pushdown automaton

    Parameters
    ----------
    value : any
        The value of the state

    """

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, StackSymbol):
            return self.value == other.value
        if isinstance(other, FormalObject):
            return False
        return self.value == other

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        return f"StackSymbol({self})"
