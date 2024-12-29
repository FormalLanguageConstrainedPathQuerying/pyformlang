""" A variable in a CFG """

from string import ascii_uppercase

from .cfg_object import CFGObject
from ..formal_object import FormalObject


class Variable(CFGObject):
    """ An variable in a CFG

    Parameters
    -----------
    value : any
        The value of the variable
    """

    def __repr__(self) -> str:
        return f"Variable({self})"

    def to_text(self) -> str:
        text = str(self._value)
        if text and text[0] not in ascii_uppercase:
            return '"VAR:' + text + '"'
        return text

    def _is_equal_to(self, other: FormalObject) -> bool:
        return isinstance(other, Variable) and self.value == other.value
