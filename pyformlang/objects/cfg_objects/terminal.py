""" A terminal in a CFG """

from .cfg_object import CFGObject


class Terminal(CFGObject):  # pylint: disable=too-few-public-methods
    """ A terminal in a CFG """

    def __repr__(self) -> str:
        return "Terminal(" + str(self.value) + ")"

    def to_text(self) -> str:
        text = str(self._value)
        if text and text[0].isupper():
            return '"TER:' + text + '"'
        return text
