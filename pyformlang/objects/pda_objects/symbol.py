"""A Symbol in a push-down automaton."""

from .pda_object import PDAObject
from ..base_terminal import BaseTerminal


class Symbol(BaseTerminal, PDAObject):
    """A Symbol in a push-down automaton.

    Parameters
    ----------
    value:
        The value of the symbol.
    """

    def __repr__(self) -> str:
        """Gets a string representation of the symbol."""
        return f"Symbol({self})"
