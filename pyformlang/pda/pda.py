""" We represent here a push-down automaton """

from typing import Dict, List, Set, AbstractSet, \
    Iterator, Iterable, Tuple, Type, Optional, Hashable, Any
from json import dumps, loads
from itertools import product
from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import write_dot

from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import Symbol as FASymbol
from pyformlang.finite_automaton import Epsilon as FAEpsilon
from pyformlang.cfg import CFG, CFGObject, Variable, Terminal, Production
from pyformlang.cfg.cfg_variable_converter import CFGVariableConverter

from .transition_function import TransitionFunction
from .transition_function import TransitionKey, TransitionValues, Transition
from .utils import PDAStateConverter, PDASymbolConverter
from ..objects.pda_objects import State, StackSymbol
from ..objects.pda_objects import Symbol as PDASymbol
from ..objects.pda_objects import Epsilon as PDAEpsilon
from ..objects.pda_objects.utils import to_state, to_symbol, to_stack_symbol

INPUT_SYMBOL = 1

STACK_FROM = 2

INPUT = 0

STATE = 0

NEW_STACK = 1

OUTPUT = 1

InputTransition = Tuple[Hashable, Hashable, Hashable,
                        Hashable, Iterable[Hashable]]


class PDA(Iterable[Transition]):
    """ Representation of a pushdown automaton

    Parameters
    ----------
    states : set of :class:`~pyformlang.pda.State`, optional
        A finite set of states
    input_symbols : set of :class:`~pyformlang.pda.Symbol`, optional
        A finite set of input symbols
    stack_alphabet : set of :class:`~pyformlang.pda.StackSymbol`, optional
        A finite stack alphabet
    transition_function : :class:`~pyformlang.pda.TransitionFunction`, optional
        Takes as arguments a state, an input symbol and a stack symbol and
        returns a state and a string of stack symbols push on the stacked to
        replace X
    start_state : :class:`~pyformlang.pda.State`, optional
        A start state, element of states
    start_stack_symbol : :class:`~pyformlang.pda.StackSymbol`, optional
        The stack is initialized with this stack symbol
    final_states : set of :class:`~pyformlang.pda.State`, optional
        A set of final or accepting states. It is a subset of states.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self,
                 states: AbstractSet[Hashable] = None,
                 input_symbols: AbstractSet[Hashable] = None,
                 stack_alphabet: AbstractSet[Hashable] = None,
                 transition_function: TransitionFunction = None,
                 start_state: Hashable = None,
                 start_stack_symbol: Hashable = None,
                 final_states: AbstractSet[Hashable] = None):
        # pylint: disable=too-many-arguments
        if states is not None:
            states = {to_state(x) for x in states}
        if input_symbols is not None:
            input_symbols = {to_symbol(x) for x in input_symbols}
        if stack_alphabet is not None:
            stack_alphabet = {to_stack_symbol(x) for x in stack_alphabet}
        if start_state is not None:
            start_state = to_state(start_state)
        if start_stack_symbol is not None:
            start_stack_symbol = to_stack_symbol(start_stack_symbol)
        if final_states is not None:
            final_states = {to_state(x) for x in final_states}
        self._states: Set[State] = states or set()
        self._input_symbols: Set[PDASymbol] = input_symbols or set()
        self._stack_alphabet: Set[StackSymbol] = stack_alphabet or set()
        self._transition_function = transition_function or TransitionFunction()
        self._start_state: Optional[State] = start_state
        if start_state is not None:
            self._states.add(start_state)
        self._start_stack_symbol: Optional[StackSymbol] = start_stack_symbol
        if start_stack_symbol is not None:
            self._stack_alphabet.add(start_stack_symbol)
        self._final_states: Set[State] = final_states or set()
        for state in self._final_states:
            self._states.add(state)

    @property
    def states(self) -> Set[State]:
        """
        Get the states fo the PDA
        Returns
        -------
        states : iterable of :class:`~pyformlang.pda.State`
            The states of the PDA
        """
        return self._states

    @property
    def input_symbols(self) -> Set[PDASymbol]:
        """
        The input symbols of the PDA

        Returns
        -------
        input_symbols : iterable of :class:`~pyformlang.pda.Symbol`
            The input symbols of the PDA
        """
        return self._input_symbols

    @property
    def stack_symbols(self) -> Set[StackSymbol]:
        """
        The stack symbols of the PDA

        Returns
        -------
        stack_symbols : iterable of :class:`~pyformlang.pda.StackSymbol`
            The stack symbols of the PDA
        """
        return self._stack_alphabet

    @property
    def start_state(self) -> Optional[State]:
        """ Get start state """
        return self._start_state

    @property
    def start_stack_symbol(self) -> Optional[StackSymbol]:
        """ Get start stack symbol """
        return self._start_stack_symbol

    @property
    def final_states(self) -> Set[State]:
        """
        The final states of the PDA
        Returns
        -------
        final_states : iterable of :class:`~pyformlang.pda.State`
            The final states of the PDA

        """
        return self._final_states

    def set_start_state(self, start_state: Hashable) -> None:
        """ Sets the start state to the automaton

        Parameters
        ----------
        start_state : :class:`~pyformlang.pda.State`
            The start state
        """
        start_state = to_state(start_state)
        self._states.add(start_state)
        self._start_state = start_state

    def set_start_stack_symbol(self, start_stack_symbol: Hashable) -> None:
        """ Sets the start stack symbol to the automaton

        Parameters
        ----------
        start_stack_symbol : :class:`~pyformlang.pda.StackSymbol`
            The start stack symbol
        """
        start_stack_symbol = to_stack_symbol(start_stack_symbol)
        self._stack_alphabet.add(start_stack_symbol)
        self._start_stack_symbol = start_stack_symbol

    def add_final_state(self, state: Hashable) -> None:
        """ Adds a final state to the automaton

        Parameters
        ----------
        state : :class:`~pyformlang.pda.State`
            The state to add
        """
        state = to_state(state)
        self._final_states.add(state)

    def get_number_transitions(self) -> int:
        """ Gets the number of transitions in the PDA

        Returns
        ----------
        n_transitions : int
            The number of transitions
        """
        return self._transition_function.get_number_transitions()

    def add_transition(self,
                       s_from: Hashable,
                       input_symbol: Hashable,
                       stack_from: Hashable,
                       s_to: Hashable,
                       stack_to: Iterable[Hashable]) -> None:
        """ Add a transition to the PDA

        Parameters
        ----------
        s_from : :class:`~pyformlang.pda.State`
            The starting symbol
        input_symbol : :class:`~pyformlang.pda.Symbol`
            The input symbol for the transition
        stack_from : :class:`~pyformlang.pda.StackSymbol`
            The stack symbol of the transition
        s_to : :class:`~pyformlang.pda.State`
            The new state
        stack_to : list of :class:`~pyformlang.pda.StackSymbol`
            The string of stack symbol which replace the stack_from
        """
        # pylint: disable=too-many-arguments
        s_from = to_state(s_from)
        input_symbol = to_symbol(input_symbol)
        stack_from = to_stack_symbol(stack_from)
        s_to = to_state(s_to)
        stack_to = tuple(to_stack_symbol(x) for x in stack_to)
        self._states.add(s_from)
        self._states.add(s_to)
        if input_symbol != PDAEpsilon():
            self._input_symbols.add(input_symbol)
        self._stack_alphabet.add(stack_from)
        for stack_symbol in stack_to:
            if stack_symbol != PDAEpsilon():
                self._stack_alphabet.add(stack_symbol)
        self._transition_function.add_transition(s_from,
                                                 input_symbol,
                                                 stack_from,
                                                 s_to,
                                                 stack_to)

    def add_transitions(self, transitions: Iterable[InputTransition]) -> None:
        """
        Adds several transitions

        Parameters
        ----------
        transitions :
            Transitions as they would be given to add_transition
        """
        for s_from, input_symbol, stack_from, s_to, stack_to in transitions:
            self.add_transition(s_from, input_symbol, stack_from,
                                s_to, stack_to)

    def remove_transition(self,
                          s_from: Hashable,
                          input_symbol: Hashable,
                          stack_from: Hashable,
                          s_to: Hashable,
                          stack_to: Iterable[Hashable]) -> None:
        """ Remove the given transition from the PDA """
        s_from = to_state(s_from)
        input_symbol = to_symbol(input_symbol)
        stack_from = to_stack_symbol(stack_from)
        s_to = to_state(s_to)
        stack_to = tuple(to_stack_symbol(x) for x in stack_to)
        self._transition_function.remove_transition(s_from,
                                                    input_symbol,
                                                    stack_from,
                                                    s_to,
                                                    stack_to)

    def __call__(self,
                 s_from: Hashable,
                 input_symbol: Hashable,
                 stack_from: Hashable) -> TransitionValues:
        """ Calls transition function with given arguments """
        s_from = to_state(s_from)
        input_symbol = to_symbol(input_symbol)
        stack_from = to_stack_symbol(stack_from)
        return self._transition_function(s_from, input_symbol, stack_from)

    def __contains__(self, transition: InputTransition) -> bool:
        """ Whether the given transition is present in the PDA """
        s_from, input_symbol, stack_from, s_to, stack_to = transition
        s_from = to_state(s_from)
        input_symbol = to_symbol(input_symbol)
        stack_from = to_stack_symbol(stack_from)
        s_to = to_state(s_to)
        stack_to = tuple(to_stack_symbol(x) for x in stack_to)
        return (s_to, stack_to) in self(s_from, input_symbol, stack_from)

    def __iter__(self) -> Iterator[Transition]:
        """ Gets an iterator of transitions of the PDA """
        yield from self._transition_function

    def to_final_state(self) -> "PDA":
        """ Turns the current PDA that accepts a language L by empty stack \
        to another PDA that accepts the same language L by final state

        Returns
        ----------
        new_pda : :class:`~pyformlang.pda.PDA`
            The new PDA which accepts by final state the language that \
            was accepted by empty stack
        """
        new_start = self.__get_next_free("#STARTTOFINAL#",
                                         State,
                                         self._states)
        new_end = self.__get_next_free("#ENDTOFINAL#",
                                       State,
                                       self._states)
        new_stack_symbol = self.__get_next_free("#BOTTOMTOFINAL#",
                                                StackSymbol,
                                                self._stack_alphabet)
        new_states = self._states.copy()
        new_states.add(new_start)
        new_states.add(new_end)
        new_stack_alphabet = self._stack_alphabet.copy()
        new_stack_alphabet.add(new_stack_symbol)
        new_tf = self._transition_function.copy()
        if self.start_state and self.start_stack_symbol:
            new_tf.add_transition(new_start, PDAEpsilon(), new_stack_symbol,
                                self.start_state, (self.start_stack_symbol,
                                                   new_stack_symbol))
        for state in self._states:
            new_tf.add_transition(state, PDAEpsilon(), new_stack_symbol,
                                  new_end, tuple())
        return PDA(new_states,
                   self._input_symbols.copy(),
                   new_stack_alphabet,
                   new_tf,
                   new_start,
                   new_stack_symbol,
                   {new_end})

    def to_empty_stack(self) -> "PDA":
        """ Turns the current PDA that accepts a language L by final state to \
        another PDA that accepts the same language L by empty stack

        Returns
        ----------
        new_pda : :class:`~pyformlang.pda.PDA`
            The new PDA which accepts by empty stack the language that was \
            accepted by final state
        """
        new_start = self.__get_next_free("#STARTEMPTYS#",
                                         State,
                                         self._states)
        new_end = self.__get_next_free("#ENDEMPTYS#",
                                       State,
                                       self._states)
        new_stack_symbol = self.__get_next_free("#BOTTOMEMPTYS#",
                                                StackSymbol,
                                                self._stack_alphabet)
        new_states = self._states.copy()
        new_states.add(new_start)
        new_states.add(new_end)
        new_stack_alphabet = self._stack_alphabet.copy()
        new_stack_alphabet.add(new_stack_symbol)
        new_tf = self._transition_function.copy()
        if self.start_state and self.start_stack_symbol:
            new_tf.add_transition(new_start, PDAEpsilon(), new_stack_symbol,
                                self.start_state, (self.start_stack_symbol,
                                                   new_stack_symbol))
        for state in self._final_states:
            for stack_symbol in new_stack_alphabet:
                new_tf.add_transition(state, PDAEpsilon(), stack_symbol,
                                      new_end, tuple())
        for stack_symbol in new_stack_alphabet:
            new_tf.add_transition(new_end, PDAEpsilon(), stack_symbol,
                                  new_end, tuple())
        return PDA(new_states,
                   self._input_symbols.copy(),
                   new_stack_alphabet,
                   new_tf,
                   new_start,
                   new_stack_symbol)

    def to_cfg(self) -> CFG:
        """ Turns the language L generated by this PDA when accepting \
        on empty \
        stack into a CFG that accepts the same language L

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The equivalent CFG
        """
        variable_converter = CFGVariableConverter(self._states,
                                                  self._stack_alphabet)
        start = Variable("#StartCFG#")
        productions = self._initialize_production_from_start_in_to_cfg(
            start, variable_converter)
        states = self._states
        for transition in self:
            for state in states:
                variable_converter.set_valid(
                    transition[INPUT][STATE],
                    transition[INPUT][STACK_FROM],
                    state)
        for transition in self:
            for state in states:
                self._process_transition_and_state_to_cfg(productions,
                                                          state,
                                                          transition,
                                                          variable_converter)
        return CFG(start_symbol=start, productions=productions)

    def _process_transition_and_state_to_cfg(
            self,
            productions: List[Production],
            state: State,
            transition: Tuple[Tuple, Tuple],
            variable_converter: CFGVariableConverter) \
                -> None:
        current_state_has_empty_new_stack = \
            len(transition[OUTPUT][NEW_STACK]) == 0 and \
            state != transition[OUTPUT][STATE]
        if not current_state_has_empty_new_stack:
            self._process_transition_and_state_to_cfg_safe(productions,
                                                           state,
                                                           transition,
                                                           variable_converter)

    def _process_transition_and_state_to_cfg_safe(
            self,
            productions: List[Production],
            state: State,
            transition: Tuple[Tuple, Tuple],
            variable_converter: CFGVariableConverter) \
                -> None:
        head = self._get_head_from_state_and_transition(
            state, transition, variable_converter)
        bodies = self._get_all_bodies_from_state_and_transition(
            state, transition, variable_converter)
        if transition[INPUT][INPUT_SYMBOL] != PDAEpsilon():
            self.__prepend_input_symbol_to_the_bodies(bodies, transition)
        for body in bodies:
            productions.append(Production(head, body, filtering=False))

    def _get_all_bodies_from_state_and_transition(
            self,
            state: State,
            transition: Tuple[Tuple, Tuple],
            variable_converter: CFGVariableConverter) \
                -> List[List[CFGObject]]:
        return self._generate_all_rules(transition[OUTPUT][STATE],
                                        state,
                                        transition[OUTPUT][NEW_STACK],
                                        variable_converter)

    def _generate_all_rules(self,
                            s_from: State,
                            s_to: State,
                            ss_by: List[StackSymbol],
                            variable_converter: CFGVariableConverter) \
            -> List[List[CFGObject]]:
        """ Generates the rules in the CFG conversion """
        if not ss_by:
            return [[]]
        if len(ss_by) == 1:
            return self._generate_length_one_rules(
                s_from, s_to, ss_by, variable_converter)
        res = []
        is_valid_and_get = variable_converter.is_valid_and_get
        append_to_res = res.append
        length_ss_by_minus_one = len(ss_by) - 1
        for states in product(self._states, repeat=length_ss_by_minus_one):
            last_one = s_from
            temp = []
            stopped = False
            for i in range(length_ss_by_minus_one):
                new_variable = is_valid_and_get(last_one,
                                                ss_by[i],
                                                states[i])
                if new_variable is None:
                    stopped = True
                    break
                temp.append(new_variable)
                last_one = states[i]
            if stopped:
                continue
            new_variable = is_valid_and_get(last_one, ss_by[-1], s_to)
            if new_variable is None:
                continue
            temp.append(new_variable)
            append_to_res(temp)
        return res

    def _generate_length_one_rules(self,
                                   s_from: State,
                                   s_to: State,
                                   ss_by: List[StackSymbol],
                                   variable_converter: CFGVariableConverter) \
                                       -> List[List[CFGObject]]:
        state = variable_converter.is_valid_and_get(s_from, ss_by[0],
                                                              s_to)
        if state is not None:
            return [[state]]
        return []

    def _get_head_from_state_and_transition(
            self,
            state: State,
            transition: Tuple[Tuple, Tuple],
            variable_converter: CFGVariableConverter) \
                -> Variable:
        return variable_converter.to_cfg_combined_variable(
            transition[INPUT][STATE],
            transition[INPUT][STACK_FROM],
            state)

    def _initialize_production_from_start_in_to_cfg(
            self,
            start: Variable,
            variable_converter: CFGVariableConverter) \
                -> List[Production]:
        if not self.start_state or not self.start_stack_symbol:
            return []
        return [Production(start,
                           [variable_converter.to_cfg_combined_variable(
                               self.start_state,
                               self.start_stack_symbol,
                               state)])
                for state in self.states]

    @classmethod
    def from_cfg(cls, cfg: CFG) -> "PDA":
        """ Converts the CFG to a PDA that generates on empty stack an \
        equivalent language

        Returns
        ----------
        new_pda : :class:`~pyformlang.pda.PDA`
            The equivalent PDA when accepting on empty stack
        """
        state = State("q")
        pda_symbol_converter = PDASymbolConverter(cfg.terminals, cfg.variables)
        input_symbols = {pda_symbol_converter.get_symbol_from(x)
                         for x in cfg.terminals}
        stack_alphabet = {pda_symbol_converter.get_stack_symbol_from(x)
                          for x in cfg.terminals.union(cfg.variables)}
        start_stack_symbol = None
        if cfg.start_symbol:
            start_stack_symbol = pda_symbol_converter.get_stack_symbol_from(
                cfg.start_symbol)
        new_pda = PDA(states={state},
                          input_symbols=input_symbols,
                          stack_alphabet=stack_alphabet,
                          start_state=state,
                          start_stack_symbol=start_stack_symbol)
        for production in cfg.productions:
            new_pda.add_transition(state, PDAEpsilon(),
                                   pda_symbol_converter.get_stack_symbol_from(
                                       production.head),
                                   state,
                                   [pda_symbol_converter.get_stack_symbol_from(
                                       x) for x in production.body])
        for terminal in cfg.terminals:
            new_pda.add_transition(state,
                                   pda_symbol_converter.get_symbol_from(
                                       terminal),
                                   pda_symbol_converter.get_stack_symbol_from(
                                       terminal),
                                   state, [])
        return new_pda

    def intersection(self, other: DeterministicFiniteAutomaton) -> "PDA":
        """ Gets the intersection of the language L generated by the \
        current PDA when accepting by final state with something else

        Currently, it only works for regular languages (represented as \
        regular expressions or finite automata) as the intersection \
        between two PDAs is not context-free (it cannot be represented \
        with a PDA).

        Equivalent to:
            >> pda and regex

        Parameters
        ----------
        other : any
            The other part of the intersection

        Returns
        ----------
        new_pda : :class:`~pyformlang.pda.PDA`
            The pda resulting of the intersection

        Raises
        ----------
        NotImplementedError
            When intersecting with something else than a regex or a finite
            automaton
        """
        if not self.start_state or not other.start_state or other.is_empty():
            return PDA()
        pda_state_converter = PDAStateConverter(self._states, other.states)
        final_states_other = other.final_states
        start = pda_state_converter.to_pda_combined_state(self.start_state,
                                                          other.start_state)
        pda = PDA(start_state=start,
                  start_stack_symbol=self._start_stack_symbol)
        symbols = self._input_symbols.copy()
        symbols.add(PDAEpsilon())
        to_process = [(self.start_state, other.start_state)]
        processed = {(self.start_state, other.start_state)}
        while to_process:
            state_in, state_dfa = to_process.pop()
            if (state_in in self._final_states and state_dfa in
                    final_states_other):
                pda.add_final_state(
                    pda_state_converter.to_pda_combined_state(state_in,
                                                              state_dfa))
            for symbol in symbols:
                if symbol == PDAEpsilon():
                    symbol_dfa = FAEpsilon()
                    next_state_dfa = state_dfa
                else:
                    symbol_dfa = FASymbol(symbol.value)
                    next_state_dfa = other.get_next_state(state_dfa, symbol_dfa)
                if not next_state_dfa:
                    continue
                for stack_symbol in self._stack_alphabet:
                    next_states_self = self(state_in, symbol, stack_symbol)
                    for next_state, next_stack in next_states_self:
                        pda.add_transition(
                            pda_state_converter.to_pda_combined_state(
                                state_in,
                                state_dfa),
                            symbol,
                            stack_symbol,
                            pda_state_converter.to_pda_combined_state(
                                next_state,
                                next_state_dfa),
                            next_stack)
                        if (next_state, next_state_dfa) not in processed:
                            to_process.append((next_state, next_state_dfa))
                            processed.add((next_state, next_state_dfa))
        return pda

    def __and__(self, other: DeterministicFiniteAutomaton) -> "PDA":
        """ Gets the intersection of the current PDA with something else

        Equivalent to:
            >> pda and regex

        Parameters
        ----------
        other : any
            The other part of the intersection

        Returns
        ----------
        new_pda : :class:`~pyformlang.pda.PDA`
            The pda resulting of the intersection

        Raises
        ----------
        NotImplementedError
            When intersecting with something else than a regex or a finite
            automaton
        """
        return self.intersection(other)

    def to_dict(self) -> Dict[TransitionKey, TransitionValues]:
        """
        Get the transitions of the PDA as a dictionary
        Returns
        -------
        transitions : dict
            The transitions
        """
        return self._transition_function.to_dict()

    def to_networkx(self) -> MultiDiGraph:
        """
        Transform the current pda into a networkx graph

        Returns
        -------
        graph :  networkx.MultiDiGraph
            A networkx MultiDiGraph representing the pda

        """
        graph = MultiDiGraph()
        for state in self._states:
            graph.add_node(state.value,
                           is_start=state == self._start_state,
                           is_final=state in self.final_states,
                           peripheries=2 if state in self.final_states else 1,
                           label=state.value)
            if state == self._start_state:
                self.__add_start_state_to_graph(graph, state)
        if self._start_stack_symbol is not None:
            graph.add_node("INITIAL_STACK_HIDDEN",
                           label=dumps(self._start_stack_symbol.value),
                           shape=None,
                           height=.0,
                           width=.0)
        for key, value in self:
            s_from, in_symbol, stack_from = key
            s_to, stack_to = value
            graph.add_edge(
                s_from.value,
                s_to.value,
                label=(dumps(in_symbol.value) + " -> " +
                       dumps(stack_from.value) + " / " +
                       dumps([x.value for x in stack_to])))
        return graph

    @classmethod
    def from_networkx(cls, graph: MultiDiGraph) -> "PDA":
        """
        Import a networkx graph into a PDA. \
        The imported graph requires to have the good format, i.e. to come \
        from the function to_networkx

        Parameters
        ----------
        graph :
            The graph representation of the PDA

        Returns
        -------
        pda :
            A PDA automaton read from the graph

        TODO
        -------
        * Explain the format
        """
        pda = PDA()
        for s_from in graph:
            if isinstance(s_from, str) and s_from.startswith("starting_"):
                continue
            for s_to in graph[s_from]:
                for transition in graph[s_from][s_to].values():
                    if "label" in transition:
                        in_symbol, stack_info = transition["label"].split(
                            " -> ")
                        in_symbol = loads(in_symbol)
                        stack_from, stack_to = stack_info.split(" / ")
                        stack_from = loads(stack_from)
                        stack_to = loads(stack_to)
                        pda.add_transition(s_from,
                                           in_symbol,
                                           stack_from,
                                           s_to,
                                           stack_to)
        for node in graph.nodes:
            if graph.nodes[node].get("is_start", False):
                pda.set_start_state(node)
            if graph.nodes[node].get("is_final", False):
                pda.add_final_state(node)
        if "INITIAL_STACK_HIDDEN" in graph.nodes:
            pda.set_start_stack_symbol(
                loads(graph.nodes["INITIAL_STACK_HIDDEN"]["label"]))
        return pda

    def write_as_dot(self, filename: str) -> None:
        """
        Write the PDA in dot format into a file

        Parameters
        ----------
        filename : str
            The filename where to write the dot file

        """
        write_dot(self.to_networkx(), filename)

    def copy(self) -> "PDA":
        """ Copies the Push-down Automaton """
        return PDA(self.states,
                   self.input_symbols,
                   self.stack_symbols,
                   self._transition_function.copy(),
                   self.start_state,
                   self.start_stack_symbol,
                   self.final_states)

    def __copy__(self) -> "PDA":
        return self.copy()

    @staticmethod
    def __add_start_state_to_graph(graph: MultiDiGraph,
                                   state: State) -> None:
        """ Adds a starting node to a given graph """
        graph.add_node("starting_" + str(state.value),
                    label="",
                    shape=None,
                    height=.0,
                    width=.0)
        graph.add_edge("starting_" + str(state.value),
                    state.value)

    @staticmethod
    def __prepend_input_symbol_to_the_bodies(bodies: List[List[CFGObject]],
                                            transition: Tuple[Tuple, Tuple]) \
                                                -> None:
        to_prepend = Terminal(transition[INPUT][INPUT_SYMBOL].value)
        for body in bodies:
            body.insert(0, to_prepend)

    @staticmethod
    def __get_next_free(prefix: str,
                        type_generating: Type,
                        to_check: Iterable[Any]) -> Any:
        """ Get free next state or symbol """
        idx = 0
        new_var = type_generating(prefix)
        while new_var in to_check:
            new_var = type_generating(prefix + str(idx))
            idx += 1
        return new_var
