""" Basic PDA object representation """

from abc import abstractmethod

from typing import Hashable, Any


class PDAObject:
    """ Basic PDA object representation """

    def __init__(self, value: Hashable) -> None:
        self._value = value
        self._hash = None

    @property
    def value(self) -> Hashable:
        """ Returns the value of the object """
        return self._value

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self._value)
        return self._hash

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError
