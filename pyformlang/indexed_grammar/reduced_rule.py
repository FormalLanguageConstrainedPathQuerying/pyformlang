"""
Representation of a reduced rule
"""

from typing import List, Set
from abc import abstractmethod

from pyformlang.cfg import Variable, Terminal
from pyformlang.cfg.cfg_object import CFGObject


class ReducedRule:
    """Representation of all possible reduced forms.
    They can be of four types :
        * Consumption
        * Production
        * End
        * Duplication
    """

    @property
    @abstractmethod
    def f_parameter(self) -> Terminal:
        """The f parameter

        Returns
        ----------
        f : cfg.Terminal
            The f parameter
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def production(self) -> Terminal:
        """The production

        Returns
        ----------
        right_terms : any
            The production
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def left_term(self) -> Variable:
        """The left term

        Returns
        ----------
        left_term : cfg.Variable
            The left term of the rule
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def right_term(self) -> CFGObject:
        """The unique right term

        Returns
        ----------
        right_term : cfg.cfg_object.CFGObject
            The unique right term of the rule
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def right_terms(self) -> List[CFGObject]:
        """The right terms

        Returns
        ----------
        right_terms : list of cfg.cfg_object.CFGObject
            The right terms of the rule
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def non_terminals(self) -> Set[Variable]:
        """Gets the non-terminals used in the rule

        terminals : set of cfg.Variable
            The non-terminals used in the rule
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def terminals(self) -> Set[Terminal]:
        """Gets the terminals used in the rule

        terminals : set of cfg.Terminal
            The terminals used in the rule
        """
        raise NotImplementedError
