""" A context free grammar """

from string import ascii_uppercase
from copy import deepcopy
from typing import Dict, List, Set, AbstractSet, Iterable, Tuple, Hashable

from networkx import DiGraph, find_cycle
from networkx.exception import NetworkXNoCycle

from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State

from .formal_grammar import FormalGrammar
from .parse_tree import ParseTree
from .cyk_table import CYKTable
from .cfg_variable_converter import CFGVariableConverter
from .utils import remove_nullable_production, get_productions_d, \
    is_special_text
from ..objects.cfg_objects import CFGObject, \
    Variable, Terminal, Epsilon, Production
from ..objects.cfg_objects.utils import to_variable, to_terminal

EPSILON_SYMBOLS = ["epsilon", "$", "ε", "ϵ", "Є"]

SUBS_SUFFIX = "#SUBS#"


class CFG(FormalGrammar):
    """ A class representing a context free grammar

    Parameters
    ----------
    variables : set of :class:`~pyformlang.cfg.Variable`, optional
        The variables of the CFG
    terminals : set of :class:`~pyformlang.cfg.Terminal`, optional
        The terminals of the CFG
    start_symbol : :class:`~pyformlang.cfg.Variable`, optional
        The start symbol
    productions : set of :class:`~pyformlang.cfg.Production`, optional
        The productions or rules of the CFG
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self,
                 variables: AbstractSet[Hashable] = None,
                 terminals: AbstractSet[Hashable] = None,
                 start_symbol: Hashable = None,
                 productions: Iterable[Production] = None) -> None:
        super().__init__()
        if variables is not None:
            variables = {to_variable(x) for x in variables}
        self._variables = variables or set()
        if terminals is not None:
            terminals = {to_terminal(x) for x in terminals}
        self._terminals = terminals or set()
        if start_symbol is not None:
            start_symbol = to_variable(start_symbol)
            self._variables.add(start_symbol)
        self._start_symbol = start_symbol
        if productions is not None:
            productions = set(productions)
        self._productions = productions or set()
        for production in self._productions:
            self.__initialize_production_in_cfg(production)
        self._impacts: Dict[CFGObject, List[Tuple[CFGObject, int]]] = {}
        self._remaining_lists: Dict[CFGObject, List[int]] = {}
        self._added_impacts: Set[CFGObject] = set()

    def __initialize_production_in_cfg(self, production: Production) -> None:
        self._variables.add(production.head)
        for cfg_object in production.body:
            if isinstance(cfg_object, Terminal):
                self._terminals.add(cfg_object)
            elif isinstance(cfg_object, Variable):
                self._variables.add(cfg_object)

    def get_generating_symbols(self) -> Set[CFGObject]:
        """ Gives the objects which are generating in the CFG

        Returns
        ----------
        generating_symbols : set of :class:`~pyformlang.cfg.CFGObject`
            The generating symbols of the CFG
        """
        return self._get_generating_or_nullable(False)

    def get_nullable_symbols(self) -> Set[CFGObject]:
        """ Gives the objects which are nullable in the CFG

        Returns
        ----------
        nullable_symbols : set of :class:`~pyformlang.cfg.CFGObject`
            The nullable symbols of the CFG
        """
        return self._get_generating_or_nullable(True)

    def _get_generating_or_nullable(self, nullable: bool = False) \
            -> Set[CFGObject]:
        """ Merge of nullable and generating """
        to_process: List[CFGObject] = [Epsilon()]
        g_symbols: Set[CFGObject] = {Epsilon()}

        self._set_impacts_and_remaining_lists()

        for symbol in self._added_impacts:
            if symbol not in g_symbols:
                g_symbols.add(symbol)
                to_process.append(symbol)

        if not nullable:
            for terminal in self._terminals:
                g_symbols.add(terminal)
                to_process.append(terminal)

        processed_with_modification = []
        while to_process:
            current = to_process.pop()
            for symbol_impact, index_impact in self._impacts.get(current, []):
                if symbol_impact in g_symbols:
                    continue
                processed_with_modification.append(
                    (symbol_impact, index_impact))
                self._remaining_lists[symbol_impact][index_impact] -= 1
                if self._remaining_lists[symbol_impact][index_impact] == 0:
                    g_symbols.add(symbol_impact)
                    to_process.append(symbol_impact)
        # Fix modifications
        for symbol_impact, index_impact in processed_with_modification:
            self._remaining_lists[symbol_impact][index_impact] += 1
        g_symbols.remove(Epsilon())
        return g_symbols

    def _set_impacts_and_remaining_lists(self) -> None:
        if self._impacts:
            return
        self._added_impacts = set()
        self._remaining_lists = {}
        self._impacts = {}
        for production in self._productions:
            head = production.head  # Should check if head is not Epsilon?
            body = production.body
            if not body:
                self._added_impacts.add(head)
                continue
            temp = self._remaining_lists.setdefault(head, [])
            temp.append(len(body))
            index_impact = len(temp) - 1
            for symbol in body:
                self._impacts.setdefault(symbol, []).append(
                    (head, index_impact))

    def generate_epsilon(self) -> bool:
        """ Whether the grammar generates epsilon or not

        Returns
        ----------
        generate_epsilon : bool
            Whether epsilon is generated or not by the CFG
        """
        generate_epsilon: Set[CFGObject] = {Epsilon()}
        to_process: List[CFGObject] = [Epsilon()]

        self._set_impacts_and_remaining_lists()

        for symbol in self._added_impacts:
            if symbol == self._start_symbol:
                return True
            if symbol not in generate_epsilon:
                generate_epsilon.add(symbol)
                to_process.append(symbol)
        remaining_lists = self._remaining_lists
        impacts = self._impacts
        remaining_lists = deepcopy(remaining_lists)

        while to_process:
            current = to_process.pop()
            for symbol_impact, index_impact in impacts.get(current, []):
                if symbol_impact in generate_epsilon:
                    continue
                remaining_lists[symbol_impact][index_impact] -= 1
                if remaining_lists[symbol_impact][index_impact] == 0:
                    if symbol_impact == self._start_symbol:
                        return True
                    generate_epsilon.add(symbol_impact)
                    to_process.append(symbol_impact)
        return False

    def get_reachable_symbols(self) -> Set[CFGObject]:
        """ Gives the objects which are reachable in the CFG

        Returns
        ----------
        reachable_symbols : set of :class:`~pyformlang.cfg.CFGObject`
            The reachable symbols of the CFG
        """
        if not self.start_symbol:
            return set()
        r_symbols: Set[CFGObject] = set()
        r_symbols.add(self.start_symbol)
        reachable_transition_d = {}
        for production in self._productions:
            temp = reachable_transition_d.setdefault(production.head, [])
            for symbol in production.body:
                if not isinstance(symbol, Epsilon):
                    temp.append(symbol)
        to_process = [self._start_symbol]
        while to_process:
            current = to_process.pop()
            for next_symbol in reachable_transition_d.get(current, []):
                if next_symbol not in r_symbols:
                    r_symbols.add(next_symbol)
                    to_process.append(next_symbol)
        return r_symbols

    def remove_useless_symbols(self) -> "CFG":
        """ Removes useless symbols in a CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG without useless symbols
        """
        generating = self.get_generating_symbols()
        productions = [x for x in self._productions
                       if x.head in generating and
                       all(y in generating for y in x.body)]
        new_var = self._variables.intersection(generating)
        new_ter = self._terminals.intersection(generating)
        cfg_temp = CFG(new_var, new_ter, self._start_symbol, productions)
        reachables = cfg_temp.get_reachable_symbols()
        productions = [x for x in productions
                       if x.head in reachables]
        new_var = new_var.intersection(reachables)
        new_ter = new_ter.intersection(reachables)
        return CFG(new_var, new_ter, self._start_symbol, productions)

    def remove_epsilon(self) -> "CFG":
        """ Removes the epsilon of a cfg

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG without epsilons
        """
        new_productions = []
        nullables = self.get_nullable_symbols()
        for production in self._productions:
            new_productions += remove_nullable_production(production,
                                                          nullables)
        return CFG(self._variables,
                   self._terminals,
                   self._start_symbol,
                   new_productions)

    def get_unit_pairs(self) -> Set[Tuple[Variable, Variable]]:
        """ Finds all the unit pairs

        Returns
        ----------
        unit_pairs : set of tuple of :class:`~pyformlang.cfg.Variable`
            The unit pairs
        """
        unit_pairs = set()
        for variable in self._variables:
            unit_pairs.add((variable, variable))
        productions = [x
                       for x in self._productions
                       if len(x.body) == 1 and isinstance(x.body[0], Variable)]
        productions_d = get_productions_d(productions)
        to_process = list(unit_pairs)
        while to_process:
            var_a, var_b = to_process.pop()
            for production in productions_d.get(var_b, []):
                temp = (var_a, production.body[0])
                if temp not in unit_pairs:
                    unit_pairs.add(temp)
                    to_process.append(temp)
        return unit_pairs

    def eliminate_unit_productions(self) -> "CFG":
        """ Eliminate all the unit production in the CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            A new CFG equivalent without unit productions
        """
        unit_pairs = self.get_unit_pairs()
        productions = [x
                       for x in self._productions
                       if len(x.body) != 1
                       or not isinstance(x.body[0], Variable)]
        productions_d = get_productions_d(productions)
        for var_a, var_b in unit_pairs:
            for production in productions_d.get(var_b, []):
                productions.append(Production(var_a, production.body,
                                              filtering=False))
        return CFG(self._variables,
                   self._terminals,
                   self._start_symbol,
                   productions)

    def _get_productions_with_only_single_terminals(self) -> List[Production]:
        """ Remove the terminals involved in a body of length more than 1 """
        term_to_var = {}
        new_productions = []
        for terminal in self._terminals:
            var = Variable(str(terminal.value) + "#CNF#")
            term_to_var[terminal] = var
        # We want to add only the useful productions
        used = set()
        for production in self._productions:
            if len(production.body) == 1:
                new_productions.append(production)
                continue
            new_body = []
            for symbol in production.body:
                if symbol in term_to_var:
                    new_body.append(term_to_var[symbol])
                    used.add(symbol)
                else:
                    new_body.append(symbol)
            new_productions.append(Production(production.head,
                                              new_body))
        for terminal in used:
            new_productions.append(
                Production(term_to_var[terminal], [terminal]))
        return new_productions

    def _get_next_free_variable(self, idx: int, prefix: str) \
            -> Tuple[int, Variable]:
        idx += 1
        temp = Variable(prefix + str(idx))
        while temp in self._variables:
            idx += 1
            temp = Variable(prefix + str(idx))
        return idx, temp

    def _decompose_productions(self, productions: Iterable[Production]) \
            -> List[Production]:
        """ Decompose productions """
        idx = 0
        new_productions = []
        done = {}
        for production in productions:
            body = production.body
            if len(body) <= 2:
                new_productions.append(production)
                continue
            new_var = []
            for _ in range(len(body) - 2):
                idx, var = self._get_next_free_variable(idx, "C#CNF#")
                new_var.append(var)
            head = production.head
            stopped = False
            for i in range(len(body) - 2):
                temp = tuple(body[i + 1:])
                if temp in done:
                    new_productions.append(Production(head,
                                                      [body[i], done[temp]]))
                    stopped = True
                    break
                new_productions.append(Production(head, [body[i], new_var[i]]))
                done[temp] = new_var[i]
                head = new_var[i]
            if not stopped:
                new_productions.append(Production(head, [body[-2], body[-1]]))
        return new_productions

    def to_normal_form(self) -> "CFG":
        """ Gets the Chomsky Normal Form of a CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            A new CFG equivalent in the CNF form

        Warnings
        ---------
        As described in Hopcroft's textbook, a normal form does not generate \
        the epsilon word. So, the grammar generated by this function is \
        equivalent to the original grammar except if this grammar generates \
        the epsilon word. In that case, the language of the generated grammar \
        contains the same word as before, except the epsilon word.

        """
        nullables = self.get_nullable_symbols()
        unit_pairs = self.get_unit_pairs()
        generating = self.get_generating_symbols()
        reachables = self.get_reachable_symbols()
        if (len(nullables) != 0 or len(unit_pairs) != len(self._variables) or
                len(generating) !=
                len(self._variables) + len(self._terminals) or
                len(reachables) !=
                len(self._variables) + len(self._terminals)):
            if len(self._productions) == 0:
                return self
            new_cfg = self.remove_useless_symbols() \
                .remove_epsilon() \
                .remove_useless_symbols() \
                .eliminate_unit_productions() \
                .remove_useless_symbols()
            return new_cfg.to_normal_form()
        # Remove terminals from body
        new_productions = self._get_productions_with_only_single_terminals()
        new_productions = self._decompose_productions(new_productions)
        return CFG(start_symbol=self._start_symbol,
                   productions=set(new_productions))

    def substitute(self, substitution: Dict[Terminal, "CFG"]) -> "CFG":
        """ Substitutes CFG to terminals in the current CFG

        Parameters
        -----------
        substitution : dict of :class:`~pyformlang.cfg.Terminal` to \
        :class:`~pyformlang.cfg.CFG`
            A substitution

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            A new CFG recognizing the substitution
        """
        idx = 0
        new_variables_d = {}
        new_vars = set()
        for variable in self._variables:
            temp = Variable(str(variable) + SUBS_SUFFIX + str(idx))
            new_variables_d[variable] = temp
            new_vars.add(temp)
            idx += 1
        productions = []
        terminals = self._terminals.copy()
        final_replacement = {}
        for ter, cfg in substitution.items():
            new_variables_d_local = {}
            for variable in cfg.variables:
                temp = Variable(str(variable) + SUBS_SUFFIX + str(idx))
                new_variables_d_local[variable] = temp
                new_vars.add(temp)
                idx += 1
            # Add rules of the new cfg
            for production in cfg.productions:
                body = []
                for cfg_obj in production.body:
                    if cfg_obj in new_variables_d_local:
                        body.append(new_variables_d_local[cfg_obj])
                    else:
                        body.append(cfg_obj)
                productions.append(
                    Production(new_variables_d_local[production.head],
                               body))
            final_replacement[ter] = new_variables_d_local[cfg.start_symbol]
            terminals = terminals.union(cfg.terminals)
        for production in self._productions:
            body = []
            for cfg_obj in production.body:
                if cfg_obj in new_variables_d:
                    body.append(new_variables_d[cfg_obj])
                elif cfg_obj in final_replacement:
                    body.append(final_replacement[cfg_obj])
                else:
                    body.append(cfg_obj)
            productions.append(Production(new_variables_d[production.head],
                                          body))
        return CFG(new_vars, None, new_variables_d[self._start_symbol],
                   set(productions))

    def union(self, other: "CFG") -> "CFG":
        """ Makes the union of two CFGs

        Equivalent to:
          >> cfg0 or cfg1

        Parameters
        ----------
        other : :class:`~pyformlang.cfg.CFG`
            The other CFG to unite with

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG resulting of the union of the two CFGs
        """
        start_temp = Variable("#STARTUNION#")
        temp_0 = Terminal("#0UNION#")
        temp_1 = Terminal("#1UNION#")
        production_0 = Production(start_temp, [temp_0])
        production_1 = Production(start_temp, [temp_1])
        cfg_temp = CFG({start_temp},
                       {temp_0, temp_1},
                       start_temp,
                       {production_0, production_1})
        return cfg_temp.substitute({temp_0: self,
                                    temp_1: other})

    def __or__(self, other: "CFG") -> "CFG":
        """ Makes the union of two CFGs

        Parameters
        ----------
        other : :class:`~pyformlang.cfg.CFG`
            The other CFG to unite with

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG resulting of the union of the two CFGs
        """
        return self.union(other)

    def concatenate(self, other: "CFG") -> "CFG":
        """ Makes the concatenation of two CFGs

        Equivalent to:
          >> cfg0 + cfg1

        Parameters
        ----------
        other : :class:`~pyformlang.cfg.CFG`
            The other CFG to concatenate with

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG resulting of the concatenation of the two CFGs
        """
        start_temp = Variable("#STARTCONC#")
        temp_0 = Terminal("#0CONC#")
        temp_1 = Terminal("#1CONC#")
        production0 = Production(start_temp, [temp_0, temp_1])
        cfg_temp = CFG({start_temp},
                       {temp_0, temp_1},
                       start_temp,
                       {production0})
        return cfg_temp.substitute({temp_0: self,
                                    temp_1: other})

    def __add__(self, other: "CFG") -> "CFG":
        """ Makes the concatenation of two CFGs

        Parameters
        ----------
        other : :class:`~pyformlang.cfg.CFG`
            The other CFG to concatenate with

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG resulting of the concatenation of the two CFGs
        """
        return self.concatenate(other)

    def get_closure(self) -> "CFG":
        """ Gets the closure of the CFG (*)

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The closure of the current CFG
        """
        start_temp = Variable("#STARTCLOS#")
        temp_1 = Terminal("#1CLOS#")
        production0 = Production(start_temp, [temp_1])
        production1 = Production(start_temp, [start_temp, start_temp])
        production2 = Production(start_temp, [])
        cfg_temp = CFG({start_temp},
                       {temp_1},
                       start_temp,
                       {production0, production1, production2})
        return cfg_temp.substitute({temp_1: self})

    def get_positive_closure(self) -> "CFG":
        """ Gets the positive closure of the CFG (+)

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The positive closure of the current CFG
        """
        start_temp = Variable("#STARTPOSCLOS#")
        var_temp = Variable("#VARPOSCLOS#")
        temp_1 = Terminal("#1POSCLOS#")
        production0 = Production(start_temp, [temp_1, var_temp])
        production1 = Production(var_temp, [var_temp, var_temp])
        production2 = Production(var_temp, [temp_1])
        production3 = Production(var_temp, [])
        cfg_temp = CFG({start_temp, var_temp},
                       {temp_1},
                       start_temp,
                       {production0, production1, production2, production3})
        return cfg_temp.substitute({temp_1: self})

    def reverse(self) -> "CFG":
        """ Reverse the current CFG

        Equivalent to:
            >> ~cfg

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            Reverse the current CFG
        """
        productions = []
        for production in self._productions:
            productions.append(Production(production.head,
                                          production.body[::-1]))
        return CFG(self.variables,
                   self.terminals,
                   self.start_symbol,
                   productions)

    def __invert__(self) -> "CFG":
        """ Reverse the current CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            Reverse the current CFG
        """
        return self.reverse()

    def is_empty(self) -> bool:
        """ Says whether the CFG is empty or not

        Returns
        ----------
        is_empty : bool
            Whether the CFG is empty or not

        TODO
        ----------
        Can be optimized
        """
        return self._start_symbol not in self.get_generating_symbols()

    def __bool__(self) -> bool:
        return not self.is_empty()

    def contains(self, word: Iterable[Hashable]) -> bool:
        """ Gives the membership of a word to the grammar

        Parameters
        ----------
        word : iterable of :class:`~pyformlang.cfg.Terminal`
            The word to check

        Returns
        ----------
        contains : bool
            Whether word if in the CFG or not
        """
        # Remove epsilons
        word = [to_terminal(x) for x in word if x != Epsilon()]
        cyk_table = CYKTable(self, word)
        return cyk_table.generate_word()

    def __contains__(self, word: Iterable[Hashable]) -> bool:
        return self.contains(word)

    def get_cnf_parse_tree(self, word: Iterable[Hashable]) -> ParseTree:
        """
        Get a parse tree of the CNF of this grammar

        Parameters
        ----------
        word : iterable of :class:`~pyformlang.cfg.Terminal`
            The word to look for

        Returns
        -------
        derivation : :class:`~pyformlang.cfg.ParseTree`
            The parse tree

        """
        word = [to_terminal(x) for x in word if x != Epsilon()]
        cyk_table = CYKTable(self, word)
        return cyk_table.get_parse_tree()

    def intersection(self, other: DeterministicFiniteAutomaton) -> "CFG":
        """ Gives the intersection of the current CFG with an other object

        Equivalent to:
          >> cfg and regex

        Parameters
        ----------
        other : any
            The other object

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            A CFG representing the intersection with the other object

        Raises
        ----------
        NotImplementedError
            When trying to intersect with something else than a regex or a
            finite automaton
        """
        if self.is_empty() or other.is_empty():
            return CFG()
        generate_empty = self.contains([]) and other.accepts([])
        cfg = self.to_normal_form()
        states = set(other.states)
        cv_converter = CFGVariableConverter(states, cfg.variables)
        new_productions = []
        for production in cfg.productions:
            if len(production.body) == 2:
                new_productions += self._intersection_when_two_non_terminals(
                    production, states, cv_converter)
            else:
                new_productions += self._intersection_when_terminal(
                    other,
                    production,
                    states,
                    cv_converter)
        start = Variable("Start")
        new_productions += self._intersection_starting_rules(cfg,
                                                             start,
                                                             other,
                                                             cv_converter)
        if generate_empty:
            new_productions.append(Production(start, []))
        res_cfg = CFG(start_symbol=start, productions=new_productions)
        return res_cfg

    @staticmethod
    def _intersection_starting_rules(
        cfg: "CFG",
        start: Variable,
        other: DeterministicFiniteAutomaton,
        cv_converter: CFGVariableConverter) \
            -> List[Production]:
        if not cfg.start_symbol or not other.start_state:
            return []
        return [Production(start,
                           [cv_converter.to_cfg_combined_variable(
                               other.start_state,
                               cfg.start_symbol,
                               final_state)])
                for final_state in other.final_states]

    @staticmethod
    def _intersection_when_terminal(
        other: DeterministicFiniteAutomaton,
        production: Production,
        states: Iterable[State],
        cv_converter: CFGVariableConverter) \
            -> List[Production]:
        productions_temp = []
        for state_p in states:
            next_state = other.get_next_state(state_p, production.body[0].value)
            if next_state:
                new_head = cv_converter.to_cfg_combined_variable(
                    state_p, production.head, next_state)
                productions_temp.append(
                    Production(new_head,
                               [production.body[0]],
                               filtering=False))
        return productions_temp

    @staticmethod
    def _intersection_when_two_non_terminals(
        production: Production,
        states: Iterable[State],
        cv_converter: CFGVariableConverter) \
            -> List[Production]:
        productions_temp = []
        for state_p in states:
            for state_r in states:
                bodies = CFG._get_all_bodies(production,
                                             state_p, state_r,
                                             states, cv_converter)
                new_head = cv_converter.to_cfg_combined_variable(
                    state_p, production.head, state_r)
                productions_temp += [Production(new_head,
                                                body,
                                                filtering=False)
                                     for body in bodies]
        return productions_temp

    @staticmethod
    def _get_all_bodies(production: Production,
                        state_p: State,
                        state_r: State,
                        states: Iterable[State],
                        cv_converter: CFGVariableConverter) \
                            -> List[List[CFGObject]]:
        return [
            [cv_converter.to_cfg_combined_variable(
                state_p,
                production.body[0],
                state_q),
             cv_converter.to_cfg_combined_variable(
                 state_q,
                 production.body[1],
                 state_r)]
            for state_q in states]

    def __and__(self, other: DeterministicFiniteAutomaton) -> "CFG":
        """ Gives the intersection of the current CFG with an other object

        Parameters
        ----------
        other : any
            The other object

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            A CFG representing the intersection with the other object

        Raises
        ----------
        """
        return self.intersection(other)

    def get_words(self, max_length: int = -1) -> Iterable[List[Terminal]]:
        """ Get the words generated by the CFG

        Parameters
        ----------
        max_length : int
            The maximum length of the words to return
        """
        nullables = self.get_nullable_symbols()
        if self.start_symbol in nullables:
            yield []
        if max_length == 0:
            return
        cfg = self.to_normal_form()
        productions = cfg.productions
        gen_d: Dict[CFGObject, List[List[List[Terminal]]]] = {}
        # Look for Epsilon Transitions
        for production in productions:
            if production.head not in gen_d:
                gen_d[production.head] = [[]]
            if len(production.body) == 2:
                for obj in production.body:
                    if obj not in gen_d:
                        gen_d[obj] = [[]]
        # To a single terminal
        for production in productions:
            body = production.body
            if len(body) == 1 and isinstance(body[0], Terminal):
                if len(gen_d[production.head]) == 1:
                    gen_d[production.head].append([])
                if [body[0]] not in gen_d[production.head][-1]:
                    gen_d[production.head][-1].append([body[0]])
                    if production.head == cfg.start_symbol:
                        yield [body[0]]
        # Complete what is missing
        current_length = 2
        total_no_modification = 0
        while current_length <= max_length or max_length == -1:
            was_modified = False
            for gen in gen_d.values():
                if len(gen) != current_length:
                    gen.append([])
            for production in productions:
                body = production.body
                if len(gen_d[production.head]) != current_length + 1:
                    gen_d[production.head].append([])
                if len(body) != 2:
                    continue
                for i in range(1, current_length):
                    j = current_length - i
                    for left in gen_d[body[0]][i]:
                        for right in gen_d[body[1]][j]:
                            new_word = left + right
                            if new_word not in gen_d[production.head][-1]:
                                was_modified = True
                                gen_d[production.head][-1].append(new_word)
                                if production.head == cfg.start_symbol:
                                    yield new_word
            if was_modified:
                total_no_modification = 0
            else:
                total_no_modification += 1
            current_length += 1
            if total_no_modification > current_length / 2:
                return

    def is_finite(self) -> bool:
        """ Tests if the grammar is finite or not

        Returns
        ----------
        is_finite : bool
            Whether the grammar is finite or not
        """
        normal = self.to_normal_form()
        di_graph = DiGraph()
        for production in normal.productions:
            body = production.body
            if len(body) == 2:
                di_graph.add_edge(production.head, body[0])
                di_graph.add_edge(production.head, body[1])
        try:
            find_cycle(di_graph, orientation="original")
        except NetworkXNoCycle:
            return True
        return False

    def copy(self) -> "CFG":
        """ Copies the Context Free Grammar """
        return CFG._copy_from(self)

    @classmethod
    def _read_line(cls,
                   line: str,
                   productions: Set[Production],
                   terminals: Set[Terminal],
                   variables: Set[Variable]) -> None:
        head_s, body_s = line.split("->")
        head_text = head_s.strip()
        if is_special_text(head_text):
            head_text = head_text[5:-1]
        head = Variable(head_text)
        variables.add(head)
        for sub_body in body_s.split("|"):
            body = []
            for body_component in sub_body.split():
                if is_special_text(body_component):
                    type_component = body_component[1:4]
                    body_component = body_component[5:-1]
                else:
                    type_component = ""
                if body_component[0] in ascii_uppercase or \
                        type_component == "VAR":
                    body_var = Variable(body_component)
                    variables.add(body_var)
                    body.append(body_var)
                elif body_component not in EPSILON_SYMBOLS or type_component \
                        == "TER":
                    body_ter = Terminal(body_component)
                    terminals.add(body_ter)
                    body.append(body_ter)
            productions.add(Production(head, body))
