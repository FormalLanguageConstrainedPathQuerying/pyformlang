"""Utility for finite automaton object creation."""

from typing import Hashable

from .state import State
from .symbol import Symbol
from .epsilon import Epsilon


def to_state(given: Hashable) -> State:
    """Transforms the given object into a state.

    Parameters
    ----------
    given:
        What we want to transform.
    """
    if isinstance(given, State):
        return given
    return State(given)


def to_symbol(given: Hashable) -> Symbol:
    """Transforms the given object into a symbol.

    Parameters
    ----------
    given:
        What we want to transform.
    """
    if given == Epsilon():
        return Epsilon()
    if isinstance(given, Symbol):
        return given
    return Symbol(given)
