"""General terminal representation."""

from abc import abstractmethod

from .formal_object import FormalObject


class BaseTerminal(FormalObject):
    """General terminal representation."""

    @abstractmethod
    def __repr__(self):
        """Gets the string representation of the terminal."""
        raise NotImplementedError

    def _is_equal_to(self, other: FormalObject) -> bool:
        return isinstance(other, BaseTerminal) and self.value == other.value
