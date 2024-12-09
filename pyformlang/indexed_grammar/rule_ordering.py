"""
Representation of a way to order rules
"""

from typing import List, Dict

from queue import Queue
from random import shuffle
from networkx import DiGraph, core_number, minimum_spanning_tree

from pyformlang.cfg import Terminal

from .reduced_rule import ReducedRule
from .consumption_rule import ConsumptionRule
from .duplication_rule import DuplicationRule
from .production_rule import ProductionRule


class RuleOrdering:
    """A class to order rules in an indexed grammar

    Parameters
    ----------
    rules : iterable of :class:`~pyformlang.indexed_grammar.ReducedRule`
        The non consumption rules of the indexed grammar
    conso_rules : dict of any to \
      :class:`~pyformlang.indexed_grammar.ConsumptionRule`
        The consumption rules of the indexed grammar
    """

    def __init__(self,
                 rules: List[ReducedRule],
                 conso_rules: Dict[Terminal, List[ConsumptionRule]]) -> None:
        self.rules = rules
        self.conso_rules = conso_rules

    def reverse(self) -> List[ReducedRule]:
        """The reverser ordering, simply reverse the order.

        Returns
        ----------
        new_rules : iterable of \
        :class:`~pyformlang.indexed_grammar.ReducedRule`
            The reversed rules
        """
        return self.rules[::1]

    def _get_graph(self) -> DiGraph:
        """ Get the graph of the non-terminals in the rules. If there
        there is a link between A and B (oriented), it means that modifying A
        may modify B"""
        di_graph = DiGraph()
        for rule in self.rules:
            if isinstance(rule, DuplicationRule):
                if rule.right_terms[0] != rule.left_term:
                    di_graph.add_edge(rule.right_terms[0], rule.left_term)
                if rule.right_terms[1] != rule.left_term:
                    di_graph.add_edge(rule.right_terms[1], rule.left_term)
            if isinstance(rule, ProductionRule):
                f_rules = self.conso_rules.setdefault(
                    rule.production, [])
                for f_rule in f_rules:
                    if f_rule.right_term != rule.left_term:
                        di_graph.add_edge(f_rule.right_term, rule.left_term)
        return di_graph

    def order_by_core(self, reverse: bool = False) -> List[ReducedRule]:
        """Order the rules using the core numbers

        Parameters
        ----------
        reverse : bool
            Boolean to know if we should reverse the order

        Returns
        ----------
        new_rules : iterable of \
        :class:`~pyformlang.indexed_grammar.ReducedRule`
            The rules ordered using core number
        """
        # Graph construction
        di_graph = self._get_graph()
        # Get core number, careful the degree is in + out
        core_numbers = dict(core_number(di_graph))
        new_order = sorted(self.rules,
                           key=lambda x: core_numbers.setdefault(
                               x.left_term, 0))
        if reverse:
            new_order.reverse()
        return new_order

    def order_by_arborescence(self, reverse: bool = True) \
            -> List[ReducedRule]:
        """Order the rules using the arborescence method.

        Parameters
        ----------
        reverse : bool
            Boolean to know if we should reverse the order

        Returns
        ----------
        new_rules : iterable of \
        :class:`~pyformlang.indexed_grammar.ReducedRule`
            The rules ordered using core number
        """
        di_graph = self._get_graph()
        arborescence = minimum_spanning_tree(di_graph.to_undirected())
        to_process = Queue()
        processed = set()
        res = {}
        res["S"] = 0
        for symbol in arborescence["S"]:
            if symbol not in processed:
                res[symbol] = 1
                processed.add(symbol)
                to_process.put(symbol)
        while not to_process.empty():
            current = to_process.get()
            for symbol in arborescence[current]:
                if symbol not in processed:
                    res[symbol] = res[current] + 1
                    processed.add(symbol)
                    to_process.put(symbol)
        new_order = sorted(self.rules,
                           key=lambda x: res.setdefault(
                               x.left_term, 0))
        if reverse:
            new_order.reverse()
        return new_order

    @staticmethod
    def _get_len_out(di_graph: DiGraph, rule: ReducedRule) -> int:
        """Get the number of out edges of a rule (more exactly, the non \
        terminal at its left.

        Parameters
        ----------
        di_graph : DiGraph
            A directed graph
        rule : :class:`~pyformlang.indexed_grammar.ReducedRule`
            The rule
        """
        if rule.left_term in di_graph:
            return len(di_graph[rule.left_term])
        return 0

    def order_by_edges(self, reverse: bool = False) -> List[ReducedRule]:
        """Order using the number of edges.

        Parameters
        ----------
        reverse : bool
            Boolean to know if we should reverse the order

        Returns
        ----------
        new_rules : iterable of \
        :class:`~pyformlang.indexed_grammar.ReducedRule`
            The rules ordered by number of edges
        """
        di_graph = self._get_graph()
        new_order = sorted(self.rules, key=lambda x:
                           self._get_len_out(di_graph, x))
        if reverse:
            new_order.reverse()
        return new_order

    def order_random(self) -> List[ReducedRule]:
        """The random ordering

        Returns
        ----------
        new_rules : iterable of \
        :class:`~pyformlang.indexed_grammar.ReducedRule`
            The rules ordered at random
        """
        shuffle(self.rules)
        return self.rules
