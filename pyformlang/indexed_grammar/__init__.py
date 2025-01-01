"""This module deals with indexed grammars.

:mod:`pyformlang.indexed_grammar`
=================================

Available Classes
-----------------
:class:`pyformlang.indexed_grammar.IndexedGrammar`:
    An indexed grammar.
:class:`pyformlang.indexed_grammar.Rules`:
    A representation of a set of indexed grammar rules.
:class:`pyformlang.indexed_grammar.ReducedRule`:
    An indexed grammar rule of any of possible forms.
:class:`pyformlang.indexed_grammar.ConsumptionRule`:
    A consumption rule, consuming something from the stack.
:class:`pyformlang.indexed_grammar.EndRule`:
    An end rule, turning a variable into a terminal.
:class:`pyformlang.indexed_grammar.ProductionRule`:
    A production rule, pushing something on the stack.
:class:`pyformlang.indexed_grammar.DuplicationRule`:
    A duplication rule, duplicating the stack.
:class:`pyformlang.indexed_grammar.CFGObject`:
    A general CFG object used in indexed grammars.
:class:`pyformlang.indexed_grammar.Variable`:
    A variable in indexed grammars.
:class:`pyformlang.indexed_grammar.Terminal`:
    A terminal in indexed grammars.
:class:`pyformlang.indexed_grammar.Epsilon`:
    An epsilon terminal.
"""

from .indexed_grammar import IndexedGrammar
from .rules import Rules
from .reduced_rule import ReducedRule
from .consumption_rule import ConsumptionRule
from .end_rule import EndRule
from .production_rule import ProductionRule
from .duplication_rule import DuplicationRule
from ..objects.cfg_objects import CFGObject, Variable, Terminal, Epsilon


__all__ = [
    "IndexedGrammar",
    "Rules",
    "ReducedRule",
    "ConsumptionRule",
    "EndRule",
    "ProductionRule",
    "DuplicationRule",
    "CFGObject",
    "Variable",
    "Terminal",
    "Epsilon",
]
