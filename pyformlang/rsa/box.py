"""
Representation of a box for recursive automaton
"""
from typing import Set, Any

from pyformlang.finite_automaton.epsilon_nfa import EpsilonNFA
from pyformlang.finite_automaton.finite_automaton import to_symbol
from pyformlang.finite_automaton.state import State
from pyformlang.finite_automaton.symbol import Symbol


class Box:
    """ Represents a box for recursive automaton

    This class represents a box for recursive automaton

    Parameters
    ----------
    enfa : :class:`~pyformlang.finite_automaton.EpsilonNFA`
        A epsilon nfa
    nonterminal : :class:`~pyformlang.finite_automaton.Symbol`
        A nonterminal for epsilon nfa

    """

    def __init__(self, enfa: EpsilonNFA, nonterminal: Any) -> None:
        self._enfa: EpsilonNFA = enfa
        self._nonterminal: Symbol = to_symbol(nonterminal)

    def to_subgraph_dot(self) -> str:
        """Creates a named subgraph representing a box"""
        graph = self._enfa.to_networkx()
        strange_nodes = []
        nonterminal = self.nonterminal.value.replace('"', '').replace("'", "").replace(".", "")
        dot_string = (f'subgraph cluster_{nonterminal}\n{{ label="{nonterminal}"\n'
                      f'fontname="Helvetica,Arial,sans-serif"\n'
                      f'node [fontname="Helvetica,Arial,sans-serif"]\n'
                      f'edge [fontname="Helvetica,Arial,sans-serif"]\nrankdir=LR;\n'
                      f'node [shape = circle style=filled fillcolor=white]')
        for node, data in graph.nodes(data=True):
            node = node.replace('"', '').replace("'", "")
            if 'is_start' not in data.keys() or 'is_final' not in data.keys():
                strange_nodes.append(node)
                continue
            if data['is_start']:
                dot_string += f'\n"{node}" [fillcolor = green];'
            if data['is_final']:
                dot_string += f'\n"{node}" [shape = doublecircle];'
        for strange_node in strange_nodes:
            graph.remove_node(strange_node)
        for node_from, node_to, data in graph.edges(data=True):
            node_from = node_from.replace('"', '').replace("'", "")
            node_to = node_to.replace('"', '').replace("'", "")
            label = data['label'].replace('"', '').replace("'", "")
            dot_string += f'\n"{node_from}" -> "{node_to}" [label = "{label}"];'
        dot_string += "\n}"
        return dot_string

    @property
    def enfa(self) -> EpsilonNFA:
        """ Box's enfa """
        return self._enfa

    @property
    def nonterminal(self) -> Symbol:
        """ Box's nonterminal """
        return self._nonterminal

    @property
    def start_states(self) -> Set[State]:
        """ The start states """
        return self._enfa.start_states

    @property
    def final_states(self) -> Set[State]:
        """ The final states """
        return self._enfa.final_states

    def is_equivalent_to(self, other: "Box") -> bool:
        """ Check whether two boxes are equivalent

        Parameters
        ----------
        other : :class:`~pyformlang.rsa.Box`
            A sequence of input symbols

        Returns
        ----------
        are_equivalent : bool
            Whether the two boxes are equivalent or not
        """

        return self._enfa.is_equivalent_to(other.enfa) \
            and self.nonterminal == other.nonterminal

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Box):
            return False
        return self.is_equivalent_to(other)

    def __hash__(self) -> int:
        return self._nonterminal.__hash__()
