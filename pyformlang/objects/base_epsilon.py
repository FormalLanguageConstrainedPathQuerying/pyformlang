""" General epsilon representation """

from typing import Any

from .formal_object import FormalObject

EPSILON_SYMBOLS = ["epsilon", "ɛ"]


class BaseEpsilon(FormalObject):
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
