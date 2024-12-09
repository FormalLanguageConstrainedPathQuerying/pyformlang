""" The transition function of Finite State Transducer """

from typing import Dict, Set, Tuple, Iterator, Iterable
from copy import deepcopy

from ..objects.finite_automaton_objects import State, Symbol

TransitionKey = Tuple[State, Symbol]
TransitionValue = Tuple[State, Tuple[Symbol, ...]]
TransitionValues = Set[TransitionValue]
Transition = Tuple[TransitionKey, TransitionValue]


class TransitionFunction(Iterable[Transition]):
    """ The transition function of Finite State Transducer """

    def __init__(self) -> None:
        self._transitions: Dict[TransitionKey, TransitionValues] = {}

    def add_transition(self,
                       s_from: State,
                       input_symbol: Symbol,
                       s_to: State,
                       output_symbols: Tuple[Symbol, ...]) -> None:
        """ Adds given transition to the function """
        key = (s_from, input_symbol)
        value = (s_to, output_symbols)
        self._transitions.setdefault(key, set()).add(value)

    def remove_transition(self,
                          s_from: State,
                          input_symbol: Symbol,
                          s_to: State,
                          output_symbols: Tuple[Symbol, ...]) -> None:
        """ Removes given transition from the function """
        key = (s_from, input_symbol)
        value = (s_to, output_symbols)
        self._transitions.get(key, set()).discard(value)

    def get_number_transitions(self) -> int:
        """ Gets the number of transitions in the function

        Returns
        ----------
        n_transitions : int
            The number of transitions
        """
        return sum(len(x) for x in self._transitions.values())

    def __call__(self, s_from: State, input_symbol: Symbol) \
            -> TransitionValues:
        """ Calls the transition function """
        return self._transitions.get((s_from, input_symbol), set())

    def __contains__(self, transition: Transition) -> bool:
        """ Whether the given transition is present in the function """
        key, value = transition
        return value in self(*key)

    def __iter__(self) -> Iterator[Transition]:
        """ Gets an iterator of transitions of the function """
        for key, values in self._transitions.items():
            for value in values:
                yield key, value

    def copy(self) -> "TransitionFunction":
        """ Copies the transition function """
        new_tf = TransitionFunction()
        for key, value in self:
            new_tf.add_transition(*key, *value)
        return new_tf

    def __copy__(self) -> "TransitionFunction":
        return self.copy()

    def to_dict(self) -> Dict[TransitionKey, TransitionValues]:
        """ Gives the transition function as a dictionary """
        return deepcopy(self._transitions)
