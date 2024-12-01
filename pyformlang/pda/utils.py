""" Useful functions for a PDA """

from typing import Type, Dict, Hashable, Any

from .pda_object import PDAObject
from .state import State
from .symbol import Symbol
from .stack_symbol import StackSymbol
from .epsilon import Epsilon


class PDAObjectCreator:
    """
    A Object in a PDA
    """

    def __init__(self) -> None:
        self._state_creator: Dict[Hashable, State] = {}
        self._symbol_creator: Dict[Hashable, Symbol] = {}
        self._stack_symbol_creator: Dict[Hashable, StackSymbol] = {}

    def to_state(self, given: Hashable) -> State:
        """ Convert to a state """
        if isinstance(given, State):
            return _get_object_from_known(given, self._state_creator)
        return _get_object_from_raw(given, self._state_creator, State)

    def to_symbol(self, given: Hashable) -> Symbol:
        """ Convert to a symbol """
        if isinstance(given, Symbol):
            return _get_object_from_known(given, self._symbol_creator)
        if given == "epsilon":
            return Epsilon()
        return _get_object_from_raw(given, self._symbol_creator, Symbol)

    def to_stack_symbol(self, given: Hashable) -> StackSymbol:
        """ Convert to a stack symbol """
        if isinstance(given, StackSymbol):
            return _get_object_from_known(given,
                                          self._stack_symbol_creator)
        if isinstance(given, Epsilon):
            return given
        return _get_object_from_raw(given,
                                    self._stack_symbol_creator,
                                    StackSymbol)


def _get_object_from_known(given: PDAObject,
                           obj_converter: Dict[Any, Any]) -> Any:
    if given.value in obj_converter:
        return obj_converter[given.value]
    obj_converter[given.value] = given
    return given


def _get_object_from_raw(given: Any,
                         obj_converter: Dict[Any, Any],
                         to_type: Type) -> Any:
    if given in obj_converter:
        return obj_converter[given]
    temp = to_type(given)
    obj_converter[given] = temp
    return temp
