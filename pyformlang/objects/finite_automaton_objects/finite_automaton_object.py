"""Representation of an object of a finite state automaton."""

from abc import abstractmethod

from ..formal_object import FormalObject


class FiniteAutomatonObject(FormalObject):
    """Representation of an object of a finite state automaton.

    Parameters
    ----------
    value:
        The value of the object.
    """

    @abstractmethod
    def __repr__(self) -> str:
        """Gets a string representation of the object."""
        raise NotImplementedError
