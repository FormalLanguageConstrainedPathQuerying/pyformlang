""" General epsilon representation """

from typing import Any

from .formal_object import FormalObject
from .base_terminal import BaseTerminal

EPSILON_SYMBOLS = ["epsilon", "ɛ"]


class BaseEpsilon(BaseTerminal):
    """ An epsilon transition

    Examples
    --------

    >>> epsilon = Epsilon()

    """

    def __init__(self) -> None:
        super().__init__("epsilon")

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BaseEpsilon) \
            or not isinstance(other, FormalObject) and other in EPSILON_SYMBOLS

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        return "epsilon"
