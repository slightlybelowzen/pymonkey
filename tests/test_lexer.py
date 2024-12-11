import pytest
from src.lexer import Lexer, Token, TokenType


def input_to_tokens(input: str) -> list[Token]:
    lexer = Lexer(input, position=0, character=input[0] if len(input) > 0 else None)
    tokens = []
    while lexer.character is not None:
        match lexer.next_token():
            case _, None:
                return tokens
            case lexer, token:
                tokens.append(token)
    return tokens

def test_identifiers():
    assert input_to_tokens("x") == [Token(type=TokenType.IDENT, literal="x", position=0)]
    # assert input_to_tokens("foo bar") == [
    #     Token(type=TokenType.IDENT, literal="foo", position=0),
    #     Token(type=TokenType.IDENT, literal="bar", position=4),
    # ]

def test_single_character_tokens():
    assert input_to_tokens("=+(){},;") == [
        Token(type=TokenType.ASSIGN, literal="=", position=0),
        Token(type=TokenType.PLUS, literal="+", position=1),
        Token(type=TokenType.LPAREN, literal="(", position=2),
        Token(type=TokenType.RPAREN, literal=")", position=3),
        Token(type=TokenType.LBRACE, literal="{", position=4),
        Token(type=TokenType.RBRACE, literal="}", position=5),
        Token(type=TokenType.COMMA, literal=",", position=6),
        Token(type=TokenType.SEMICOLON, literal=";", position=7),
    ]

@pytest.mark.skip(reason="Not implemented")
def test_monkey_program():
    input = """let five = 5;
let ten = 10;
let add = fn(x, y) {
x + y;
};
let result = add(five, ten);"""
    assert input_to_tokens(input) == [
        Token(type=TokenType.LET, literal="let", position=0),
        Token(type=TokenType.IDENT, literal="five", position=4),
        Token(type=TokenType.ASSIGN, literal="=", position=8),
        Token(type=TokenType.INT, literal="5", position=10),
        Token(type=TokenType.SEMICOLON, literal=";", position=11),
        Token(type=TokenType.LET, literal="let", position=13),
        Token(type=TokenType.IDENT, literal="ten", position=17),
        Token(type=TokenType.ASSIGN, literal="=", position=21),
        Token(type=TokenType.INT, literal="10", position=23),
        Token(type=TokenType.SEMICOLON, literal=";", position=24),
        Token(type=TokenType.LET, literal="let", position=26),
        Token(type=TokenType.IDENT, literal="add", position=30),
        Token(type=TokenType.ASSIGN, literal="=", position=34),
        Token(type=TokenType.FUNCTION, literal="fn", position=36),
        Token(type=TokenType.LPAREN, literal="(", position=40),
        Token(type=TokenType.IDENT, literal="x", position=41),
        Token(type=TokenType.COMMA, literal=",", position=43),
        Token(type=TokenType.IDENT, literal="y", position=45),
        Token(type=TokenType.RPAREN, literal=")", position=46),
        Token(type=TokenType.LBRACE, literal="{", position=47),
        Token(type=TokenType.IDENT, literal="x", position=51),
        Token(type=TokenType.PLUS, literal="+", position=53),
        Token(type=TokenType.IDENT, literal="y", position=55),
        Token(type=TokenType.SEMICOLON, literal=";", position=56),
        Token(type=TokenType.RBRACE, literal="}", position=57),
        Token(type=TokenType.SEMICOLON, literal=";", position=58),
        Token(type=TokenType.LET, literal="let", position=60),
        Token(type=TokenType.IDENT, literal="result", position=64),
        Token(type=TokenType.ASSIGN, literal="=", position=68),
        Token(type=TokenType.IDENT, literal="add", position=70),
        Token(type=TokenType.LPAREN, literal="(", position=72),
        Token(type=TokenType.IDENT, literal="five", position=73),
        Token(type=TokenType.COMMA, literal=",", position=75),
        Token(type=TokenType.IDENT, literal="ten", position=77),
        Token(type=TokenType.RPAREN, literal=")", position=80),
        Token(type=TokenType.SEMICOLON, literal=";", position=81),
    ]
