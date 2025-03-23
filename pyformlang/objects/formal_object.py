""" General object representation """

from typing import Hashable, Optional, Any
from abc import abstractmethod


class FormalObject:
    """ General object representation """

    def __init__(self, value: Hashable) -> None:
        self._value = value
        self._hash = None
        self.index: Optional[int] = None

    @property
    def value(self) -> Hashable:
        """ Gets the value of the object

        Returns
        ---------
        value : any
            The value of the object
        """
        return self._value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FormalObject):
            return self.value == other
        return self._is_equal_to(other) and other._is_equal_to(self)

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self._value)
        return self._hash

    def __str__(self) -> str:
        return str(self._value)

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def _is_equal_to(self, other: "FormalObject") -> bool:
        raise NotImplementedError
