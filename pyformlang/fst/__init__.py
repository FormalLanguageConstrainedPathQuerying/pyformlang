"""This module deals with finite state transducers.

:mod:`pyformlang.fst`
=====================

Available Classes
-----------------
:class:`pyformlang.fst.FST`:
    A Finite State Transducer.
:class:`pyformlang.fst.TransitionFunction`:
    A transition function in FST.
:class:`pyformlang.fst.State`:
    A state in FST.
:class:`pyformlang.fst.Symbol`:
    A symbol in FST.
:class:`pyformlang.fst.Epsilon`:
    An epsilon symbol.
"""

from .fst import FST, TransitionFunction, State, Symbol, Epsilon


__all__ = [
    "FST",
    "TransitionFunction",
    "State",
    "Symbol",
    "Epsilon",
]
