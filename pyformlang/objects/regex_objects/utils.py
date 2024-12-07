""" Utility for regex object creation """

from .regex_objects import Symbol, Node, \
    Empty, Concatenation, Union, KleeneStar, Epsilon

CONCATENATION_SYMBOLS = ["."]
UNION_SYMBOLS = ["|", "+"]
KLEENE_STAR_SYMBOLS = ["*"]
EPSILON_SYMBOLS = ["epsilon", "$"]
PARENTHESIS = ["(", ")"]

SPECIAL_SYMBOLS = CONCATENATION_SYMBOLS + \
                  UNION_SYMBOLS + \
                  KLEENE_STAR_SYMBOLS + \
                  EPSILON_SYMBOLS + \
                  PARENTHESIS


def to_node(value: str) -> Node:
    """ Transforms a given value into a node """
    if not value:
        res = Empty()
    elif value in CONCATENATION_SYMBOLS:
        res = Concatenation()
    elif value in UNION_SYMBOLS:
        res = Union()
    elif value in KLEENE_STAR_SYMBOLS:
        res = KleeneStar()
    elif value in EPSILON_SYMBOLS:
        res = Epsilon()
    elif value[0] == "\\":
        res = Symbol(value[1:])
    else:
        res = Symbol(value)
    return res
