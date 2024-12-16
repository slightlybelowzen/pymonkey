from src.ast import LetStatement, Program
from src.lexer import Lexer
from src.parser import Parser


def input_to_ast(input: str) -> Program:
    lexer = Lexer(input)
    parser = Parser(lexer)
    return parser.parse_program()

def check_let_statement(ast: Program, expected_identifiers: list[str], expected_values: list[str]) -> bool:
    print(ast)
    if len(ast.statements) != len(expected_identifiers):
        return False
    for i, statement in enumerate(ast.statements):
        assert isinstance(statement, LetStatement)
        assert statement.name.value == expected_identifiers[i]
        # assert statement.value == expected_values[i]
    return True


def test_let_statements():
    input = "let x = 5; let y = 10;"
    ast = input_to_ast(input)
    assert check_let_statement(ast, ["x", "y"], ["5", "10"])
