""" Basic grammar representation """

from typing import Set, Optional
from abc import abstractmethod

from ..objects.cfg_objects import Variable, Terminal, Production


class Grammar:
    """ Basic grammar representation """

    def __init__(self) -> None:
        self._variables: Set[Variable]
        self._terminals: Set[Terminal]
        self._start_symbol: Optional[Variable]
        self._productions: Set[Production]

    @property
    def variables(self) -> Set[Variable]:
        """ Gives the variables

        Returns
        ----------
        variables : set of :class:`~pyformlang.cfg.Variable`
            The variables of the CFG
        """
        return self._variables

    @property
    def terminals(self) -> Set[Terminal]:
        """ Gives the terminals

        Returns
        ----------
        terminals : set of :class:`~pyformlang.cfg.Terminal`
            The terminals of the CFG
        """
        return self._terminals

    @property
    def productions(self) -> Set[Production]:
        """ Gives the productions

        Returns
        ----------
        productions : set of :class:`~pyformlang.cfg.Production`
            The productions of the CFG
        """
        return self._productions

    @property
    def start_symbol(self) -> Optional[Variable]:
        """ Gives the start symbol

        Returns
        ----------
        start_variable : :class:`~pyformlang.cfg.Variable`
            The start symbol of the CFG
        """
        return self._start_symbol

    @abstractmethod
    def to_normal_form(self) -> "Grammar":
        """ Gets some normal form of the grammar"""
        raise NotImplementedError

    @abstractmethod
    def is_normal_form(self) -> bool:
        """ Whether the grammar is in normal form """
        raise NotImplementedError
