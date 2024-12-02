"""
Represents an epsilon transition
"""

from typing import Any

from .symbol import Symbol


class Epsilon(Symbol):
    """ An epsilon transition

    Examples
    --------

    >>> epsilon = Epsilon()

    """

    def __init__(self) -> None:
        super().__init__("epsilon")

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Epsilon)

    def __hash__(self) -> int:
        return hash("EPSILON TRANSITION")
