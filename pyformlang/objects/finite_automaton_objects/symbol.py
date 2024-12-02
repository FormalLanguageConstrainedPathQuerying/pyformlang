"""
This module describe a symbol in a finite automaton.
"""

from typing import Any

from .finite_automaton_object import FiniteAutomatonObject


class Symbol(FiniteAutomatonObject):
    """ A symbol in a finite automaton

    Parameters
    ----------
    value : any
        The value of the symbol

    Examples
    ----------
    >>> from pyformlang.finite_automaton import Symbol
    >>> Symbol("A")
    A
    """

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Symbol):
            return self.value == other.value
        return self.value == other

    def __hash__(self) -> int:
        return super().__hash__()
