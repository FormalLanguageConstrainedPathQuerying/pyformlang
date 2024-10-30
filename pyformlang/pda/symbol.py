""" A Symbol in a pushdown automaton """

from typing import Any

from .pda_object import PDAObject


class Symbol(PDAObject):
    """ A Symbol in a pushdown automaton

    Parameters
    ----------
    value : any
        The value of the state

    """

    def __hash__(self) -> int:
        return super().__hash__()

    @property
    def value(self) -> Any:
        """ Returns the value of the symbol

        Returns
        ----------
        value: The value
            any
        """
        return self._value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Symbol):
            return self._value == other.value
        return False

    def __repr__(self) -> str:
        return "Symbol(" + str(self._value) + ")"
