""" A variable in a CFG """

from string import ascii_uppercase

from .cfg_object import CFGObject
from .cfg_convertible import CFGConvertible


class Variable(CFGObject, CFGConvertible):
    """ An variable in a CFG

    Parameters
    -----------
    value : any
        The value of the variable
    """

    def __repr__(self) -> str:
        return "Variable(" + str(self.value) + ")"

    def to_text(self) -> str:
        text = str(self._value)
        if text and text[0] not in ascii_uppercase:
            return '"VAR:' + text + '"'
        return text
