""" An epsilon terminal """

from typing import Any

from .terminal import Terminal


class Epsilon(Terminal):
    """ An epsilon terminal """
    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        super().__init__("epsilon")

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Epsilon)

    def __hash__(self) -> int:
        return super().__hash__()

    def to_text(self) -> str:
        return "epsilon"
