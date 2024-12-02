""" A production or rule of a CFG """

from typing import List, Set, Any

from .cfg_object import CFGObject
from .variable import Variable
from .terminal import Terminal
from .epsilon import Epsilon


class Production:
    """ A production or rule of a CFG

    Parameters
    ----------
    head : :class:`~pyformlang.cfg.Variable`
        The head of the production
    body : iterable of :class:`~pyformlang.cfg.CFGObject`
        The body of the production
    """

    __slots__ = ["_body", "_head", "_hash"]

    def __init__(self,
                 head: Variable,
                 body: List[CFGObject],
                 filtering: bool = True) -> None:
        if filtering:
            self._body = [x for x in body if not isinstance(x, Epsilon)]
        else:
            self._body = body
        self._head = head
        self._hash = None

    @property
    def head(self) -> Variable:
        """Gets the head variable"""
        return self._head

    @property
    def body(self) -> List[CFGObject]:
        """Gets the body objects"""
        return self._body

    @property
    def body_variables(self) -> Set[Variable]:
        """Gets variables of body of the production"""
        return {object for object in self.body if isinstance(object, Variable)}

    @property
    def body_terminals(self) -> Set[Terminal]:
        """Gets terminals of body of the production"""
        return {object for object in self.body if isinstance(object, Terminal)}

    def __repr__(self) -> str:
        return str(self.head) + " -> " + " ".join([str(x) for x in self.body])

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Production):
            return False
        return self.head == other.head and self.body == other.body

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = sum(map(hash, self._body)) + hash(self._head)
        return self._hash

    def is_normal_form(self) -> bool:
        """
        Tells is the production is in Chomsky Normal Form

        Returns
        -------
        is_normal_form : bool
            If the production is in CNF

        """
        if len(self._body) == 2:
            return (isinstance(self._body[0], Variable) and
                    isinstance(self._body[1], Variable))
        if len(self._body) == 1:
            return isinstance(self._body[0], Terminal)
        return False
