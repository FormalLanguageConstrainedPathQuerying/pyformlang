""" Basic PDA object representation """

from abc import abstractmethod

from ..formal_object import FormalObject


class PDAObject(FormalObject):
    """ Basic PDA object representation """

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError
