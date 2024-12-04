"""
:mod:`pyformlang.fcfg`
=======================

This submodule implements functions related to feature-based grammars.


Available Classes
-----------------

Sources
-------

Daniel Jurafsky and James H. Martin, Speech and Language Processing

"""

from .fcfg import FCFG, CFGObject, \
    Variable, Terminal, Epsilon, ParseTree, NotParsableException
from .feature_production import FeatureProduction
from .feature_structure import FeatureStructure, \
    ContentAlreadyExistsException, \
    FeatureStructuresNotCompatibleException, \
    PathDoesNotExistsException


__all__ = ["FCFG",
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
           "PathDoesNotExistsException"]
