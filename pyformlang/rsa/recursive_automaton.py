"""Representation of a recursive automaton."""

from typing import Dict, Set, AbstractSet, Optional, Hashable, Any

from pyformlang.finite_automaton import Symbol
from pyformlang.regular_expression import Regex
from pyformlang.cfg import Epsilon

from .box import Box
from ..objects.finite_automaton_objects.utils import to_symbol


class RecursiveAutomaton:
    """Representation of a recursive automaton.

    Parameters
    ----------
    start_box:
        A start box of the recursive automaton.
    boxes:
        A finite set of boxes.
    """

    def __init__(self,
                 start_box: Box,
                 boxes: AbstractSet[Box]) -> None:
        """Initializes the recursive automaton."""
        self._nonterminal_to_box: Dict[Symbol, Box] = {}
        self._start_nonterminal = start_box.nonterminal
        if start_box not in boxes:
            self._nonterminal_to_box[start_box.nonterminal] = start_box
        for box in boxes:
            self._nonterminal_to_box[box.nonterminal] = box

    @property
    def nonterminals(self) -> Set[Symbol]:
        """Gets the set of nonterminals of the automaton."""
        return set(self._nonterminal_to_box.keys())

    @property
    def boxes(self) -> Set[Box]:
        """Gets the set of boxes of the automaton."""
        return set(self._nonterminal_to_box.values())

    @property
    def start_nonterminal(self) -> Symbol:
        """Gets the start nonterminal of the automaton."""
        return self._start_nonterminal

    @property
    def start_box(self) -> Box:
        """Gets the start box of the automaton."""
        return self._nonterminal_to_box[self.start_nonterminal]

    def get_box_by_nonterminal(self, nonterminal: Hashable) -> Optional[Box]:
        """Gets a box by the given nonterminal.

        Parameters
        ----------
        nonterminal:
            A nonterminal representing a box.

        Returns
        -------
        The box represented by the given nonterminal.
        """
        nonterminal = to_symbol(nonterminal)
        return self._nonterminal_to_box.get(nonterminal, None)

    def get_number_boxes(self) -> int:
        """Gets the number of boxes in the current automaton."""
        return len(self._nonterminal_to_box)

    @classmethod
    def from_regex(cls, regex: Regex, start_nonterminal: Hashable) \
            -> "RecursiveAutomaton":
        """Creates a recursive automaton from regular expression.

        Parameters
        ----------
        regex:
            The regular expression to create automaton from.
        start_nonterminal:
            The start nonterminal for the recursive automaton.

        Returns
        -------
        The new recursive automaton built from regular expression.
        """
        start_nonterminal = to_symbol(start_nonterminal)
        box = Box(regex.to_minimal_dfa(), start_nonterminal)
        return RecursiveAutomaton(box, {box})

    @classmethod
    def from_ebnf(cls, text: str, start_nonterminal: Hashable = "S") \
            -> "RecursiveAutomaton":
        """Creates a recursive automaton from Extended Backus-Naur Form.

        Parameters
        -----------
        text:
            The text of transform.
        start_nonterminal:
            The start nonterminal.

        Returns
        -------
        The new recursive automaton built from context-free grammar.
        """
        start_nonterminal = to_symbol(start_nonterminal)
        productions: Dict[Hashable, str] = {}
        boxes = set()
        nonterminals = set()
        for production in text.splitlines():
            production = production.strip()
            if "->" not in production:
                continue

            head, body = production.split("->")
            head = head.strip()
            body = body.strip()
            nonterminals.add(to_symbol(head))

            if body == "":
                body = Epsilon().to_text()

            if head in productions:
                productions[head] += " | " + body
            else:
                productions[head] = body

        for head, body in productions.items():
            boxes.add(Box(Regex(body).to_minimal_dfa(), to_symbol(head)))
        start_box_dfa = Regex(productions[start_nonterminal.value]) \
            .to_minimal_dfa()
        start_box = Box(start_box_dfa, start_nonterminal)
        return RecursiveAutomaton(start_box, boxes)

    def is_equal_to(self, other: "RecursiveAutomaton") -> bool:
        """Check whether two recursive automata are equal by boxes.

        Not equivalency in terms of formal languages theory, just mapping boxes

        Parameters
        ----------
        other:
            The other recursive automaton.

        Returns
        -------
        Whether the two recursive automata are equal or not.
        """
        return self.boxes == other.boxes

    def __eq__(self, other: Any) -> bool:
        """Checks if the current automaton is equal to the given object."""
        if not isinstance(other, RecursiveAutomaton):
            return False
        return self.is_equal_to(other)

    def to_dot(self) -> str:
        """Creates dot representation of recursive automaton.

        Returns
        -------
        The dot representation of current recursive automaton.
        """
        dot_string = 'digraph "" {'
        for box in self._nonterminal_to_box.values():
            dot_string += f'\n{box.to_subgraph_dot()}'
        dot_string += "\n}"
        return dot_string
