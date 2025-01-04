"""Tests for recursive top-down parser."""

import pytest

from pyformlang.cfg import CFG, Variable, Terminal
from pyformlang.cfg.recursive_decent_parser import (
    RecursiveDecentParser,
    NotParsableError,
)


@pytest.fixture
def parser() -> RecursiveDecentParser:
    cfg = CFG.from_text("""
                E -> S + S
                E -> S * S
                S -> ( E )
                S -> int
            """)
    return RecursiveDecentParser(cfg)


class TestRecursiveDecentParser:
    def test_creation(self, parser) -> None:
        assert parser is not None

    def test_get_parsing_tree(self, parser) -> None:
        assert parser.is_parsable(
            ["(", "int", "+", "(", "int", "*", "int", ")", ")"]
        )
        parse_tree = parser.get_parse_tree(
            ["(", "int", "+", "(", "int", "*", "int", ")", ")"]
        )
        derivation = parse_tree.get_leftmost_derivation()
        assert derivation == [
            [Variable("S")],
            [Terminal("("), Variable("E"), Terminal(")")],
            [
                Terminal("("),
                Variable("S"),
                Terminal("+"),
                Variable("S"),
                Terminal(")"),
            ],
            [
                Terminal("("),
                Terminal("int"),
                Terminal("+"),
                Variable("S"),
                Terminal(")"),
            ],
            [
                Terminal("("),
                Terminal("int"),
                Terminal("+"),
                Terminal("("),
                Variable("E"),
                Terminal(")"),
                Terminal(")"),
            ],
            [
                Terminal("("),
                Terminal("int"),
                Terminal("+"),
                Terminal("("),
                Variable("S"),
                Terminal("*"),
                Variable("S"),
                Terminal(")"),
                Terminal(")"),
            ],
            [
                Terminal("("),
                Terminal("int"),
                Terminal("+"),
                Terminal("("),
                Terminal("int"),
                Terminal("*"),
                Variable("S"),
                Terminal(")"),
                Terminal(")"),
            ],
            [
                Terminal("("),
                Terminal("int"),
                Terminal("+"),
                Terminal("("),
                Terminal("int"),
                Terminal("*"),
                Terminal("int"),
                Terminal(")"),
                Terminal(")"),
            ],
        ]

    def test_no_parse_tree(self, parser) -> None:
        with pytest.raises(NotParsableError):
            parser.get_parse_tree([")"])
        assert not (parser.is_parsable([")"]))

    def test_infinite_recursion(self) -> None:
        cfg = CFG.from_text("""
            S -> S E
        """)
        parser = RecursiveDecentParser(cfg)
        with pytest.raises(RecursionError):
            parser.is_parsable([")"])
        assert not parser.is_parsable([")"], left=False)
