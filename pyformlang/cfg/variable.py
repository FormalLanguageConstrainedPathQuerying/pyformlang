""" A variable in a CFG """
import string

from typing import Optional, Hashable

from .cfg_object import CFGObject


class Variable(CFGObject):  # pylint: disable=too-few-public-methods
    """ An variable in a CFG

    Parameters
    -----------
    value : any
        The value of the variable
    """

    def __init__(self, value: Hashable) -> None:
        super().__init__(value)
        self.index_cfg_converter: Optional[int] = None

    def __repr__(self) -> str:
        return "Variable(" + str(self.value) + ")"

    def to_text(self) -> str:
        text = str(self._value)
        if text and text[0] not in string.ascii_uppercase:
            return '"VAR:' + text + '"'
        return text
