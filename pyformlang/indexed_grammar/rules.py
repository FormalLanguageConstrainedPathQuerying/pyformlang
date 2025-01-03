"""Representation of rules in the indexed grammar."""

from typing import Dict, List, Set, Tuple, Iterable, Hashable

from pyformlang.cfg import Variable, Terminal

from .reduced_rule import ReducedRule
from .production_rule import ProductionRule
from .consumption_rule import ConsumptionRule
from .rule_ordering import RuleOrdering
from ..objects.cfg_objects.utils import to_variable, to_terminal


class Rules:
    """Class to store and manipulate indexed grammar rules.

    Parameters
    ----------
    rules:
        A list of all the rules.
    optim:
        Optimization of the order of the rules
        0 -> given order
        1 -> reverse order
        2 -> order by core number
        3 -> reverse order of core number
        4 -> reverse order by arborescence
        5 -> order by arborescence
        6 -> order by number of edges
        7 -> reverse order by number of edges
        8 -> random order
    """

    def __init__(self, rules: Iterable[ReducedRule], optim: int = 7) -> None:
        """Initializes the rules of the indexed grammar."""
        self._rules: List[ReducedRule] = []
        self._consumption_rules: Dict[Terminal, List[ConsumptionRule]] = {}
        self._optim = optim
        for rule in rules:
            # We separate consumption rule from other
            if isinstance(rule, ConsumptionRule):
                temp = self._consumption_rules.setdefault(rule.f_parameter, [])
                if rule not in temp:
                    temp.append(rule)
                self._consumption_rules[rule.f_parameter] = temp
            else:
                if rule not in self._rules:
                    self._rules.append(rule)
        rule_ordering = RuleOrdering(self._rules, self._consumption_rules)
        if optim == 1:
            self._rules = rule_ordering.reverse()
        elif optim == 2:
            self._rules = rule_ordering.order_by_core()
        elif optim == 3:
            self._rules = rule_ordering.order_by_core(reverse=True)
        elif optim == 4:
            self._rules = rule_ordering.order_by_arborescence(reverse=True)
        elif optim == 5:
            self._rules = rule_ordering.order_by_arborescence(reverse=False)
        elif optim == 6:
            self._rules = rule_ordering.order_by_edges()
        elif optim == 7:
            self._rules = rule_ordering.order_by_edges(reverse=True)
        elif optim == 8:
            self._rules = rule_ordering.order_random()

    @property
    def optim(self) -> int:
        """Gets the optimization number."""
        return self._optim

    @property
    def rules(self) -> List[ReducedRule]:
        """Gets the non consumption rules."""
        return self._rules

    @property
    def length(self) -> Tuple[int, int]:
        """Get the total number of rules.

        Returns
        -------
        A pair of the number of non consumption rules and the number \
        of consumption rules.
        """
        return len(self._rules), len(self._consumption_rules.values())

    @property
    def consumption_rules(self) -> Dict[Terminal, List[ConsumptionRule]]:
        """Gets a dictionary of consumption rules by the consumed symbol."""
        return self._consumption_rules

    @property
    def non_terminals(self) -> Set[Variable]:
        """Gets all the nonterminals used by all the rules."""
        non_terminals = set()
        for rules in self._consumption_rules.values():
            for rule in rules:
                non_terminals.update(rule.non_terminals)
        for rule in self._rules:
            non_terminals.update(rule.non_terminals)
        return non_terminals

    @property
    def terminals(self) -> Set[Terminal]:
        """Gets all the terminals used by all the rules."""
        terminals = set()
        for rules in self._consumption_rules.values():
            for rule in rules:
                terminals.update(rule.terminals)
        for rule in self._rules:
            terminals.update(rule.terminals)
        return terminals

    def add_production(self,
                       left: Hashable,
                       right: Hashable,
                       prod: Hashable) -> None:
        """Adds the production rule.

        A rule of form:
            left[sigma] -> right[prod sigma]

        Parameters
        ----------
        left:
            The left nonterminal of the rule.
        right:
            The right nonterminal of the rule.
        prod:
            The production used in the rule.
        """
        left = to_variable(left)
        right = to_variable(right)
        prod = to_terminal(prod)
        self._rules.append(ProductionRule(left, right, prod))

    def remove_production(self,
                          left: Hashable,
                          right: Hashable,
                          prod: Hashable) -> None:
        """Removes the production rule.

        A rule of form:
            left[sigma] -> right[prod sigma]

        Parameters
        ----------
        left:
            The left nonterminal of the rule.
        right:
            The right nonterminal of the rule.
        prod:
            The production used in the rule.
        """
        left = to_variable(left)
        right = to_variable(right)
        prod = to_terminal(prod)
        self._rules = list(filter(lambda x: not (isinstance(x, ProductionRule)
                                                 and x.left_term == left
                                                 and x.right_term == right
                                                 and x.production == prod),
                                  self._rules))
