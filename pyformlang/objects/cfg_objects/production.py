"""A production or rule of a CFG."""

from typing import List, Set, Any

from .cfg_object import CFGObject
from .variable import Variable
from .terminal import Terminal
from .epsilon import Epsilon


class Production:
    """A production or rule of a CFG.

    Parameters
    ----------
    head:
        The head of the production.
    body:
        The body of the production.
    filtering:
        Whether to ignore the epsilon terminals in body.
    """

    __slots__ = ["_body", "_head", "_hash"]

    def __init__(self,
                 head: Variable,
                 body: List[CFGObject],
                 filtering: bool = True) -> None:
        """Initializes the production."""
        if filtering:
            self._body = [x for x in body if not isinstance(x, Epsilon)]
        else:
            self._body = body
        self._head = head
        self._hash = None

    @property
    def head(self) -> Variable:
        """Gets the head variable of the production."""
        return self._head

    @property
    def body(self) -> List[CFGObject]:
        """Gets the body objects of the production."""
        return self._body

    @property
    def variables(self) -> Set[Variable]:
        """Gets variables used in the production."""
        return {self.head} | {object for object in self.body
                              if isinstance(object, Variable)}

    @property
    def terminals(self) -> Set[Terminal]:
        """Gets terminals used in the production."""
        return {object for object in self.body
                if isinstance(object, Terminal) and object != Epsilon()}

    def __eq__(self, other: Any) -> bool:
        """Checks if current production is equal to the given object."""
        if not isinstance(other, Production):
            return False
        return self.head == other.head and self.body == other.body

    def __hash__(self) -> int:
        """Gets the hash of the production."""
        if self._hash is None:
            self._hash = sum(map(hash, self._body)) + hash(self._head)
        return self._hash

    def __repr__(self) -> str:
        """Gets the string representation of the production."""
        return str(self.head) + " -> " + " ".join([str(x) for x in self.body])

    def is_normal_form(self) -> bool:
        """Tells if the production is in Chomsky Normal Form.

        Returns
        -------
        Whether the production is in CNF.
        """
        if len(self._body) == 2:
            return (isinstance(self._body[0], Variable) and
                    isinstance(self._body[1], Variable))
        if len(self._body) == 1:
            return isinstance(self._body[0], Terminal)
        return False
