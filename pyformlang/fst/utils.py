""" Utility for FST """

from typing import Dict, Set, Iterable, Tuple

from ..objects.finite_automaton_objects import State
from ..objects.finite_automaton_objects.utils import to_state


class StateRenaming:
    """ Class for renaming the states in FST """

    def __init__(self) -> None:
        self._state_renaming: Dict[Tuple[str, int], str] = {}
        self._seen_states: Set[str] = set()

    def add_state(self, state: State, idx: int) -> None:
        """
        Add a state
        Parameters
        ----------
        state : State
            The state to add
        idx : int
            The index of the FST
        """
        current_name = str(state)
        if current_name in self._seen_states:
            counter = 0
            new_name = current_name + str(counter)
            while new_name in self._seen_states:
                counter += 1
                new_name = current_name + str(counter)
            self._state_renaming[(current_name, idx)] = new_name
            self._seen_states.add(new_name)
        else:
            self._state_renaming[(current_name, idx)] = current_name
            self._seen_states.add(current_name)

    def add_states(self, states: Iterable[State], idx: int) -> None:
        """
        Add states
        Parameters
        ----------
        states : Iterable of States
            The states to add
        idx : int
            The index of the FST
        """
        for state in states:
            self.add_state(state, idx)

    def get_renamed_state(self, state: State, idx: int) -> State:
        """
        Get the renaming.

        Parameters
        ----------
        state : State
            The state to rename
        idx : int
            The index of the FST

        Returns
        -------
        new_name : State
            Renamed state
        """
        renaming = self._state_renaming[(str(state), idx)]
        return to_state(renaming)
