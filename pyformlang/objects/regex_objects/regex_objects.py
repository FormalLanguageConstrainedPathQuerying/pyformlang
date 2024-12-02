"""
Representation of some objects used in regex.
"""

from typing import List, Iterable
from abc import abstractmethod

from ..cfg_objects.production import Production
from ..cfg_objects.utils import to_variable, to_terminal


class Node:
    """ Represents a node in the tree representation of a regex

    Parameters
    ----------
    value : str
        The value of the node
    """

    def __init__(self, value: str) -> None:
        self._value = value

    @property
    def value(self) -> str:
        """ Give the value of the node

        Returns
        ----------
        value : str
            The value of the node
        """
        return self._value

    @abstractmethod
    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        """
        The string representation of the node

        Parameters
        ----------
        sons_repr : iterable of str
            The sons representations

        Returns
        -------
        repr : str
            The representation of this node

        """
        raise NotImplementedError

    @abstractmethod
    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        """ Gets the rules for a context-free grammar to represent the \
        operator"""
        raise NotImplementedError


class Operator(Node):
    """ Represents an operator

    Parameters
    ----------
    value : str
        The value of the operator
    """

    def __repr__(self) -> str:
        return "Operator(" + str(self._value) + ")"

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        """ Get the string representation """
        raise NotImplementedError

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        """ Gets the rules for a context-free grammar to represent the \
        operator"""
        raise NotImplementedError


class Symbol(Node):
    """ Represents a symbol

    Parameters
    ----------
    value : str
        The value of the symbol
    """

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        return str(self.value)

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        """ Gets the rules for a context-free grammar to represent the \
        operator"""
        return [Production(
            to_variable(current_symbol),
            [to_terminal(self.value)])]

    def __repr__(self) -> str:
        return "Symbol(" + str(self._value) + ")"


class Concatenation(Operator):
    """ Represents a concatenation
    """

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        return "(" + ".".join(sons_repr) + ")"

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        return [Production(
            to_variable(current_symbol),
            [to_variable(son) for son in sons])]

    def __init__(self) -> None:
        super().__init__("Concatenation")


class Union(Operator):
    """ Represents a union
    """

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        return "(" + "|".join(sons_repr) + ")"

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        return [Production(
            to_variable(current_symbol),
            [to_variable(son)]) for son in sons]

    def __init__(self) -> None:
        super().__init__("Union")


class KleeneStar(Operator):
    """ Represents an epsilon symbol
    """

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        return "(" + ".".join(sons_repr) + ")*"

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
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

    def __init__(self) -> None:
        super().__init__("Kleene Star")


class Epsilon(Symbol):
    """ Represents an epsilon symbol
    """

    def get_str_repr(self, sons_repr: Iterable[str]) -> str:
        return "$"

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        return [Production(to_variable(current_symbol), [])]

    def __init__(self) -> None:
        super().__init__("Epsilon")


class Empty(Symbol):
    """ Represents an empty symbol
    """

    def __init__(self) -> None:
        super().__init__("Empty")

    def get_cfg_rules(self, current_symbol: str, sons: Iterable[str]) \
            -> List[Production]:
        return []


class MisformedRegexError(Exception):
    """ Error for misformed regex """

    def __init__(self, message: str, regex: str) -> None:
        super().__init__(message + " Regex: " + regex)
        self._regex = regex
