"""Pyformlang is a python module to perform operation on formal languages.

How to use the documentation
----------------------------
Documentation is available in two formats: docstrings directly
in the code and a readthedocs website: https://pyformlang.readthedocs.io.

Available subpackages
---------------------
:mod:`pyformlang.regular_expression`:
    Regular Expressions.
:mod:`pyformlang.finite_automaton`:
    Finite Automata (deterministic, non-deterministic,
    with/without epsilon transitions).
:mod:`pyformlang.fst`:
    Finite State Transducers.
:mod:`pyformlang.cfg`:
    Context-Free Grammars.
:mod:`pyformlang.pda`:
    Push-Down Automata.
:mod:`pyformlang.indexed_grammar`:
    Indexed Grammars.
:mod:`pyformlang.rsa`:
    Recursive Automata.
:mod:`pyformlang.fcfg`:
    Context-Free Grammars with Features.
"""

from . import finite_automaton
from . import regular_expression
from . import cfg
from . import fst
from . import indexed_grammar
from . import pda
from . import rsa
from . import fcfg


__all__ = [
    "finite_automaton",
    "regular_expression",
    "cfg",
    "fst",
    "indexed_grammar",
    "pda",
    "rsa",
    "fcfg",
]
