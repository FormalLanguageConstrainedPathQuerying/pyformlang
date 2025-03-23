"""
Representation of a consumption rule, i.e. a rule that consumes something on \
the stack
"""

from typing import List, Set, Hashable, Any

from pyformlang.cfg import CFGObject, Variable, Terminal

from .reduced_rule import ReducedRule
from ..objects.cfg_objects.utils import to_variable, to_terminal


class ConsumptionRule(ReducedRule):
    """ Contains a representation of a consumption rule, i.e. a rule of the \
    form:
            C[ r sigma] -> B[sigma]

    Parameters
    ----------
    f_param : any
        The consumed symbol
    left : any
        The non terminal on the left (here C)
    right : any
        The non terminal on the right (here B)
    """

    def __init__(self,
                 f_param: Hashable,
                 left_term: Hashable,
                 right_term: Hashable) -> None:
        self._f = to_terminal(f_param)
        self._left_term = to_variable(left_term)
        self._right_term = to_variable(right_term)

    @property
    def f_parameter(self) -> Terminal:
        """Gets the symbol which is consumed

        Returns
        ----------
        f : any
            The symbol being consumed by the rule
        """
        return self._f

    @property
    def production(self) -> Terminal:
        raise NotImplementedError

    @property
    def left_term(self) -> Variable:
        """Gets the symbol on the left of the rule

        left : any
            The left symbol of the rule
        """
        return self._left_term

    @property
    def right_term(self) -> Variable:
        """Gets the symbol on the right of the rule

        right : any
            The right symbol
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

        non_terminals : iterable of any
            The non_terminals used in the rule
        """
        return {self._left_term, self._right_term}

    @property
    def terminals(self) -> Set[Terminal]:
        """Gets the terminals used in the rule

        terminals : set of any
            The terminals used in the rule
        """
        return {self._f}

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ConsumptionRule):
            return False
        return other.left_term == self.left_term \
            and other.right_term == self.right_term \
            and other.f_parameter == self.f_parameter

    def __repr__(self) -> str:
        return f"{self._left_term} [ {self._f} ] -> {self._right_term}"
