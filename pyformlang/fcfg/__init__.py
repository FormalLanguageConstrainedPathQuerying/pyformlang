"""This module implements functions related to feature-based grammars.

:mod:`pyformlang.fcfg`
======================

Available Classes
-----------------
:class:`pyformlang.fcfg.FCFG`:
    A context-free grammar with features.
:class:`pyformlang.fcfg.FeatureStructure`:
    A feature structure containing constraints.
:class:`pyformlang.fcfg.FeatureProduction`:
    A production in the FCFG.
:class:`pyformlang.fcfg.CFGObject`:
    The general CFG object used in FCFG.
:class:`pyformlang.fcfg.Variable`:
    A variable in FCFG.
:class:`pyformlang.fcfg.Terminal`:
    A terminal in FCFG.
:class:`pyformlang.fcfg.Epsilon`:
    The epsilon terminal.
:class:`pyformlang.fcfg.ParseTree`:
    A parse tree of the grammar.
:class:`pyformlang.fcfg.NotParsableException`:
    An exception that occurs when the given grammar cannot be parsed.
:class:`pyformlang.fcfg.ContentAlreadyExistsException`:
    An exception raised when trying to add content that already exists.
:class:`pyformlang.fcfg.FeatureStructuresNotCompatibleException`:
    An exception raised when trying to unify incompatible structures.
:class:`pyformlang.fcfg.PathDoesNotExistsException`:
    An exception raised when looking for a path that does not exist.

Sources
-------
Daniel Jurafsky and James H. Martin, Speech and Language Processing.
"""

from .fcfg import FCFG, CFGObject, \
    Variable, Terminal, Epsilon, ParseTree, NotParsableException
from .feature_production import FeatureProduction
from .feature_structure import FeatureStructure, \
    ContentAlreadyExistsException, \
    FeatureStructuresNotCompatibleException, \
    PathDoesNotExistsException


__all__ = [
    "FCFG",
    "FeatureStructure",
    "FeatureProduction",
    "CFGObject",
    "Variable",
    "Terminal",
    "Epsilon",
    "ParseTree",
    "NotParsableException",
    "ContentAlreadyExistsException",
    "FeatureStructuresNotCompatibleException",
    "PathDoesNotExistsException",
]
