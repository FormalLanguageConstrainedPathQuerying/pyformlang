"""General epsilon representation."""

from typing import Any

from .formal_object import FormalObject
from .base_terminal import BaseTerminal

EPSILON_SYMBOLS = ["epsilon", "ɛ"]


class BaseEpsilon(BaseTerminal):
    """An epsilon transition.

    Examples
    --------
    >>> epsilon = Epsilon()
    """

    def __init__(self) -> None:
        """Initializes the epsilon terminal."""
        super().__init__("epsilon")

    def __eq__(self, other: Any) -> bool:
        """Check if the epsilon is equal to the given object."""
        return isinstance(other, BaseEpsilon) \
            or not isinstance(other, FormalObject) and other in EPSILON_SYMBOLS

    def __hash__(self) -> int:
        """Gets the hash of the epsilon symbol."""
        return super().__hash__()

    def __repr__(self) -> str:
        """Gets the string representation of the epsilon symbol."""
        return "epsilon"

    def _is_equal_to(self, other: FormalObject) -> bool:
        return isinstance(other, BaseEpsilon)
