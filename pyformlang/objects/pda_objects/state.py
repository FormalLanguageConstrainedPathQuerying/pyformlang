""" A State in a pushdown automaton """

from .pda_object import PDAObject
from ..formal_object import FormalObject


class State(PDAObject):
    """ A State in a pushdown automaton

    Parameters
    ----------
    value : any
        The value of the state

    """

    def __repr__(self) -> str:
        return f"State({self})"

    def _is_equal_to(self, other: FormalObject) -> bool:
        return isinstance(other, State) and self.value == other.value
