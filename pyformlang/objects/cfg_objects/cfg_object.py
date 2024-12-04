""" An object in a CFG (Variable and Terminal)"""

from abc import abstractmethod

from .cfg_convertible import CFGConvertible
from ..formal_object import FormalObject


class CFGObject(CFGConvertible, FormalObject):
    """ An object in a CFG

    Parameters
    -----------
    value : any
        The value of the object
    """

    @abstractmethod
    def to_text(self) -> str:
        """ Turns the object into a text format """
        raise NotImplementedError
