"""
A representation of a duplication rule, i.e. a rule that duplicates the stack
"""

from typing import List, Set, Hashable, Any

from pyformlang.cfg import CFGObject, Variable, Terminal

from .reduced_rule import ReducedRule
from ..objects.cfg_objects.utils import to_variable


class DuplicationRule(ReducedRule):
    """Represents a duplication rule, i.e. a rule of the form:
        A[sigma] -> B[sigma] C[sigma]

    Parameters
    ----------
    left_term : any
        The non-terminal on the left of the rule (A here)
    right_term0 : any
        The first non-terminal on the right of the rule (B here)
    right_term1 : any
        The second non-terminal on the right of the rule (C here)
    """

    def __init__(self,
                 left_term: Hashable,
                 right_term0: Hashable,
                 right_term1: Hashable) -> None:
        self._left_term = to_variable(left_term)
        self._right_terms = (to_variable(right_term0),
                             to_variable(right_term1))

    @property
    def f_parameter(self) -> Terminal:
        raise NotImplementedError

    @property
    def production(self) -> Terminal:
        raise NotImplementedError

    @property
    def left_term(self) -> Variable:
        """Gives the non-terminal on the left of the rule

        Returns
        ---------
        left_term : any
            The left term of the rule
        """
        return self._left_term

    @property
    def right_term(self) -> CFGObject:
        raise NotImplementedError

    @property
    def right_terms(self) -> List[CFGObject]:
        """Gives the non-terminals on the right of the rule

        Returns
        ---------
        right_terms : iterable of any
            The right terms of the rule
        """
        return list(self._right_terms)

    @property
    def non_terminals(self) -> Set[Variable]:
        """Gives the set of non-terminals used in this rule

        Returns
        ---------
        non_terminals : iterable of any
            The non terminals used in this rule
        """
        return {self._left_term, *self._right_terms}

    @property
    def terminals(self) -> Set[Terminal]:
        """Gets the terminals used in the rule

        Returns
        ----------
        terminals : set of any
            The terminals used in this rule
        """
        return set()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DuplicationRule):
            return False
        return other.left_term == self._left_term \
            and other.right_terms == self.right_terms

    def __repr__(self) -> str:
        """Gives a string representation of the rule, ignoring the sigmas"""
        return f"{self._left_term} -> " \
            + f"{self._right_terms[0]} {self._right_terms[1]}"
