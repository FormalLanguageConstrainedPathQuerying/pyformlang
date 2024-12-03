""" Basic grammar representation """

from typing import Set, AbstractSet, Iterable, Optional, Hashable, TypeVar, Type
from abc import abstractmethod

from ..objects.cfg_objects import Variable, Terminal, Production

GrammarT = TypeVar("GrammarT", bound="Grammar")


class Grammar:
    """ Basic grammar representation """

    @abstractmethod
    def __init__(self,
                 variables: AbstractSet[Hashable] = None,
                 terminals: AbstractSet[Hashable] = None,
                 start_symbol: Hashable = None,
                 productions: Iterable[Production] = None) -> None:
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
    def generate_epsilon(self) -> bool:
        """ Whether the grammar generates epsilon or not """
        raise NotImplementedError

    @abstractmethod
    def to_normal_form(self) -> "Grammar":
        """ Gets Chomsky normal form of the grammar """
        raise NotImplementedError

    def is_normal_form(self) -> bool:
        """
        Whether the current grammar is in Chomsky Normal Form

        Returns
        -------
        is_normal_form : bool
            If the current grammar is in CNF
        """
        return all(
            production.is_normal_form() for production in self._productions)

    def to_text(self) -> str:
        """
        Turns the grammar into its string representation. This might lose some\
         type information and the start_symbol.
        Returns
        -------
        text : str
            The grammar as a string.
        """
        res = []
        for production in self._productions:
            res.append(str(production.head) + " -> " +
                       " ".join([x.to_text() for x in production.body]))
        return "\n".join(res) + "\n"

    @classmethod
    def from_text(
        cls: Type[GrammarT],
        text: str,
        start_symbol: Optional[Hashable] = Variable("S")) \
            -> GrammarT:
        """
        Read a context free grammar from a text.
        The text contains one rule per line.
        The structure of a production is:
        head -> body1 | body2 | ... | bodyn
        where | separates the bodies.
        A variable (or non terminal) begins by a capital letter.
        A terminal begins by a non-capital character
        Terminals and Variables are separated by spaces.
        An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є.
        If you want to have a variable name starting with a non-capital \
        letter or a terminal starting with a capital letter, you can \
        explicitly give the type of your symbol with "VAR:yourVariableName" \
        or "TER:yourTerminalName" (with the quotation marks). For example:
        S -> "TER:John" "VAR:d" a b

        Parameters
        ----------
        text : str
            The text of transform
        start_symbol : str, optional
            The start symbol, S by default

        Returns
        -------
        cfg : :class:`~pyformlang.cfg.CFG`
            A context free grammar.
        """
        variables = set()
        productions = set()
        terminals = set()
        cls._read_text(text, productions, terminals, variables)
        return cls(variables=variables, terminals=terminals,
                   productions=productions, start_symbol=start_symbol)

    @classmethod
    def _read_text(cls,
                   text: str,
                   productions: Set[Production],
                   terminals: Set[Terminal],
                   variables: Set[Variable]) -> None:
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            cls._read_line(line, productions, terminals, variables)

    @classmethod
    @abstractmethod
    def _read_line(cls,
                   line: str,
                   productions: Set[Production],
                   terminals: Set[Terminal],
                   variables: Set[Variable]) -> None:
        raise NotImplementedError
