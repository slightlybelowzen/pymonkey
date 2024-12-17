import pytest
from src.parser import ParserError
from src.ast import (
    ExpressionStatement,
    Identifier,
    IntegerLiteral,
    LetStatement,
    PrefixExpression,
    Program,
    ReturnStatement,
)
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


def check_return_statement(ast: Program, expected_values: list[str]) -> bool:
    assert len(ast.statements) == len(expected_values)
    for _, statement in enumerate(ast.statements):
        assert isinstance(statement, ReturnStatement)
        assert statement.token_literal() == "return"
        # assert statement.return_value.value == expected_values[i]
    return True


def check_identifier_statements(ast: Program, expected_identifiers: list[str]) -> bool:
    assert len(ast.statements) == len(expected_identifiers)
    for i, statement in enumerate(ast.statements):
        assert isinstance(statement, ExpressionStatement)
        assert isinstance(statement.expression, Identifier)
        assert statement.expression.value == expected_identifiers[i]
    return True


def check_integer_literal_statements(ast: Program, expected_values: list[str]) -> bool:
    assert len(ast.statements) == len(expected_values)
    for i, statement in enumerate(ast.statements):
        assert isinstance(statement, ExpressionStatement)
        assert isinstance(statement.expression, IntegerLiteral)
        assert statement.expression.value == int(expected_values[i])
    return True


def check_prefix_expressions(
    ast: Program, expected_operator: str, expected_value: int
) -> bool:
    assert len(ast.statements) == 1
    print(ast)
    for statement in ast.statements:
        assert isinstance(statement, ExpressionStatement)
        assert isinstance(statement.expression, PrefixExpression)
        assert statement.expression.operator == expected_operator
        assert statement.expression.right.token_literal() == expected_value
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


@pytest.mark.parametrize(
    "input, expected_values, expectation",
    [
        ("return 5;", ["5"], does_not_raise()),
        ("return 5; return 10;", ["5", "10"], does_not_raise()),
    ],
)
def test_return_statements(
    input: str,
    expected_values: list[str],
    expectation,  # type: ignore
):
    with expectation:
        ast = input_to_ast(input)
        assert check_return_statement(ast, expected_values)


@pytest.mark.parametrize(
    "input, expected_identifiers, expectation",
    [
        ("foobar;", ["foobar"], does_not_raise()),
        ("x;", ["x"], does_not_raise()),
    ],
)
def test_identifier_expressions(
    input: str,
    expected_identifiers: list[str],
    expectation,  # type: ignore
):
    with expectation:
        ast = input_to_ast(input)
        assert check_identifier_statements(ast, expected_identifiers)


@pytest.mark.parametrize(
    "input, expected_values, expectation",
    [
        ("5;", ["5"], does_not_raise()),
        ("10;", ["10"], does_not_raise()),
    ],
)
def test_integer_literal_expressions(
    input: str,
    expected_values: list[str],
    expectation,  # type: ignore
):
    with expectation:
        ast = input_to_ast(input)
        assert check_integer_literal_statements(ast, expected_values)


@pytest.mark.parametrize(
    "input, expected_operator, expected_value, expectation",
    [
        ("!5;", "!", 5, does_not_raise()),
        ("-15;", "-", 15, does_not_raise()),
    ],
)
def test_prefix_expressions(
    input: str,
    expected_operator: str,
    expected_value: int,
    expectation,  # type: ignore
):
    with expectation:
        ast = input_to_ast(input)
        assert check_prefix_expressions(ast, expected_operator, expected_value)
