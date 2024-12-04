"""
Represents an epsilon transition
"""

from .symbol import Symbol
from ..base_epsilon import BaseEpsilon


class Epsilon(BaseEpsilon, Symbol):
    """ An epsilon transition

    Examples
    --------

    >>> epsilon = Epsilon()

    """
