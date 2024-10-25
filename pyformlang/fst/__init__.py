"""
:mod:`pyformlang.fst`
=====================

This module deals with finite state transducers.

Available Classes
-----------------

FST
    A Finite State Transducer

"""

from .fst import FST, State, Symbol, Epsilon


__all__ = ["FST",
           "State",
           "Symbol",
           "Epsilon"]
