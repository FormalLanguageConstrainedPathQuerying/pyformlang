""" Tests the terminal """
from pyformlang.cfg import Variable, Terminal, Epsilon
from pyformlang.finite_automaton import State, Symbol, Epsilon as FAEpsilon


class TestTerminal:
    """ Tests the terminal """
    # pylint: disable=missing-function-docstring

    def test_creation(self):
        terminal0 = Terminal(0)
        terminal1 = Terminal(1)
        terminal2 = Terminal(0)
        terminal3 = Terminal("0")
        assert terminal0 == terminal2
        assert terminal0 != terminal1
        assert terminal0 != terminal3
        assert hash(terminal0) == hash(terminal2)
        assert hash(terminal0) != hash(terminal1)
        assert str(terminal0) == str(terminal2)
        assert str(terminal0) == str(terminal3)
        assert str(terminal0) != str(terminal1)
        epsilon = Epsilon()
        assert epsilon.to_text() == "epsilon"
        assert Terminal("C").to_text() == '"TER:C"'
        assert repr(Epsilon()) == "epsilon"

    def test_eq(self):
        assert "epsilon" == Epsilon()
        assert Epsilon() == "ɛ"
        assert Terminal("A") != Variable("A")
        assert Variable("S") == Variable("S")
        assert Terminal("A") != Terminal("B")
        assert "A" == Terminal("A")
        assert Variable(1) == 1
        assert Epsilon() == FAEpsilon()
        assert Terminal("ABC") != Symbol("ABC")
        assert State("S") != Variable("S")
