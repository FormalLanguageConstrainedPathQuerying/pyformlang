""" An object in a CFG (Variable and Terminal)"""

from abc import abstractmethod

from .cfg_object_convertible import CFGObjectConvertible


class CFGObject(CFGObjectConvertible):
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
