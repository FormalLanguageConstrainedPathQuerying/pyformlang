"""
Represents a end rule, i.e. a rule which give only a terminal
"""

from typing import List, Set, Hashable, Any

from pyformlang.cfg import CFGObject, Variable, Terminal

from .reduced_rule import ReducedRule
from ..objects.cfg_objects.utils import to_variable, to_terminal


class EndRule(ReducedRule):
    """Represents an end rule, i.e. a rule of the form:
        A[sigma] -> a

    Parameters
    -----------
    left : any
        The non-terminal on the left, "A" here
    right : any
        The terminal on the right, "a" here
    """

    def __init__(self, left_term: Hashable, right_term: Hashable) -> None:
        self._left_term = to_variable(left_term)
        self._right_term = to_terminal(right_term)

    @property
    def f_parameter(self) -> Terminal:
        raise NotImplementedError

    @property
    def production(self) -> Terminal:
        raise NotImplementedError

    @property
    def left_term(self) -> Variable:
        """Gets the non-terminal on the left of the rule

        Returns
        ---------
        left_term : any
            The left non-terminal of the rule
        """
        return self._left_term

    @property
    def right_term(self) -> Terminal:
        """Gets the terminal on the right of the rule

        Returns
        ----------
        right_term : any
            The right terminal of the rule
        """
        return self._right_term

    @property
    def right_terms(self) -> List[CFGObject]:
        """Gives the terminals on the right of the rule

        Returns
        ---------
        right_terms : iterable of any
            The right terms of the rule
        """
        return [self._right_term]

    @property
    def non_terminals(self) -> Set[Variable]:
        """Gets the non-terminals used

        Returns
        ----------
        non_terminals : iterable of any
            The non terminals used in this rule
        """
        return {self._left_term}

    @property
    def terminals(self) -> Set[Terminal]:
        """Gets the terminals used

        Returns
        ----------
        terminals : set of any
             The terminals used in this rule
        """
        return {self._right_term}

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EndRule):
            return False
        return other.left_term == self.left_term \
            and other.right_term == self.right_term

    def __repr__(self) -> str:
        """Gets the string representation of the rule"""
        return f"{self._left_term} -> {self._right_term}"
