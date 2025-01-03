"""Representation of an end rule.

A rule which gives only a terminal.
"""

from typing import List, Set, Hashable, Any

from pyformlang.cfg import CFGObject, Variable, Terminal

from .reduced_rule import ReducedRule
from ..objects.cfg_objects.utils import to_variable, to_terminal


class EndRule(ReducedRule):
    """Representation of an end rule.

    It is a rule of form:
        A[sigma] -> a

    Parameters
    -----------
    left_term:
        The non-terminal on the left, "A" here.
    right_term:
        The terminal on the right, "a" here.
    """

    def __init__(self, left_term: Hashable, right_term: Hashable) -> None:
        """Initializes the end rule."""
        self._left_term = to_variable(left_term)
        self._right_term = to_terminal(right_term)

    @property
    def f_parameter(self) -> Terminal:
        """Gets the symbol consumed by the rule."""
        raise NotImplementedError

    @property
    def production(self) -> Terminal:
        """Gets the symbol produced by the rule."""
        raise NotImplementedError

    @property
    def left_term(self) -> Variable:
        """Gets a nonterminal on the left of the rule."""
        return self._left_term

    @property
    def right_term(self) -> Terminal:
        """Gets a terminal on the right of the rule."""
        return self._right_term

    @property
    def right_terms(self) -> List[CFGObject]:
        """Gets a list of right terms of the rule."""
        return [self._right_term]

    @property
    def non_terminals(self) -> Set[Variable]:
        """Gets the nonterminals used in the rule."""
        return {self._left_term}

    @property
    def terminals(self) -> Set[Terminal]:
        """Gets the terminals used in the rule."""
        return {self._right_term}

    def __eq__(self, other: Any) -> bool:
        """Checks if the rule is equal to the given object."""
        if not isinstance(other, EndRule):
            return False
        return other.left_term == self.left_term \
            and other.right_term == self.right_term

    def __repr__(self) -> str:
        """Gets a string representation of the rule."""
        return f"{self._left_term} -> {self._right_term}"
