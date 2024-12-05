"""
Representation of a state in a finite state automaton
"""

from typing import Any

from .finite_automaton_object import FiniteAutomatonObject
from ..cfg_objects import CFGObjectConvertible
from ..formal_object import FormalObject


class State(CFGObjectConvertible, FiniteAutomatonObject):
    """ A state in a finite automaton

    Parameters
    ----------
    value : any
        The value of the state

    Examples
    ----------
    >>> from pyformlang.finite_automaton import State
    >>> State("A")
    A

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
