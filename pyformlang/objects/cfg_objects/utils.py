"""Utility for CFG object creation."""

from typing import Hashable

from .variable import Variable
from .terminal import Terminal
from .epsilon import Epsilon


def to_variable(given: Hashable) -> Variable:
    """Transforms the given object into a variable."""
    if isinstance(given, Variable):
        return given
    return Variable(given)


def to_terminal(given: Hashable) -> Terminal:
    """Transforms the given object into a terminal."""
    if given == Epsilon():
        return Epsilon()
    if isinstance(given, Terminal):
        return given
    return Terminal(given)
