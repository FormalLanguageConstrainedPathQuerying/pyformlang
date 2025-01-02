"""A terminal in a CFG."""

from .cfg_object import CFGObject
from ..base_terminal import BaseTerminal


class Terminal(BaseTerminal, CFGObject):
    """A terminal in a CFG.

    Parameters
    ----------
    value:
        A value of the terminal.
    """

    def __repr__(self) -> str:
        """Gets the string representation of the terminal."""
        return f"Terminal({self})"

    def to_text(self) -> str:
        """Gets a formatted string representing the terminal."""
        text = str(self._value)
        if text and text[0].isupper():
            return '"TER:' + text + '"'
        return text
