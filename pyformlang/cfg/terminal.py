""" A terminal in a CFG """

from typing import Any

from .cfg_object import CFGObject


class Terminal(CFGObject):  # pylint: disable=too-few-public-methods
    """ A terminal in a CFG """

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CFGObject):
            return self.value == other.value
        return self.value == other

    def __repr__(self) -> str:
        return "Terminal(" + str(self.value) + ")"

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.value)
        return self._hash

    def to_text(self) -> str:
        text = str(self._value)
        if text and text[0].isupper():
            return '"TER:' + text + '"'
        return text
