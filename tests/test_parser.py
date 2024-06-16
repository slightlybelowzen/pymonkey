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
def test_parse_let_statement(input: str, expected: list[str]):
    lexer = Lexer(input)
    parser = Parser(lexer)
    program = parser.parse_program()
    if not program:
        raise Exception("AST is empty")
    assert len(program.statements) == 3
    for i, expected_identifier in enumerate(expected):
        statement = program.statements[i]
        assert statement.token_literal() == "let"
        let_stmt = LetStatement(token=statement.token, identifier=statement.identifier)
        assert let_stmt.identifier.value == expected_identifier
        assert let_stmt.identifier.token_literal() == expected_identifier
