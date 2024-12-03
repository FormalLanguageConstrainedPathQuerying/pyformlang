""" An epsilon symbol """

from typing import Any

from .stack_symbol import StackSymbol
from ..finite_automaton_objects.epsilon import EPSILON_SYMBOLS


class Epsilon(StackSymbol):
    """ An epsilon symbol """

    def __init__(self) -> None:
        super().__init__("epsilon")

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Epsilon) or other in EPSILON_SYMBOLS

    def __hash__(self) -> int:
        return super().__hash__()
