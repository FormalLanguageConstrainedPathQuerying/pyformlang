""" An object in a CFG (Variable and Terminal)"""

from typing import Hashable, Any
from abc import abstractmethod

from .cfg_convertible import CFGConvertible


class CFGObject(CFGConvertible):
    """ An object in a CFG

    Parameters
    -----------
    value : any
        The value of the object
    """

    __slots__ = ["_value", "_hash"]

    def __init__(self, value: Hashable) -> None:
        super().__init__()
        self._value = value
        self._hash = None

    @property
    def value(self) -> Hashable:
        """Gets the value of the object"""
        return self._value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CFGObject):
            return self.value == other.value
        return self.value == other

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self._value)
        return self._hash

    def __str__(self) -> str:
        return str(self._value)

    @abstractmethod
    def to_text(self) -> str:
        """ Turns the object into a text format """
        raise NotImplementedError
