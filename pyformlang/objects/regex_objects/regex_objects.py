"""Representation of some objects used in regex."""

from typing import List, Iterable
from abc import abstractmethod

from ..cfg_objects.production import Production
from ..cfg_objects.utils import to_variable, to_terminal


class Node:
    """Represents a node in the tree representation of a regex.

    Parameters
    ----------
    value:
        The value of the node.
    """

    def __init__(self, value: str) -> None:
        """Initializes the node."""
        self._value = value

    @property
    def value(self) -> str:
        """Gets the value of the node.

        Returns
        -------
        The value of the node.
        """
        return self._value

    @abstractmethod
    def __repr__(self) -> str:
        """Gets a string representation of the node."""
        raise NotImplementedError

    @abstractmethod
    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        """Gets the string representation of the node with given sons.

        Parameters
        ----------
        sons_repr:
            The sons representations.

        Returns
        -------
        The representation of this node.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        """Gets CFG productions representing the current node.

        Parameters
        ----------
        current_symbol:
            A head of the productions.
        sons:
            The son representations.

        Returns
        -------
        The productions representing the node.
        """
        raise NotImplementedError


class Operator(Node):
    """Represents an operator.

    Parameters
    ----------
    value:
        The value of the operator.
    """

    def __repr__(self) -> str:
        """Gets a string representation of the operator node."""
        return "Operator(" + str(self._value) + ")"

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        """Get the string representation of the operator with sons."""
        raise NotImplementedError

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        """Gets CFG productions representing the operator."""
        raise NotImplementedError


class Symbol(Node):
    """Represents a symbol.

    Parameters
    ----------
    value:
        The value of the symbol.
    """

    def __repr__(self) -> str:
        """Gets a string representation of the symbol node."""
        return "Symbol(" + str(self._value) + ")"

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        """Gets a string representation of the symbol with given sons."""
        return str(self.value)

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        """Gets CFG productions representing the symbol."""
        return [Production(
            to_variable(current_symbol),
            [to_terminal(self.value)])]


class Concatenation(Operator):
    """Represents a concatenation."""

    def __init__(self) -> None:
        """Initializes the concatenation operator."""
        super().__init__("Concatenation")

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        """Gets a string representation of the operator with given sons."""
        return "(" + ".".join(sons_repr) + ")"

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        """Gets CFG productions representing the operator."""
        return [Production(
            to_variable(current_symbol),
            [to_variable(son) for son in sons])]


class Union(Operator):
    """Represents a union."""

    def __init__(self) -> None:
        """Initializes the union operator."""
        super().__init__("Union")

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        """Gets a string representation of the operator with given sons."""
        return "(" + "|".join(sons_repr) + ")"

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        """Gets CFG productions representing the operator."""
        return [Production(
            to_variable(current_symbol),
            [to_variable(son)]) for son in sons]


class KleeneStar(Operator):
    """Represents a kleene star operator."""

    def __init__(self) -> None:
        """Initializes the kleene star operator."""
        super().__init__("Kleene Star")

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        """Gets a string representation of the operator with given sons."""
        return "(" + ".".join(sons_repr) + ")*"

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        """Gets CFG productions representing the operator."""
        return [
            Production(
                to_variable(current_symbol), []),
            Production(
                to_variable(current_symbol),
                [to_variable(current_symbol), to_variable(current_symbol)]),
            Production(
                to_variable(current_symbol),
                [to_variable(son) for son in sons])
        ]


class Epsilon(Symbol):
    """Represents an epsilon symbol."""

    def __init__(self) -> None:
        """Initializes the epsilon symbol."""
        super().__init__("Epsilon")

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        """Gets a string representation of the symbol with given sons."""
        return "$"

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        """Gets CFG productions representing the symbol."""
        return [Production(to_variable(current_symbol), [])]


class Empty(Symbol):
    """Represents an empty symbol."""

    def __init__(self) -> None:
        """Initializes the empty symbol."""
        super().__init__("Empty")

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        """Gets CFG productions representing the symbol."""
        return []


class MisformedRegexError(Exception):
    """Error for misformed regex."""

    def __init__(self, message: str, regex: str) -> None:
        """Initializes the misformed regex exception.

        Parameters
        ----------
        message:
            A message to show.
        regex:
            A regex that caused the error.
        """
        super().__init__(message + " Regex: " + regex)
        self._regex = regex
