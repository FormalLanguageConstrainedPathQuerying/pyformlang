"""Representation of a reduced rule of an indexed grammar.

Rule of any of available forms.
"""

from typing import List, Set, Any
from abc import abstractmethod

from pyformlang.cfg import CFGObject, Variable, Terminal


class ReducedRule:
    """Representation of any of possible reduced forms.

    They can be of four types:
        * Consumption
        * Production
        * End
        * Duplication
    """

    @property
    @abstractmethod
    def f_parameter(self) -> Terminal:
        """Gets the symbol consumed by the rule."""
        raise NotImplementedError

    @property
    @abstractmethod
    def production(self) -> Terminal:
        """Gets the symbol produced by the rule."""
        raise NotImplementedError

    @property
    @abstractmethod
    def left_term(self) -> Variable:
        """Gets a nonterminal on the left of the rule."""
        raise NotImplementedError

    @property
    @abstractmethod
    def right_term(self) -> CFGObject:
        """Gets the single right term of the rule."""
        raise NotImplementedError

    @property
    @abstractmethod
    def right_terms(self) -> List[CFGObject]:
        """Gets a list of right terms of the rule."""
        raise NotImplementedError

    @property
    @abstractmethod
    def non_terminals(self) -> Set[Variable]:
        """Gets the nonterminals used in the rule."""
        raise NotImplementedError

    @property
    @abstractmethod
    def terminals(self) -> Set[Terminal]:
        """Gets the terminals used in the rule."""
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Checks if the rule is equal to the given object."""
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        """Gets a string representation of the rule."""
        raise NotImplementedError
