"""
Representation of an indexed grammar
"""

# pylint: disable=cell-var-from-loop

from typing import Dict, List, Set, FrozenSet, Tuple, Hashable, Any

from pyformlang.cfg import CFGObject, Variable, Terminal
from pyformlang.finite_automaton import FiniteAutomaton
from pyformlang.regular_expression import Regex

from .rules import Rules
from .duplication_rule import DuplicationRule
from .production_rule import ProductionRule
from .end_rule import EndRule
from .utils import exists, addrec_bis
from ..objects.cfg_objects.utils import to_variable


class IndexedGrammar:
    """ Describes an indexed grammar.

    Parameters
    ----------
    rules : :class:`~pyformlang.indexed_grammar.Rules`
        The rules of the grammar, in reduced form put into a Rule
    start_variable : Any, optional
        The start symbol of the indexed grammar
    """

    def __init__(self,
                 rules: Rules,
                 start_variable: Hashable = "S") -> None:
        self._rules = rules
        self._start_variable = to_variable(start_variable)
        # Precompute all non-terminals
        non_terminals = self.non_terminals
        # We cache the marked items in case of future update of the query
        self._marked: Dict[CFGObject, Set[FrozenSet[Variable]]] = {}
        # Initialize the marked symbols
        # Mark the identity
        for non_terminal_a in non_terminals:
            self._marked[non_terminal_a] = set()
            temp = frozenset({non_terminal_a})
            self._marked[non_terminal_a].add(temp)
        # Mark all end symbols
        for non_terminal_a in non_terminals:
            if exists(self._rules.rules,
                      lambda x: x.is_end_rule()
                      and x.left_term == non_terminal_a):
                self._marked[non_terminal_a].add(frozenset())

    @property
    def rules(self) -> Rules:
        """ Get the rules of the grammar """
        return self._rules

    @property
    def start_variable(self) -> Variable:
        """ Get the start variable of the grammar """
        return self._start_variable

    @property
    def non_terminals(self) -> Set[Variable]:
        """Get all the non-terminals in the grammar

        Returns
        ----------
        terminals : iterable of any
            The non-terminals used in the grammar
        """
        return {self.start_variable} | self._rules.non_terminals

    @property
    def terminals(self) -> Set[Terminal]:
        """Get all the terminals in the grammar

        Returns
        ----------
        terminals : iterable of any
            The terminals used in the grammar
        """
        return self._rules.terminals

    def _duplication_processing(self, rule: DuplicationRule) \
            -> Tuple[bool, bool]:
        """Processes a duplication rule

        Parameters
        ----------
        rule : :class:`~pyformlang.indexed_grammar.DuplicationRule`
            The duplication rule to process
        """
        was_modified = False
        need_stop = False
        right_term_marked0 = []
        for marked_term0 in self._marked[rule.right_terms[0]]:
            right_term_marked1 = []
            for marked_term1 in self._marked[rule.right_terms[1]]:
                if marked_term0 <= marked_term1:
                    temp = marked_term1
                elif marked_term1 <= marked_term0:
                    temp = marked_term0
                else:
                    temp = marked_term0.union(marked_term1)
                # Check if it was marked before
                if temp not in self._marked[rule.left_term]:
                    was_modified = True
                    if rule.left_term == rule.right_terms[0]:
                        right_term_marked0.append(temp)
                    elif rule.left_term == rule.right_terms[1]:
                        right_term_marked1.append(temp)
                    else:
                        self._marked[rule.left_term].add(temp)
                    # Stop condition, no need to continue
                    if rule.left_term == self._start_variable and len(
                            temp) == 0:
                        need_stop = True
            for temp in right_term_marked1:
                self._marked[rule.right_terms[1]].add(temp)
        for temp in right_term_marked0:
            self._marked[rule.right_terms[0]].add(temp)

        return was_modified, need_stop

    def _production_process(self, rule: ProductionRule) \
            -> Tuple[bool, bool]:
        """Processes a production rule

        Parameters
        ----------
        rule : :class:`~pyformlang.indexed_grammar.ProductionRule`
            The production rule to process
        """
        was_modified = False
        # f_rules contains the consumption rules associated with
        # the current production symbol
        f_rules = self._rules.consumption_rules.setdefault(
            rule.production, [])
        # l_rules contains the left symbol plus what is marked on
        # the right side
        l_temp = [(x.left_term,
                   self._marked[x.right_term]) for x in f_rules]
        marked_symbols = [x.left_term for x in f_rules]
        # Process all combinations of consumption rule
        was_modified |= addrec_bis(l_temp,
                                   self._marked[rule.left_term],
                                   self._marked[rule.right_term])
        # End condition
        if frozenset() in self._marked[self._start_variable]:
            return was_modified, True
        # Is it useful?
        if rule.right_term in marked_symbols:
            for term in [term for term in l_temp
                         if rule.right_term == term[0]]:
                for sub_term in [sub_term
                                 for sub_term in term[1]
                                 if sub_term not in
                                 self._marked[rule.left_term]]:
                    was_modified = True
                    self._marked[rule.left_term].add(sub_term)
                    if (rule.left_term == self._start_variable and
                            len(sub_term) == 0):
                        return was_modified, True
        # Edge case
        if frozenset() in self._marked[rule.right_term]:
            if frozenset() not in self._marked[rule.left_term]:
                was_modified = True
                self._marked[rule.left_term].add(frozenset())
        return was_modified, False

    def is_empty(self) -> bool:
        """Checks whether the grammar generates a word or not

        Returns
        ----------
        is_empty : bool
            Whether the grammar is empty or not
        """
        # To know when no more modification are done
        was_modified = True
        while was_modified:
            was_modified = False
            for rule in self._rules.rules:
                # If we have a duplication rule, we mark all combinations of
                # the sets marked on the right side for the symbol on the left
                # side
                if isinstance(rule, DuplicationRule):
                    dup_res = self._duplication_processing(rule)
                    was_modified |= dup_res[0]
                    if dup_res[1]:
                        return False
                elif isinstance(rule, ProductionRule):
                    prod_res = self._production_process(rule)
                    if prod_res[1]:
                        return False
                    was_modified |= prod_res[0]
        if frozenset() in self._marked[self._start_variable]:
            return False
        return True

    def __bool__(self) -> bool:
        return not self.is_empty()

    def get_reachable_non_terminals(self) -> Set[Variable]:
        """ Get the reachable symbols

        Returns
        ----------
        reachables : set of any
            The reachable symbols from the start state
        """
        # Preprocess
        reachable_from: Dict[Variable, Set[CFGObject]] = {}
        consumption_rules = self._rules.consumption_rules
        for rule in self._rules.rules:
            if isinstance(rule, DuplicationRule):
                left = rule.left_term
                right0 = rule.right_terms[0]
                right1 = rule.right_terms[1]
                if left not in reachable_from:
                    reachable_from[left] = set()
                reachable_from[left].add(right0)
                reachable_from[left].add(right1)
            if isinstance(rule, ProductionRule):
                left = rule.left_term
                right = rule.right_term
                if left not in reachable_from:
                    reachable_from[left] = set()
                reachable_from[left].add(right)
        for key in consumption_rules:
            for rule in consumption_rules[key]:
                left = rule.left_term
                right = rule.right_term
                if left not in reachable_from:
                    reachable_from[left] = set()
                reachable_from[left].add(right)
        # Processing
        to_process = [self._start_variable]
        reachables = {self._start_variable}
        while to_process:
            current = to_process.pop()
            for symbol in reachable_from.get(current, set()):
                if symbol not in reachables:
                    variable = to_variable(symbol)
                    reachables.add(variable)
                    to_process.append(variable)
        return reachables

    def get_generating_non_terminals(self) -> Set[Variable]:
        """ Get the generating symbols

        Returns
        ----------
        generating : set of any
            The generating symbols from the start state
        """
        # Preprocess
        generating_from: Dict[Variable, Set[Variable]] = {}
        duplication_pointer: Dict[CFGObject, List[Tuple[Variable, int]]] = {}
        generating = set()
        to_process = []
        self._preprocess_rules_generating(duplication_pointer, generating,
                                          generating_from, to_process)
        self._preprocess_consumption_rules_generating(generating_from)
        # Processing
        while to_process:
            current = to_process.pop()
            for symbol in generating_from.get(current, []):
                if symbol not in generating:
                    generating.add(symbol)
                    to_process.append(symbol)
            for symbol, pointer in duplication_pointer.get(current, []):
                pointer -= 1
                if pointer == 0:
                    if symbol not in generating:
                        generating.add(symbol)
                        to_process.append(symbol)
        return generating

    def _preprocess_consumption_rules_generating(
            self,
            generating_from: Dict[Variable, Set[Variable]]) \
                -> None:
        for key in self._rules.consumption_rules:
            for rule in self._rules.consumption_rules[key]:
                left = rule.left_term
                right = rule.right_term
                if right in generating_from:
                    generating_from[right].add(left)
                else:
                    generating_from[right] = {left}

    def _preprocess_rules_generating(
        self,
        duplication_pointer: Dict[CFGObject, List[Tuple[Variable, int]]],
        generating: Set[Variable],
        generating_from: Dict[Variable, Set[Variable]],
        to_process: List[Variable]) \
            -> None:
        for rule in self._rules.rules:
            if isinstance(rule, DuplicationRule):
                left = rule.left_term
                right0 = rule.right_terms[0]
                right1 = rule.right_terms[1]
                temp = (left, 2)
                duplication_pointer.setdefault(right0, []).append(temp)
                duplication_pointer.setdefault(right1, []).append(temp)
            if isinstance(rule, ProductionRule):
                left = rule.left_term
                right = rule.right_term
                if right in generating_from:
                    generating_from[right].add(left)
                else:
                    generating_from[right] = {left}
            if isinstance(rule, EndRule):
                left = rule.left_term
                if left not in generating:
                    generating.add(left)
                    to_process.append(left)

    def remove_useless_rules(self) -> "IndexedGrammar":
        """ Remove useless rules in the grammar

        More precisely, we remove rules which do not contain only generating \
        or  reachable non terminals.

        Returns
        ----------
        i_grammar : :class:`~pyformlang.indexed_grammar.IndexedGrammar`
            The indexed grammar which useless rules
        """
        l_rules = []
        generating = self.get_generating_non_terminals()
        reachables = self.get_reachable_non_terminals()
        consumption_rules = self._rules.consumption_rules
        for rule in self._rules.rules:
            if isinstance(rule, DuplicationRule):
                left = rule.left_term
                right0 = rule.right_terms[0]
                right1 = rule.right_terms[1]
                if all(x in generating and x in reachables for x in
                       [left, right0, right1]):
                    l_rules.append(rule)
            if isinstance(rule, ProductionRule):
                left = rule.left_term
                right = rule.right_term
                if all(x in generating and x in reachables for x in
                       [left, right]):
                    l_rules.append(rule)
            if isinstance(rule, EndRule):
                left = rule.left_term
                if left in generating and left in reachables:
                    l_rules.append(rule)
        for key in consumption_rules:
            for rule in consumption_rules[key]:
                left = rule.left_term
                right = rule.right_term
                if all(x in generating and x in reachables for x in
                       [left, right]):
                    l_rules.append(rule)
        rules = Rules(l_rules, self._rules.optim)
        return IndexedGrammar(rules)

    def intersection(self, other: Any) -> "IndexedGrammar":
        """ Computes the intersection of the current indexed grammar with the \
        other object

        Equivalent to
        --------------
          >> indexed_grammar and regex

        Parameters
        ----------
        other : any
            The object to intersect with

        Returns
        ----------
        i_grammar : :class:`~pyformlang.indexed_grammar.IndexedGrammar`
            The indexed grammar which useless rules

        Raises
        ------
        NotImplementedError
            When trying to intersection with something else than a regular
            expression or a finite automaton
        """
        if isinstance(other, Regex):
            other = other.to_epsilon_nfa()
        if isinstance(other, FiniteAutomaton):
            fst = other.to_fst()
            return fst.intersection(self)
        raise NotImplementedError

    def __and__(self, other: Any) -> "IndexedGrammar":
        """ Computes the intersection of the current indexed grammar with the
        other object

        Parameters
        ----------
        other : any
            The object to intersect with

        Returns
        ----------
        i_grammar : :class:`~pyformlang.indexed_grammar.IndexedGrammar`
            The indexed grammar which useless rules
        """
        return self.intersection(other)
