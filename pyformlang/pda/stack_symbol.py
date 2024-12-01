""" A StackSymbol in a pushdown automaton """

from typing import Optional, Hashable, Any

from .symbol import Symbol

class StackSymbol(Symbol):
    """ A StackSymbol in a pushdown automaton

    Parameters
    ----------
    value : any
        The value of the state

    """

    def __init__(self, value: Hashable) -> None:
        super().__init__(value)
        self.index_cfg_converter: Optional[int] = None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, StackSymbol):
            return False
        return self._value == other.value

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        return "StackSymbol(" + str(self._value) + ")"
