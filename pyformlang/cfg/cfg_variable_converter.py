"""A converter into CFG variables."""

from typing import Dict, List, AbstractSet, Tuple, Optional, Hashable

from ..objects.formal_object import FormalObject
from ..objects.cfg_objects import Variable


class CFGVariableConverter:
    """A converter into CFG variables."""

    def __init__(self,
                 states: AbstractSet[FormalObject],
                 stack_symbols: AbstractSet[FormalObject]) -> None:
        """Initializes the converter."""
        self._counter = 0
        self._inverse_states_d: Dict[FormalObject, int] = {}
        self._counter_state = 0
        for self._counter_state, state in enumerate(states):
            self._inverse_states_d[state] = self._counter_state
            state.index = self._counter_state
        self._counter_state += 1
        self._inverse_stack_symbol_d: Dict[FormalObject, int] = {}
        self._counter_symbol = 0
        for self._counter_symbol, symbol in enumerate(stack_symbols):
            self._inverse_stack_symbol_d[symbol] = self._counter_symbol
            symbol.index = self._counter_symbol
        self._counter_symbol += 1
        self._conversions: List[List[List[Tuple[bool, Optional[Variable]]]]] \
            = [[[(False, None) for _ in range(len(states))]
                for _ in range(len(stack_symbols))] for _ in
               range(len(states))]

    def _get_state_index(self, state: FormalObject) -> int:
        """Gets the state index."""
        if state.index is None:
            if state not in self._inverse_states_d:
                self._inverse_states_d[state] = self._counter_state
                self._counter_state += 1
            state.index = self._inverse_states_d[state]
        return state.index

    def _get_symbol_index(self, symbol: FormalObject) -> int:
        """Gets the symbol index."""
        if symbol.index is None:
            if symbol not in self._inverse_stack_symbol_d:
                self._inverse_stack_symbol_d[symbol] = self._counter_symbol
                self._counter_symbol += 1
            symbol.index = self._inverse_stack_symbol_d[symbol]
        return symbol.index

    def to_cfg_combined_variable(self,
                                 state0: FormalObject,
                                 stack_symbol: FormalObject,
                                 state1: FormalObject) -> Variable:
        """Conversion used in the PDA to CFG transformation."""
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
                  state0: FormalObject,
                  stack_symbol: FormalObject,
                  state1: FormalObject) -> None:
        """Set valid."""
        i_stack_symbol, i_state0, i_state1 = self._get_indexes(
            stack_symbol, state0, state1)
        prev = self._conversions[i_state0][i_stack_symbol][i_state1]
        self._conversions[i_state0][i_stack_symbol][i_state1] = (True, prev[1])

    def is_valid_and_get(self,
                         state0: FormalObject,
                         stack_symbol: FormalObject,
                         state1: FormalObject) -> Optional[Variable]:
        """Check if valid and get."""
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
                     stack_symbol: FormalObject,
                     state0: FormalObject,
                     state1: FormalObject) \
            -> Tuple[int, int, int]:
        i_state0 = self._get_state_index(state0)
        i_stack_symbol = self._get_symbol_index(stack_symbol)
        i_state1 = self._get_state_index(state1)
        return i_stack_symbol, i_state0, i_state1
