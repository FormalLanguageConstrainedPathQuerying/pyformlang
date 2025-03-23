"""
This module describe a symbol in a finite automaton.
"""

from .finite_automaton_object import FiniteAutomatonObject
from ..base_terminal import BaseTerminal


class Symbol(BaseTerminal, FiniteAutomatonObject):
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

    def __repr__(self) -> str:
        return f"Symbol({self})"
