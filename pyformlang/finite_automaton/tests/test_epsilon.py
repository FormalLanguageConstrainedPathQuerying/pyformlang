"""
Tests for epsilon transitions
"""

from pyformlang.finite_automaton import Epsilon
from pyformlang.finite_automaton import State, Symbol


class TestEpsilon:
    """ Tests for epsilon transitions """

    def test_epsilon(self):
        """ Generic tests for epsilon """
        eps0 = Epsilon()
        eps1 = Epsilon()
        symb = Symbol(0)
        assert eps0 == eps1
        assert eps0 != symb
        assert "epsilon" == Epsilon()
        assert Epsilon() == "ɛ"
        assert Symbol("ɛ") != Epsilon()
        assert Epsilon() != State("epsilon")
