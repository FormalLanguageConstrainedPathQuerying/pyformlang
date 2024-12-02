""" Useful functions for a PDA """

from typing import Dict, Iterable, Optional, Hashable

from pyformlang.cfg import CFGObject, Variable, Terminal, Epsilon as CFGEpsilon

from .state import State
from .symbol import Symbol
from .stack_symbol import StackSymbol
from .epsilon import Epsilon as PDAEpsilon


class PDAObjectConverter:
    """Creates Objects for a PDA"""

    def __init__(self,
                 terminals: Iterable[Terminal],
                 variables: Iterable[Variable]) -> None:
        self._inverse_symbol: Dict[CFGObject, Optional[Symbol]] = {}
        self._inverse_stack_symbol: Dict[CFGObject, Optional[StackSymbol]] = {}
        for terminal in terminals:
            self._inverse_symbol[terminal] = None
            self._inverse_stack_symbol[terminal] = None
        for variable in variables:
            self._inverse_stack_symbol[variable] = None

    def get_symbol_from(self, symbol: CFGObject) -> Symbol:
        """Get a symbol"""
        if isinstance(symbol, CFGEpsilon):
            return PDAEpsilon()
        inverse_symbol = self._inverse_symbol[symbol]
        if inverse_symbol is None:
            value = str(symbol.value)
            temp = Symbol(value)
            self._inverse_symbol[symbol] = temp
            return temp
        return inverse_symbol

    def get_stack_symbol_from(self, stack_symbol: CFGObject) \
            -> StackSymbol:
        """Get a stack symbol"""
        if isinstance(stack_symbol, CFGEpsilon):
            return PDAEpsilon()
        inverse_stack_symbol = self._inverse_stack_symbol[stack_symbol]
        if inverse_stack_symbol is None:
            value = str(stack_symbol.value)
            if isinstance(stack_symbol, Terminal):
                value = "#TERM#" + value
            temp = StackSymbol(value)
            self._inverse_stack_symbol[stack_symbol] = temp
            return temp
        return inverse_stack_symbol


def to_state(given: Hashable) -> State:
    """ Convert to a state """
    if isinstance(given, State):
        return given
    return State(given)


def to_symbol(given: Hashable) -> Symbol:
    """ Convert to a symbol """
    if isinstance(given, Symbol):
        return given
    if given == "epsilon":
        return PDAEpsilon()
    return Symbol(given)


def to_stack_symbol(given: Hashable) -> StackSymbol:
    """ Convert to a stack symbol """
    if isinstance(given, StackSymbol):
        return given
    if given == "epsilon":
        return PDAEpsilon()
    return StackSymbol(given)
