"""Creation of objects for PDA"""

from typing import Dict, Iterable, Optional

from pyformlang.pda import Epsilon as PDAEpsilon, Symbol, StackSymbol

from .cfg_object import CFGObject
from .variable import Variable
from .terminal import Terminal
from .epsilon import Epsilon as CFGEpsilon


class PDAObjectCreator:
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
