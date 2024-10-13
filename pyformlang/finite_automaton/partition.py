"""Class to manage partitions used in Hopcroft minimization algorithm
For internal usage.
"""

from typing import Dict, List, Iterable, Any

from .doubly_linked_list import DoublyLinkedList


class Partition:
    """Class to manage partitions used in Hopcroft minimization algorithm"""

    def __init__(self, n_states: int) -> None:
        self._class_names: Dict[Any, int] = {}  # States to class index
        # Class idx to states
        self.part: List[DoublyLinkedList] = \
            [DoublyLinkedList() for _ in range(n_states)]
        self._place: Dict[Any, Any] = {}  # state to position in list
        self._counter = 0  # Number of classes

    def add_class(self, new_class: Iterable[Any]) -> None:
        """Adds a new class"""
        index = self._counter
        self._counter += 1
        for element in new_class:
            self._class_names[element] = index
            node = self.part[index].append(element)
            self._place[element] = node

    def move_to_new_class(self, elements_to_move: Iterable[Any]) -> None:
        """Move elements to a new class"""
        for element in elements_to_move:
            place = self._place[element]
            place.delete()
        self.add_class(elements_to_move)

    def get_valid_sets(self, inverse: Iterable[Any]) -> List[int]:
        """Get the valid sets"""
        class_names = [0] * self._counter
        for element in inverse:
            class_names[self._class_names[element]] += 1
        return [i for i, value in enumerate(class_names)
                if value != 0 and value != len(self.part[i])]

    def split(self, to_split: Any, splitter: Iterable[Any]) -> int:
        """ Splits """
        elements_to_move = []
        for element in splitter:
            if self._class_names[element] == to_split:
                elements_to_move.append(element)
        self.move_to_new_class(elements_to_move)
        return self._counter - 1

    def get_groups(self) -> List[Any]:
        """ Get the groups """
        res = []
        for i in range(self._counter):
            res.append([x.value for x in self.part[i]])
        return res
