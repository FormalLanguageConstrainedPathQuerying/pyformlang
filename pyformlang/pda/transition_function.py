"""A transition function in a push-down automaton."""

from typing import Dict, Set, Iterator, Iterable, Tuple
from copy import deepcopy

from ..objects.pda_objects import State, Symbol, StackSymbol

TransitionKey = Tuple[State, Symbol, StackSymbol]
TransitionValue = Tuple[State, Tuple[StackSymbol, ...]]
TransitionValues = Set[TransitionValue]
Transition = Tuple[TransitionKey, TransitionValue]


class TransitionFunction(Iterable[Transition]):
    """A transition function in a push-down automaton."""

    def __init__(self) -> None:
        """Creates an empty PDA transition function."""
        self._transitions: Dict[TransitionKey, TransitionValues] = {}

    # pylint: disable=too-many-arguments
    def add_transition(self,
                       s_from: State,
                       input_symbol: Symbol,
                       stack_from: StackSymbol,
                       s_to: State,
                       stack_to: Tuple[StackSymbol, ...]) -> None:
        """Adds the given transition to the function.

        Parameters
        ----------
        s_from:
            The starting state of the transition.
        input_symbol:
            The input symbol of the transition.
        stack_from:
            The source stack symbol of the transition.
        s_to:
            The target state of the transition.
        stack_to:
            The sequence of stack symbols to replace `stack_from` with.
        """
        temp_in = (s_from, input_symbol, stack_from)
        temp_out = (s_to, stack_to)
        if temp_in in self._transitions:
            self._transitions[temp_in].add(temp_out)
        else:
            self._transitions[temp_in] = {temp_out}

    def remove_transition(self,
                          s_from: State,
                          input_symbol: Symbol,
                          stack_from: StackSymbol,
                          s_to: State,
                          stack_to: Tuple[StackSymbol, ...]) -> None:
        """Removes the given transition from the function.

        Parameters
        ----------
        s_from:
            The starting state of the transition.
        input_symbol:
            The input symbol of the transition.
        stack_from:
            The source stack symbol of the transition.
        s_to:
            The target state of the transition.
        stack_to:
            The target stack symbol sequence of the transition.
        """
        key = (s_from, input_symbol, stack_from)
        self._transitions.get(key, set()).discard((s_to, stack_to))

    def get_number_transitions(self) -> int:
        """Gets the number of transitions described by the function.

        Returns
        -------
        The number of transitions in the function.
        """
        return sum(len(x) for x in self._transitions.values())

    def __call__(self,
                 s_from: State,
                 input_symbol: Symbol,
                 stack_from: StackSymbol) -> TransitionValues:
        """Makes a call of the transition function.

        Parameters
        ----------
        s_from:
            The starting state of the transition.
        input_symbol:
            The input symbol of the transition.
        stack_from:
            The source stack symbol of the transition.

        Returns
        -------
        A set of target state and target stack pairs.
        """
        return self._transitions.get((s_from, input_symbol, stack_from), set())

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
        for temp_in, temp_out in self:
            new_tf.add_transition(*temp_in, *temp_out)
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
