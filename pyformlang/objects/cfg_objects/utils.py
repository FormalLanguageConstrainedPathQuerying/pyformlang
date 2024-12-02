""" Utility for cfg object creation """

from typing import Hashable

from .variable import Variable
from .terminal import Terminal
from .epsilon import Epsilon


def to_variable(given: Hashable) -> Variable:
    """ Transformation into a variable """
    if isinstance(given, Variable):
        return given
    return Variable(given)


def to_terminal(given: Hashable) -> Terminal:
    """ Transformation into a terminal """
    if isinstance(given, Terminal):
        return given
    if given == "epsilon":
        return Epsilon()
    return Terminal(given)