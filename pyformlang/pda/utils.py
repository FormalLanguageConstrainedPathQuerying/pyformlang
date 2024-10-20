""" Useful functions for a PDA """

from typing import Type, Dict, Any

from .state import State
from .symbol import Symbol
from .stack_symbol import StackSymbol
from .epsilon import Epsilon


class PDAObjectCreator:
    """
    A Object in a PDA
    """

    def __init__(self) -> None:
        self._state_creator: Dict[Any, State] = {}
        self._symbol_creator: Dict[Any, Symbol] = {}
        self._stack_symbol_creator: Dict[Any, StackSymbol] = {}

    def to_state(self, given: Any) -> State:
        """ Convert to a state """
        if isinstance(given, State):
            return _get_object_from_known(given, self._state_creator)
        return _get_object_from_raw(given, self._state_creator, State)

    def to_symbol(self, given: Any) -> Symbol:
        """ Convert to a symbol """
        if isinstance(given, Symbol):
            return _get_object_from_known(given, self._symbol_creator)
        if given == "epsilon":
            return Epsilon()
        return _get_object_from_raw(given, self._symbol_creator, Symbol)

    def to_stack_symbol(self, given: Any) -> StackSymbol:
        """ Convert to a stack symbol """
        if isinstance(given, StackSymbol):
            return _get_object_from_known(given,
                                          self._stack_symbol_creator)
        if isinstance(given, Epsilon):
            return given
        return _get_object_from_raw(given,
                                    self._stack_symbol_creator,
                                    StackSymbol)


def _get_object_from_known(given: Any,
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
