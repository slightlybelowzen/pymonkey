import pytest

from pymonkey.ast import LetStatement
from pymonkey.lexer import Lexer
from pymonkey.parser import Parser


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            """let five = 5;
let ten = 10;
let foobar = 838838;""",
            ["five", "ten", "foobar"],
        ),
    ],
    ids=["simple-let-statements"],
)
def test_parse_let_statement_identifiers(input: str, expected: list[str]):
    lexer = Lexer(input)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.statements) == 3
    for i, expected_identifier in enumerate(expected):
        statement = program.statements[i]
        assert statement.token_literal() == "let"
        let_stmt = LetStatement(token=statement.token, identifier=statement.identifier)
        assert let_stmt.identifier.value == expected_identifier
        assert let_stmt.identifier.token_literal() == expected_identifier


@pytest.mark.parametrize(
    "input",
    [
        (
            """return 5;
return 10;
return 838838;""",
        ),
    ],
    ids=["simple-return-statements"],
)
def test_parse_return_statement(input: str):
    lexer = Lexer(input)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.statements) == 3
    for statement in program.statements:
        assert statement.token_literal() == "return"
