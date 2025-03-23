"""General formal object representation."""

from typing import Hashable, Optional, Any
from abc import abstractmethod


class FormalObject:
    """General formal object representation.

    Parameters
    ----------
    value:
        A value of the object.
    """

    def __init__(self, value: Hashable) -> None:
        """Initializes the object."""
        self._value = value
        self._hash = None
        self.index: Optional[int] = None

    @property
    def value(self) -> Hashable:
        """Gets the value of the object.

        Returns
        --------
        The value of the object.
        """
        return self._value

    def __eq__(self, other: Any) -> bool:
        """Checks if current formal object is equal to the given object."""
        if not isinstance(other, FormalObject):
            return self.value == other
        return self._is_equal_to(other) and other._is_equal_to(self)

    def __hash__(self) -> int:
        """Gets the hash of current formal object."""
        if self._hash is None:
            self._hash = hash(self._value)
        return self._hash

    def __str__(self) -> str:
        """Gets the string value of the object."""
        return str(self._value)

    @abstractmethod
    def __repr__(self) -> str:
        """Gets the string representation of the object."""
        raise NotImplementedError

    @abstractmethod
    def _is_equal_to(self, other: "FormalObject") -> bool:
        """Checks equality of two formal objects."""
        raise NotImplementedError
