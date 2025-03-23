"""
Represents a production rule, i.e. a rule that pushed on the stack
"""

from typing import List, Set, Hashable, Any

from pyformlang.cfg import CFGObject, Variable, Terminal

from .reduced_rule import ReducedRule
from ..objects.cfg_objects.utils import to_variable, to_terminal


class ProductionRule(ReducedRule):
    """Represents a production rule, i.e. a rule of the form:
        A[sigma] -> B[r sigma]

    Parameters
    ----------
    left : any
        The non-terminal on the left side of the rule, A here
    right : any
        The non-terminal on the right side of the rule, B here
    prod : any
        The terminal used in the rule, "r" here
    """

    def __init__(self,
                 left_term: Hashable,
                 right_term: Hashable,
                 production: Hashable) -> None:
        self._left_term = to_variable(left_term)
        self._right_term = to_variable(right_term)
        self._production = to_terminal(production)

    @property
    def f_parameter(self) -> Terminal:
        raise NotImplementedError

    @property
    def production(self) -> Terminal:
        """Gets the terminal used in the production

        Returns
        ----------
        production : any
            The production used in this rule
        """
        return self._production

    @property
    def left_term(self) -> Variable:
        """Gets the non-terminal on the left side of the rule

        Returns
        ----------
        left_term : any
            The left term of this rule
        """
        return self._left_term

    @property
    def right_term(self) -> Variable:
        """Gets the non-terminal on the right side of the rule

        Returns
        ----------
        right_term : any
            The right term used in this rule
        """
        return self._right_term

    @property
    def right_terms(self) -> List[CFGObject]:
        """Gives the non-terminals on the right of the rule

        Returns
        ---------
        right_terms : iterable of any
            The right terms of the rule
        """
        return [self._right_term]

    @property
    def non_terminals(self) -> Set[Variable]:
        """Gets the non-terminals used in the rule

        Returns
        ----------
        non_terminals : any
            The non terminals used in this rules
        """
        return {self._left_term, self._right_term}

    @property
    def terminals(self) -> Set[Terminal]:
        """Gets the terminals used in the rule

        Returns
        ----------
        terminals : any
            The terminals used in this rule
        """
        return {self._production}

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ProductionRule):
            return False
        return other.left_term == self.left_term \
            and other.right_term == self.right_term \
            and other.production == self.production

    def __repr__(self) -> str:
        """Gets the string representation of the rule"""
        return f"{self._left_term} -> {self._right_term} [ {self._production} ]"
