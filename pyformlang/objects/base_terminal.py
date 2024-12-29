""" General terminal representation """

from typing import Any
from abc import abstractmethod

from .formal_object import FormalObject


class BaseTerminal(FormalObject):
    """ General terminal representation """

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BaseTerminal):
            return self.value == other.value
        if isinstance(other, FormalObject):
            return False
        return self.value == other

    def __hash__(self) -> int:
        return super().__hash__()

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError
