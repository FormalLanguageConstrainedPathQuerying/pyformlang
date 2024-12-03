""" Utility for pda object creation """

from typing import Hashable

from .state import State
from .symbol import Symbol
from .stack_symbol import StackSymbol
from .epsilon import Epsilon, EPSILON_SYMBOLS


def to_state(given: Hashable) -> State:
    """ Convert to a state """
    if isinstance(given, State):
        return given
    return State(given)


def to_symbol(given: Hashable) -> Symbol:
    """ Convert to a symbol """
    if isinstance(given, Symbol):
        return given
    if given in EPSILON_SYMBOLS:
        return Epsilon()
    return Symbol(given)


def to_stack_symbol(given: Hashable) -> StackSymbol:
    """ Convert to a stack symbol """
    if isinstance(given, StackSymbol):
        return given
    if given in EPSILON_SYMBOLS:
        return Epsilon()
    return StackSymbol(given)
