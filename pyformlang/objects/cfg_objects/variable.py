""" A variable in a CFG """

from typing import Any
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

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Variable):
            return self.value == other.value
        if isinstance(other, FormalObject):
            return False
        return self.value == other

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        return f"Variable({self})"

    def to_text(self) -> str:
        text = str(self._value)
        if text and text[0] not in ascii_uppercase:
            return '"VAR:' + text + '"'
        return text
