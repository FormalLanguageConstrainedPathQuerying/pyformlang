""" A terminal in a CFG """

from .cfg_object import CFGObject
from ..base_terminal import BaseTerminal


class Terminal(BaseTerminal, CFGObject):
    """ A terminal in a CFG """

    def __repr__(self) -> str:
        return f"Terminal({self})"

    def to_text(self) -> str:
        text = str(self._value)
        if text and text[0].isupper():
            return '"TER:' + text + '"'
        return text
