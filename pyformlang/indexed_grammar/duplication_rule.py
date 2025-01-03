"""Representation of a duplication rule.

A rule that duplicates the stack.
"""

from typing import List, Set, Hashable, Any

from pyformlang.cfg import CFGObject, Variable, Terminal

from .reduced_rule import ReducedRule
from ..objects.cfg_objects.utils import to_variable


class DuplicationRule(ReducedRule):
    """Representation of a duplication rule.

    It is a rule of form:
        A[sigma] -> B[sigma] C[sigma]

    Parameters
    ----------
    left_term:
        The non-terminal on the left of the rule, "A" here.
    right_term0:
        The first non-terminal on the right of the rule, "B" here.
    right_term1:
        The second non-terminal on the right of the rule, "C" here.
    """

    def __init__(self,
                 left_term: Hashable,
                 right_term0: Hashable,
                 right_term1: Hashable) -> None:
        """Initializes the duplication rule."""
        self._left_term = to_variable(left_term)
        self._right_terms = (to_variable(right_term0),
                             to_variable(right_term1))

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
    def right_term(self) -> CFGObject:
        """Gets the single right term of the rule."""
        raise NotImplementedError

    @property
    def right_terms(self) -> List[CFGObject]:
        """Gets a list of right terms of the rule."""
        return list(self._right_terms)

    @property
    def non_terminals(self) -> Set[Variable]:
        """Gets the nonterminals used in the rule."""
        return {self._left_term, *self._right_terms}

    @property
    def terminals(self) -> Set[Terminal]:
        """Gets the terminals used in the rule."""
        return set()

    def __eq__(self, other: Any) -> bool:
        """Checks if the rule is equal to the given object."""
        if not isinstance(other, DuplicationRule):
            return False
        return other.left_term == self._left_term \
            and other.right_terms == self.right_terms

    def __repr__(self) -> str:
        """Gets a string representation of the rule."""
        return f"{self._left_term} -> " \
            + f"{self._right_terms[0]} {self._right_terms[1]}"
