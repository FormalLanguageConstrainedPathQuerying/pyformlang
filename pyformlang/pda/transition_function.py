""" A transition function in a pushdown automaton """

from copy import deepcopy
from typing import Dict, Set, Sequence, Iterator, Iterable, Tuple

from ..objects.pda_objects import State, Symbol, StackSymbol

TransitionKey = Tuple[State, Symbol, StackSymbol]
TransitionValue = Tuple[State, Tuple[StackSymbol, ...]]
TransitionValues = Set[TransitionValue]
Transition = Tuple[TransitionKey, TransitionValue]


class TransitionFunction(Iterable[Transition]):
    """ A transition function in a pushdown automaton """

    def __init__(self) -> None:
        self._transitions: Dict[TransitionKey, TransitionValues] = {}

    def get_number_transitions(self) -> int:
        """ Gets the number of transitions

        Returns
        ----------
        n_transitions : int
            The number of transitions
        """
        return sum(len(x) for x in self._transitions.values())

    # pylint: disable=too-many-arguments
    def add_transition(self,
                       s_from: State,
                       input_symbol: Symbol,
                       stack_from: StackSymbol,
                       s_to: State,
                       stack_to: Sequence[StackSymbol]) -> None:
        """ Add a transition to the function

        Parameters
        ----------
        s_from : :class:`~pyformlang.pda.State`
            The starting symbol
        input_symbol : :class:`~pyformlang.pda.Symbol`
            The input symbol
        stack_from : :class:`~pyformlang.pda.StackSymbol`
            The stack symbol of the transition
        s_to : :class:`~pyformlang.pda.State`
            The new state
        stack_to : list of :class:`~pyformlang.pda.StackSymbol`
            The string of stack symbol which replace the stack_from
        """
        temp_in = (s_from, input_symbol, stack_from)
        temp_out = (s_to, tuple(stack_to))
        if temp_in in self._transitions:
            self._transitions[temp_in].add(temp_out)
        else:
            self._transitions[temp_in] = {temp_out}

    def copy(self) -> "TransitionFunction":
        """ Copy the current transition function

        Returns
        ----------
        new_tf : :class:`~pyformlang.pda.TransitionFunction`
            The copy of the transition function
        """
        new_tf = TransitionFunction()
        for temp_in, transition in self._transitions.items():
            for temp_out in transition:
                new_tf.add_transition(temp_in[0], temp_in[1], temp_in[2],
                                      *temp_out)
        return new_tf

    def __iter__(self) -> Iterator[Transition]:
        for key, values in self._transitions.items():
            for value in values:
                yield key, value

    def __call__(self,
                 s_from: State,
                 input_symbol: Symbol,
                 stack_from: StackSymbol) -> TransitionValues:
        return self._transitions.get((s_from, input_symbol, stack_from), set())

    def to_dict(self) -> Dict[TransitionKey, TransitionValues]:
        """Get the dictionary representation of the transitions"""
        return deepcopy(self._transitions)
