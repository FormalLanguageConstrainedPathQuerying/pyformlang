"""This module deals with recursive automata.

:mod:`pyformlang.rsa`
=====================

Available Classes
-----------------
:class:`pyformlang.rsa.RecursiveAutomaton`:
    A recursive automaton.
:class:`pyformlang.rsa.Box`:
    A constituent part of a recursive automaton.

References
----------
[1] Alur R., Etessami K., Yannakakis M. (2001) Analysis of \
Recursive State Machines. In: Berry G.,
Comon H., Finkel A. (eds) Computer Aided Verification. CAV 2001.
Lecture Notes in Computer Science, vol 2102.
Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44585-4_18
"""

from .recursive_automaton import RecursiveAutomaton
from .box import Box


__all__ = [
    "RecursiveAutomaton",
    "Box",
]
