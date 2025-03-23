"""
Pyformlang
==========
Pyformlang is a python module to perform operation on formal languages.
How to use the documentation
----------------------------
Documentation is available in two formats: docstrings directly
in the code and a readthedocs website: https://pyformlang.readthedocs.io.
Available subpackages
---------------------
regular_expression
    Regular Expressions
finite_automaton
    Finite automata (deterministic, non-deterministic, with/without epsilon
    transitions
fst
    Finite State Transducers
cfg
    Context-Free Grammar
pda
    Push-Down Automata
Indexed Grammar
    Indexed Grammar
rsa
    Recursive automaton

"""

from . import finite_automaton
from . import regular_expression
from . import cfg
from . import fst
from . import indexed_grammar
from . import pda
from . import rsa
from . import fcfg


__all__ = ["finite_automaton",
           "regular_expression",
           "cfg",
           "fst",
           "indexed_grammar",
           "pda",
           "rsa",
           "fcfg"]
