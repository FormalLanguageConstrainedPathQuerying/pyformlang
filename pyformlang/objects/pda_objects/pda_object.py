"""Basic PDA object representation."""

from abc import abstractmethod

from ..formal_object import FormalObject


class PDAObject(FormalObject):
    """Basic PDA object representation.

    Parameters
    ----------
    value:
        The value of the object.
    """

    @abstractmethod
    def __repr__(self) -> str:
        """Gets a string representation of the object."""
        raise NotImplementedError
