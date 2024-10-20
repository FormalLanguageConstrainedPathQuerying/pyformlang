""" A State in a pushdown automaton """

from typing import Optional, Any

from .pda_object import PDAObject


class State(PDAObject):
    """ A State in a pushdown automaton

    Parameters
    ----------
    value : any
        The value of the state

    """

    def __init__(self, value: Any) -> None:
        super().__init__(value)
        self.index_cfg_converter: Optional[int] = None

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
        if isinstance(other, State):
            return self._value == other.value
        return False

    def __repr__(self) -> str:
        return "State(" + str(self._value) + ")"
