"""Representation of a production rule.

A rule that pushes on the stack.
"""

from typing import List, Set, Hashable, Any

from pyformlang.cfg import CFGObject, Variable, Terminal

from .reduced_rule import ReducedRule
from ..objects.cfg_objects.utils import to_variable, to_terminal


class ProductionRule(ReducedRule):
    """Representation of a production rule.

    It is a rule of form:
        A[sigma] -> B[r sigma]

    Parameters
    ----------
    left_term:
        The non-terminal on the left side of the rule, "A" here.
    right_term:
        The non-terminal on the right side of the rule, "B" here.
    production:
        The terminal produced by the rule, "r" here.
    """

    def __init__(self,
                 left_term: Hashable,
                 right_term: Hashable,
                 production: Hashable) -> None:
        """Initializes the production rule."""
        self._left_term = to_variable(left_term)
        self._right_term = to_variable(right_term)
        self._production = to_terminal(production)

    @property
    def f_parameter(self) -> Terminal:
        """Gets the symbol consumed by the rule."""
        raise NotImplementedError

    @property
    def production(self) -> Terminal:
        """Gets the symbol produced by the rule."""
        return self._production

    @property
    def left_term(self) -> Variable:
        """Gets a nonterminal on the left of the rule."""
        return self._left_term

    @property
    def right_term(self) -> Variable:
        """Gets a nonterminal on the right of the rule."""
        return self._right_term

    @property
    def right_terms(self) -> List[CFGObject]:
        """Gets a list of right terms of the rule."""
        return [self._right_term]

    @property
    def non_terminals(self) -> Set[Variable]:
        """Gets the nonterminals used in the rule."""
        return {self._left_term, self._right_term}

    @property
    def terminals(self) -> Set[Terminal]:
        """Gets the terminals used in the rule."""
        return {self._production}

    def __eq__(self, other: Any) -> bool:
        """Checks if the rule is equal to the given object."""
        if not isinstance(other, ProductionRule):
            return False
        return other.left_term == self.left_term \
            and other.right_term == self.right_term \
            and other.production == self.production

    def __repr__(self) -> str:
        """Gets a string representation of the rule."""
        return f"{self._left_term} -> {self._right_term} [ {self._production} ]"
