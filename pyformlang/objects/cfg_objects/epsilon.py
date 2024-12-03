""" An epsilon terminal """

from typing import Any

from .terminal import Terminal
from ..finite_automaton_objects.epsilon import EPSILON_SYMBOLS


class Epsilon(Terminal):
    """ An epsilon terminal """

    def __init__(self) -> None:
        super().__init__("epsilon")

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Epsilon) or other in EPSILON_SYMBOLS

    def __hash__(self) -> int:
        return super().__hash__()

    def to_text(self) -> str:
        return "epsilon"
