""" Useful functions """

from typing import Any

from .variable import Variable
from .terminal import Terminal


def to_variable(given: Any) -> Variable:
    """ Transformation into a variable """
    if isinstance(given, Variable):
        return given
    return Variable(given)


def to_terminal(given: Any) -> Terminal:
    """ Transformation into a terminal """
    if isinstance(given, Terminal):
        return given
    return Terminal(given)
