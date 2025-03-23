""" A queue with non duplicate elements"""

from typing import Any


class SetQueue:
    """ A queue with non duplicate elements"""

    def __init__(self) -> None:
        self._to_process = []
        self._processing = set()

    def append(self, value: Any) -> None:
        """ Append an element """
        if value not in self._processing:
            self._to_process.append(value)
            self._processing.add(value)

    def pop(self) -> Any:
        """ Pop an element """
        popped = self._to_process.pop()
        self._processing.remove(popped)
        return popped

    def __bool__(self) -> bool:
        return bool(self._to_process)
