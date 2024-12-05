""" A State in a pushdown automaton """

from typing import Any

from .pda_object import PDAObject
from ..cfg_objects import CFGObjectConvertible
from ..formal_object import FormalObject


class State(CFGObjectConvertible, PDAObject):
    """ A State in a pushdown automaton

    Parameters
    ----------
    value : any
        The value of the state

    """

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, State):
            return self.value == other.value
        if isinstance(other, FormalObject):
            return False
        return self.value == other

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        return f"State({self})"
