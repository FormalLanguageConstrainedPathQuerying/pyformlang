"""States for internal usage."""

from typing import Dict, List, Iterable, Tuple

from pyformlang.cfg import Variable, Terminal, ParseTree

from .feature_structure import FeatureStructure
from .feature_production import FeatureProduction

Positions = Tuple[int, int, int]
StateKey = Tuple[FeatureProduction, Positions]
ProcessedStates = List[Dict[StateKey, List["State"]]]


class State:
    """State for internal usage."""

    def __init__(self,
                 production: FeatureProduction,
                 positions: Positions,
                 feature_stucture: FeatureStructure,
                 parse_tree: ParseTree) -> None:
        """Initializes the state."""
        self.production = production
        self.positions = positions
        self.feature_stucture = feature_stucture
        self.parse_tree = parse_tree

    def get_key(self) -> StateKey:
        """Gets the key of the state."""
        return self.production, self.positions

    def is_incomplete(self) -> bool:
        """Checks if a state is incomplete."""
        return self.positions[2] < len(self.production.body)

    def next_is_variable(self) -> bool:
        """Checks if the next symbol to process is a variable."""
        return isinstance(self.production.body[self.positions[2]], Variable)

    def next_is_symbol(self, symbol: Terminal) -> bool:
        """Check if the next symbol matches the given symbol."""
        return self.production.body[self.positions[2]] == symbol


class StateProcessed:
    """List of processed states for internal usage."""

    def __init__(self, size: int) -> None:
        """Initializes the list of processed states."""
        self.processed: ProcessedStates = [{} for _ in range(size)]

    def add(self, i: int, element: State) -> bool:
        """Adds the given state to the processed states.

        Returns
        -------
        Whether the insertion was successful or not.
        """
        key = element.get_key()
        if key not in self.processed[i]:
            self.processed[i][key] = []
        for other in self.processed[i][key]:
            if other.feature_stucture.subsumes(element.feature_stucture):
                return False
        self.processed[i][key].append(element)
        return True

    def generator(self, i: int) -> Iterable[State]:
        """Generates a collection of all the states at the given position."""
        for states in self.processed[i].values():
            yield from states
