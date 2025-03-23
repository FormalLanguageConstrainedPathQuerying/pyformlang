"""An epsilon symbol in finite automaton."""

from .symbol import Symbol
from ..base_epsilon import BaseEpsilon


class Epsilon(BaseEpsilon, Symbol):
    """An epsilon symbol in finite automaton.

    Examples
    --------
    >>> epsilon = Epsilon()
    """
