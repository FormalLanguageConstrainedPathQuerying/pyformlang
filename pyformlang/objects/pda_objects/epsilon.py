""" An epsilon symbol """

from typing import Any

from .stack_symbol import StackSymbol


class Epsilon(StackSymbol):
    """ An epsilon symbol """

    def __init__(self) -> None:
        super().__init__("epsilon")

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Epsilon)

    def __hash__(self) -> int:
        return super().__hash__()
