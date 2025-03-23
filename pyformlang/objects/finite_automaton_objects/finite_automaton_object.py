"""
Represents an object of a finite state automaton
"""

from abc import abstractmethod

from ..formal_object import FormalObject


class FiniteAutomatonObject(FormalObject):
    """ Represents an object in a finite state automaton

    Parameters
    ----------
    value: any
        The value of the object
    """

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError
