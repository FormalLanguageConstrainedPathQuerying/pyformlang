"""This module implements functions related to context-free grammars.

:mod:`pyformlang.cfg`
=====================

Available Classes
-----------------
:class:`pyformlang.cfg.CFG`:
    The main context-free grammar class.
:class:`pyformlang.cfg.Production`:
    A class to represent a production in a CFG.
:class:`pyformlang.cfg.CFGObject`:
    A general CFG object representation.
:class:`pyformlang.cfg.Variable`:
    A variable in context-free grammar.
:class:`pyformlang.cfg.Terminal`:
    A terminal in context-free grammar.
:class:`pyformlang.cfg.Epsilon`:
    The epsilon symbol (special terminal).
:class:`pyformlang.cfg.ParseTree`:
    A parse tree of the grammar.
:class:`pyformlang.cfg.DerivationDoesNotExistError`:
    An exception that occurs if the given word cannot
    be derived from the grammar.
"""

from .cfg import CFG, CFGObject, Variable, Terminal, Epsilon, Production
from .parse_tree import ParseTree, DerivationDoesNotExistError


__all__ = [
    "CFG",
    "Production",
    "CFGObject",
    "Variable",
    "Terminal",
    "Epsilon",
    "ParseTree",
    "DerivationDoesNotExistError",
]
