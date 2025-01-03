"""Representation of a consumption rule.

A rule that consumes something on the stack.
"""

from typing import List, Set, Hashable, Any

from pyformlang.cfg import CFGObject, Variable, Terminal

from .reduced_rule import ReducedRule
from ..objects.cfg_objects.utils import to_variable, to_terminal


class ConsumptionRule(ReducedRule):
    """Representation of a consumption rule.

    It is a rule of form:
        C[r sigma] -> B[sigma]

    Parameters
    ----------
    f_param:
        The consumed symbol, "r" here.
    left_term:
        The non terminal on the left, "C" here.
    right_term:
        The non terminal on the right, "B" here.
    """

    def __init__(self,
                 f_param: Hashable,
                 left_term: Hashable,
                 right_term: Hashable) -> None:
        """Initializes the consumption rule."""
        self._f = to_terminal(f_param)
        self._left_term = to_variable(left_term)
        self._right_term = to_variable(right_term)

    @property
    def f_parameter(self) -> Terminal:
        """Gets the symbol consumed by the rule."""
        return self._f

    @property
    def production(self) -> Terminal:
        """Gets the symbol produced by the rule."""
        raise NotImplementedError

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
        return {self._f}

    def __eq__(self, other: Any) -> bool:
        """Checks if the rule is equal to the given object."""
        if not isinstance(other, ConsumptionRule):
            return False
        return other.left_term == self.left_term \
            and other.right_term == self.right_term \
            and other.f_parameter == self.f_parameter

    def __repr__(self) -> str:
        """Gets a string representation of the rule."""
        return f"{self._left_term} [ {self._f} ] -> {self._right_term}"
