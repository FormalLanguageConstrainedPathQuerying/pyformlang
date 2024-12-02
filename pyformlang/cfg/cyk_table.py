"""
Representation of a CYK table
"""

from typing import Dict, List, Set, Iterable, Tuple, Any

from .grammar import Grammar
from .parse_tree import ParseTree
from ..objects.cfg_objects import CFGObject, Terminal, Epsilon


class CYKTable:
    """
    A CYK table

    Parameters
    ----------
    cfg : A context-free grammar
    word : iterable of Terminals
        The word from which we construct the CYK table
    """

    def __init__(self, grammar: Grammar, word: List[Terminal]) -> None:
        self._normal_form: Grammar = grammar.to_normal_form()
        self._word: List[Terminal] = word
        self._productions_d: Dict[Tuple, List[CFGObject]] = {}
        self._cyk_table: Dict[Tuple[int, int], Set[CYKNode]] = {}
        self._set_productions_by_body()
        if not self._generates_all_terminals():
            self._cyk_table[(0, len(self._word))] = set()
        else:
            self._set_cyk_table()

    def _set_productions_by_body(self) -> None:
        # Organize productions
        for production in self._normal_form.productions:
            temp = tuple(production.body)
            if temp in self._productions_d:
                self._productions_d[temp].append(production.head)
            else:
                self._productions_d[temp] = [production.head]

    def _set_cyk_table(self) -> None:
        self._initialize_cyk_table()
        self._propagate_in_cyk_table()

    def _get_windows(self) -> Iterable[Tuple[int, int]]:
        # The windows must in order by length
        for window_size in range(2, len(self._word) + 1):
            for start_window in range(len(self._word) - window_size + 1):
                yield start_window, start_window + window_size

    def _get_all_window_pairs(self, start_window: int, end_window: int) \
            -> Iterable[Tuple["CYKNode", "CYKNode"]]:
        for mid_window in range(start_window + 1, end_window):
            for var_b in self._cyk_table[(start_window, mid_window)]:
                for var_c in self._cyk_table[(mid_window, end_window)]:
                    yield var_b, var_c

    def _propagate_in_cyk_table(self) -> None:
        for start_window, end_window in self._get_windows():
            for var_b, var_c in self._get_all_window_pairs(start_window,
                                                           end_window):
                for var_a in self._productions_d.get((var_b.value,
                                                      var_c.value), []):
                    self._cyk_table[(start_window, end_window)].add(
                        CYKNode(var_a, var_b, var_c))

    def _initialize_cyk_table(self) -> None:
        for i, terminal in enumerate(self._word):
            self._cyk_table[(i, i + 1)] = \
                {CYKNode(x, CYKNode(terminal))
                 for x in self._productions_d[(terminal,)]}
        for window_size in range(2, len(self._word) + 1):
            for start_window in range(len(self._word) - window_size + 1):
                # We use set because we do not want duplicate
                # It makes iterations longer
                self._cyk_table[
                    (start_window, start_window + window_size)] = set()

    def generate_word(self) -> bool:
        """
        Checks is the word is generated
        Returns
        -------
        is_generated : bool

        """
        return self._normal_form.start_symbol \
            in self._cyk_table[(0, len(self._word))]

    def _generates_all_terminals(self) -> bool:
        generate_all_terminals = True
        for terminal in self._word:
            if (terminal,) not in self._productions_d:
                generate_all_terminals = False
        return generate_all_terminals

    def get_parse_tree(self) -> ParseTree:
        """
        Give the parse tree associated with this CYK Table

        Returns
        -------
        parse_tree : :class:`~pyformlang.cfg.ParseTree`
        """
        if not self._word:
            return CYKNode(self._normal_form.start_symbol or Epsilon())
        if not self.generate_word():
            raise DerivationDoesNotExist
        root = [
            x
            for x in self._cyk_table[(0, len(self._word))]
            if x == self._normal_form.start_symbol][0]
        return root


class CYKNode(ParseTree):
    """A node in the CYK table"""

    def __init__(self,
                 value: CFGObject,
                 left_son: "CYKNode" = None,
                 right_son: "CYKNode" = None) -> None:
        super().__init__(value)
        self.value = value
        self.left_son = left_son
        self.right_son = right_son
        if left_son is not None:
            self.sons.append(left_son)
        if right_son is not None:
            self.sons.append(right_son)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CYKNode):
            return self.value == other.value
        return self.value == other

    def __hash__(self) -> int:
        return hash(self.value)


class DerivationDoesNotExist(Exception):
    """Exception raised when the word cannot be derived"""
