""" Utility for finite automaton object creation """

from typing import Hashable

from .state import State
from .symbol import Symbol
from .epsilon import Epsilon


def to_state(given: Hashable) -> State:
    """ Transforms the input into a state

    Parameters
    ----------
    given : any
        What we want to transform
    """
    if isinstance(given, State):
        return given
    return State(given)


def to_symbol(given: Hashable) -> Symbol:
    """ Transforms the input into a symbol

    Parameters
    ----------
    given : any
        What we want to transform
    """
    if isinstance(given, Symbol):
        return given
    if given in ("epsilon", "ɛ"):
        return Epsilon()
    return Symbol(given)
