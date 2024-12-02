""" Useful functions for a PDA """

from typing import Dict, Set, Iterable, Optional, Hashable
from numpy import empty

from pyformlang.cfg import CFGObject, Variable, Terminal, Epsilon as CFGEpsilon
from pyformlang.finite_automaton import State as FAState

from .state import State as PDAState
from .symbol import Symbol
from .stack_symbol import StackSymbol
from .epsilon import Epsilon as PDAEpsilon


class PDASymbolConverter:
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


class PDAStateConverter:
    """Combines PDA and FA states"""
    # pylint: disable=too-few-public-methods

    def __init__(self,
                 states_pda: Set[PDAState],
                 states_dfa: Set[FAState]) -> None:
        self._inverse_state_pda = {}
        for i, state in enumerate(states_pda):
            self._inverse_state_pda[state] = i
        self._inverse_state_dfa = {}
        for i, state in enumerate(states_dfa):
            self._inverse_state_dfa[state] = i
        self._conversions = empty((len(states_pda), len(states_dfa)),
                                     dtype=PDAState)

    def to_pda_combined_state(self,
                              state_pda: PDAState,
                              state_other: FAState) -> PDAState:
        """ To PDA state in the intersection function """
        i_state_pda = self._inverse_state_pda[state_pda]
        i_state_other = self._inverse_state_dfa[state_other]
        if self._conversions[i_state_pda, i_state_other] is None:
            self._conversions[i_state_pda, i_state_other] = \
                [PDAState((state_pda, state_other))]
        return self._conversions[i_state_pda, i_state_other][0]
