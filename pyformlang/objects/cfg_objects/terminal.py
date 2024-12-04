""" A terminal in a CFG """

from typing import Any

from .cfg_object import CFGObject


class Terminal(CFGObject):
    """ A terminal in a CFG """

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Terminal):
            return self.value == other.value
        if isinstance(other, CFGObject):
            return False
        return self.value == other

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        return "Terminal(" + str(self.value) + ")"

    def to_text(self) -> str:
        text = str(self._value)
        if text and text[0].isupper():
            return '"TER:' + text + '"'
        return text
