""" General object representation """

from typing import Hashable, Any
from abc import abstractmethod


class FormalObject:
    """ General object representation """

    def __init__(self, value: Hashable) -> None:
        self._value = value
        self._hash = None

    @property
    def value(self) -> Hashable:
        """ Gets the value of the object

        Returns
        ---------
        value : any
            The value of the object
        """
        return self._value

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self._value)
        return self._hash

    def __str__(self) -> str:
        return str(self._value)

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError
