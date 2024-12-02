""" A State in a pushdown automaton """

from typing import Any

from .pda_object import PDAObject
from ..cfg_objects import CFGConvertible


class State(PDAObject, CFGConvertible):
    """ A State in a pushdown automaton

    Parameters
    ----------
    value : any
        The value of the state

    """

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, State):
            return False
        return self._value == other.value

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        return "State(" + str(self._value) + ")"
