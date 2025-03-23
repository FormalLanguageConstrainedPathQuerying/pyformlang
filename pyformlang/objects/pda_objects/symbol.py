""" A Symbol in a pushdown automaton """

from .pda_object import PDAObject
from ..base_terminal import BaseTerminal


class Symbol(BaseTerminal, PDAObject):
    """ A Symbol in a pushdown automaton

    Parameters
    ----------
    value : any
        The value of the state

    """

    def __repr__(self) -> str:
        return f"Symbol({self})"
