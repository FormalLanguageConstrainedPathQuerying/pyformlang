"""A CFG Variable Converter"""

from typing import Dict, List, AbstractSet, Tuple, Optional, Hashable

from ..objects.cfg_objects import Variable, CFGObjectConvertible


class CFGVariableConverter:
    """A CFG Variable Converter"""

    def __init__(self,
                 states: AbstractSet[CFGObjectConvertible],
                 stack_symbols: AbstractSet[CFGObjectConvertible]) -> None:
        self._counter = 0
        self._inverse_states_d: Dict[CFGObjectConvertible, int] = {}
        self._counter_state = 0
        for self._counter_state, state in enumerate(states):
            self._inverse_states_d[state] = self._counter_state
            state.index_cfg_converter = self._counter_state
        self._counter_state += 1
        self._inverse_stack_symbol_d: Dict[CFGObjectConvertible, int] = {}
        self._counter_symbol = 0
        for self._counter_symbol, symbol in enumerate(stack_symbols):
            self._inverse_stack_symbol_d[symbol] = self._counter_symbol
            symbol.index_cfg_converter = self._counter_symbol
        self._counter_symbol += 1
        self._conversions: List[List[List[Tuple[bool, Optional[Variable]]]]] \
            = [[[(False, None) for _ in range(len(states))]
                for _ in range(len(stack_symbols))] for _ in
               range(len(states))]

    def _get_state_index(self, state: CFGObjectConvertible) -> int:
        """Get the state index"""
        if state.index_cfg_converter is None:
            if state not in self._inverse_states_d:
                self._inverse_states_d[state] = self._counter_state
                self._counter_state += 1
            state.index_cfg_converter = self._inverse_states_d[state]
        return state.index_cfg_converter

    def _get_symbol_index(self, symbol: CFGObjectConvertible) -> int:
        """Get the symbol index"""
        if symbol.index_cfg_converter is None:
            if symbol not in self._inverse_stack_symbol_d:
                self._inverse_stack_symbol_d[symbol] = self._counter_symbol
                self._counter_symbol += 1
            symbol.index_cfg_converter = self._inverse_stack_symbol_d[symbol]
        return symbol.index_cfg_converter

    def to_cfg_combined_variable(self,
                                 state0: CFGObjectConvertible,
                                 stack_symbol: CFGObjectConvertible,
                                 state1: CFGObjectConvertible) -> Variable:
        """ Conversion used in the to_pda method """
        i_stack_symbol, i_state0, i_state1 = self._get_indexes(
            stack_symbol, state0, state1)
        prev = self._conversions[i_state0][i_stack_symbol][i_state1]
        if prev[1] is None:
            return self._create_new_variable(
                i_stack_symbol, i_state0, i_state1, prev)[1]
        return prev[1]

    def _create_new_variable(self,
                             i_stack_symbol: int,
                             i_state0: int,
                             i_state1: int,
                             prev: Tuple,
                             value: Hashable = None) -> Tuple[bool, Variable]:
        if value is None:
            value = self._counter
        temp = (prev[0], Variable(value))
        self._counter += 1
        self._conversions[i_state0][i_stack_symbol][i_state1] = temp
        return temp

    def set_valid(self,
                  state0: CFGObjectConvertible,
                  stack_symbol: CFGObjectConvertible,
                  state1: CFGObjectConvertible) -> None:
        """Set valid"""
        i_stack_symbol, i_state0, i_state1 = self._get_indexes(
            stack_symbol, state0, state1)
        prev = self._conversions[i_state0][i_stack_symbol][i_state1]
        self._conversions[i_state0][i_stack_symbol][i_state1] = (True, prev[1])

    def is_valid_and_get(self,
                         state0: CFGObjectConvertible,
                         stack_symbol: CFGObjectConvertible,
                         state1: CFGObjectConvertible) -> Optional[Variable]:
        """Check if valid and get"""
        i_state0 = self._get_state_index(state0)
        i_stack_symbol = self._get_symbol_index(stack_symbol)
        i_state1 = self._get_state_index(state1)
        current = self._conversions[i_state0][i_stack_symbol][i_state1]
        if not current[0]:
            return None
        if current[1] is None:
            return self._create_new_variable(i_stack_symbol,
                                             i_state0,
                                             i_state1,
                                             current)[1]
        return current[1]

    def _get_indexes(self,
                     stack_symbol: CFGObjectConvertible,
                     state0: CFGObjectConvertible,
                     state1: CFGObjectConvertible) \
            -> Tuple[int, int, int]:
        i_state0 = self._get_state_index(state0)
        i_stack_symbol = self._get_symbol_index(stack_symbol)
        i_state1 = self._get_state_index(state1)
        return i_stack_symbol, i_state0, i_state1
