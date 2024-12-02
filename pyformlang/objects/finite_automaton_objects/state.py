"""
Representation of a state in a finite state automaton
"""

from typing import Any

from .finite_automaton_object import FiniteAutomatonObject
from ..cfg_objects import CFGConvertible


class State(CFGConvertible, FiniteAutomatonObject):
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
        return self.value == other

    def __hash__(self) -> int:
        return super().__hash__()
