"""The transition function of Finite State Transducer."""

from typing import Dict, Set, Tuple, Iterator, Iterable
from copy import deepcopy

from ..objects.finite_automaton_objects import State, Symbol

TransitionKey = Tuple[State, Symbol]
TransitionValue = Tuple[State, Tuple[Symbol, ...]]
TransitionValues = Set[TransitionValue]
Transition = Tuple[TransitionKey, TransitionValue]


class TransitionFunction(Iterable[Transition]):
    """The transition function of Finite State Transducer."""

    def __init__(self) -> None:
        """Creates an empty FST transition function."""
        self._transitions: Dict[TransitionKey, TransitionValues] = {}

    def add_transition(self,
                       s_from: State,
                       input_symbol: Symbol,
                       s_to: State,
                       output_symbols: Tuple[Symbol, ...]) -> None:
        """Adds the given transition to the function.

        Parameters
        ----------
        s_from:
            The source state.
        input_symbol:
            The symbol to read.
        s_to:
            The destination state.
        output_symbols:
            The symbols to output.
        """
        key = (s_from, input_symbol)
        value = (s_to, output_symbols)
        self._transitions.setdefault(key, set()).add(value)

    def remove_transition(self,
                          s_from: State,
                          input_symbol: Symbol,
                          s_to: State,
                          output_symbols: Tuple[Symbol, ...]) -> None:
        """Removes the given transition from the function.

        Parameters
        ----------
        s_from:
            The source state.
        input_symbol:
            The symbol to read.
        s_to:
            The destination state.
        output_symbols:
            The symbols to output.
        """
        key = (s_from, input_symbol)
        value = (s_to, output_symbols)
        self._transitions.get(key, set()).discard(value)

    def get_number_transitions(self) -> int:
        """Gets the number of transitions in the function.

        Returns
        -------
        The number of transitions in the function.
        """
        return sum(len(x) for x in self._transitions.values())

    def __call__(self, s_from: State, input_symbol: Symbol) \
            -> TransitionValues:
        """Makes a call of the transition function.

        Parameters
        ----------
        s_from:
            The source state.
        input_symbol:
            The symbol to read.

        Returns
        -------
        A set of destination state and output string pairs.
        """
        return self._transitions.get((s_from, input_symbol), set())

    def __contains__(self, transition: Transition) -> bool:
        """Checks if the given transition is present in the function.

        Parameters
        ----------
        transition:
            The transition to check containment of.

        Returns
        -------
        Whether the given transition is present in the function.
        """
        key, value = transition
        return value in self(*key)

    def __iter__(self) -> Iterator[Transition]:
        """Yields the transitions described by the transition function."""
        for key, values in self._transitions.items():
            for value in values:
                yield key, value

    def copy(self) -> "TransitionFunction":
        """Copies the current transition function.

        Returns
        -------
        A copy of the transition function.
        """
        new_tf = TransitionFunction()
        for key, value in self:
            new_tf.add_transition(*key, *value)
        return new_tf

    def __copy__(self) -> "TransitionFunction":
        """Copies the current transition function."""
        return self.copy()

    def to_dict(self) -> Dict[TransitionKey, TransitionValues]:
        """Gets the dictionary representation of the transition function.

        Returns
        -------
        The transition function as a dictionary.
        """
        return deepcopy(self._transitions)
