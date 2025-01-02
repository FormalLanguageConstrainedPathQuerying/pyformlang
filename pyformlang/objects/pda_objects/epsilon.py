"""An epsilon symbol in push-down automaton."""

from .stack_symbol import StackSymbol
from ..base_epsilon import BaseEpsilon


class Epsilon(BaseEpsilon, StackSymbol):
    """An epsilon symbol in push-down automaton."""
