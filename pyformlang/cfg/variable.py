""" A variable in a CFG """
import string

from typing import Optional, Any

from .cfg_object import CFGObject


class Variable(CFGObject):  # pylint: disable=too-few-public-methods
    """ An variable in a CFG

    Parameters
    -----------
    value : any
        The value of the variable
    """

    def __init__(self, value: Any) -> None:
        super().__init__(value)
        self._hash = None
        self.index_cfg_converter: Optional[int] = None

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CFGObject):
            return self._value == other.value
        return self._value == other

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return "Variable(" + str(self.value) + ")"

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = self._compute_new_hash()
        return self._hash

    def _compute_new_hash(self) -> int:
        return hash(self._value)

    def to_text(self) -> str:
        text = str(self._value)
        if text and text[0] not in string.ascii_uppercase:
            return '"VAR:' + text + '"'
        return text
