import pytest
from src.parser import ParserError
from src.ast import LetStatement, Program
from contextlib import nullcontext as does_not_raise
from src.lexer import Lexer
from src.parser import Parser


def input_to_ast(input: str) -> Program:
    lexer = Lexer(input)
    parser = Parser(lexer)
    return parser.parse_program()


def check_let_statement(
    ast: Program, expected_identifiers: list[str], expected_values: list[str]
) -> bool:
    if len(ast.statements) != len(expected_identifiers):
        return False
    for i, statement in enumerate(ast.statements):
        assert isinstance(statement, LetStatement)
        assert statement.name.value == expected_identifiers[i]
        # TODO: uncomment this once we have expression parsing working
        # assert statement.value == expected_values[i]
    return True


@pytest.mark.parametrize(
    "input, expected_identifiers, expected_values, expectation",
    [
        ("let x = 5;", ["x"], ["5"], does_not_raise()),
        ("let x = 5; let y = 10;", ["x", "y"], ["5", "10"], does_not_raise()),
        ("let x = 5; let y = x + 10;", ["x", "y"], ["5", "x + 10"], does_not_raise()),
        ("let x 5;", ["x"], ["5"], pytest.raises(ParserError)),
    ],
)
# haven't quite figured out how to type the expectation parameter correctly
def test_let_statements(
    input: str,
    expected_identifiers: list[str],
    expected_values: list[str],
    expectation,  # type: ignore
):
    with expectation:
        ast = input_to_ast(input)
        assert check_let_statement(ast, expected_identifiers, expected_values)
