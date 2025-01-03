"""Testing the rules."""

from pyformlang.indexed_grammar import ProductionRule
from pyformlang.indexed_grammar import DuplicationRule
from pyformlang.indexed_grammar import Rules
from pyformlang.indexed_grammar import ConsumptionRule
from pyformlang.indexed_grammar import EndRule
from pyformlang.indexed_grammar.tests.test_indexed_grammar import (
    get_example_rules,
)


class TestIndexedGrammar:
    """Tests things related to rules."""

    # pylint: disable=missing-function-docstring

    def test_consumption_rules(self) -> None:
        """Tests the consumption rules."""
        consumption = ConsumptionRule("end", "C", "T")
        terminals = consumption.terminals
        assert terminals == {"end"}
        representation = str(consumption)
        assert representation == "C [ end ] -> T"

    def test_duplication_rules(self) -> None:
        """Tests the duplication rules."""
        duplication = DuplicationRule("B0", "A0", "C")
        assert duplication.terminals == set()
        assert str(duplication) == "B0 -> A0 C"

    def test_end_rule(self) -> None:
        """Tests the end rules."""
        end_rule = EndRule("A0", "b")
        assert end_rule.terminals == {"b"}
        assert end_rule.right_term == "b"
        assert str(end_rule) == "A0 -> b"

    def test_production_rules(self) -> None:
        """Tests the production rules."""
        production = ProductionRule("S", "C", "end")
        assert production.terminals == {"end"}
        assert str(production) == "S -> C [ end ]"

    def test_rules(self) -> None:
        """Tests the rules."""
        l_rules = get_example_rules()
        rules = Rules(l_rules)
        assert rules.terminals == {"b", "end", "epsilon"}
        assert rules.length == (5, 2)
        rules.remove_production("S", "Cinit", "end")
        assert rules.length == (4, 2)
        rules.add_production("S", "Cinit", "end")
        assert rules.length == (5, 2)
