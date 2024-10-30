""" Basic PDA object representation """

from typing import Any


class PDAObject:
    """ Basic PDA object representation """

    def __init__(self, value: Any) -> None:
        self._value = value
        self._hash = None

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self._value)
        return self._hash

    @property
    def value(self) -> Any:
        """ Returns the value of the object """
        return self._value

    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
