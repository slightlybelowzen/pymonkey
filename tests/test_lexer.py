import pprint
from src.lexer import Lexer, Token, TokenType


def input_to_tokens(input: str) -> list[Token]:
    lexer = Lexer(input)
    tokens: list[Token] = []
    next_token = lexer.next_token()
    while next_token.type != TokenType.EOF:
        tokens.append(next_token)
        next_token = lexer.next_token()
    pprint.pprint(tokens)
    return tokens


def test_identifiers():
    assert input_to_tokens("x") == [
        Token(type=TokenType.IDENT, literal="x", position=0)
    ]
    assert input_to_tokens("foo bar") == [
        Token(type=TokenType.IDENT, literal="foo", position=0),
        Token(type=TokenType.IDENT, literal="bar", position=4),
    ]


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
        Token(type=TokenType.ASSIGN, literal="=", position=9),
        Token(type=TokenType.INT, literal=5, position=11),
        Token(type=TokenType.SEMICOLON, literal=";", position=12),
        Token(type=TokenType.LET, literal="let", position=14),
        Token(type=TokenType.IDENT, literal="ten", position=18),
        Token(type=TokenType.ASSIGN, literal="=", position=22),
        Token(type=TokenType.INT, literal=10, position=24),
        Token(type=TokenType.SEMICOLON, literal=";", position=26),
        Token(type=TokenType.LET, literal="let", position=28),
        Token(type=TokenType.IDENT, literal="add", position=32),
        Token(type=TokenType.ASSIGN, literal="=", position=36),
        Token(type=TokenType.FUNCTION, literal="fn", position=38),
        Token(type=TokenType.LPAREN, literal="(", position=40),
        Token(type=TokenType.IDENT, literal="x", position=41),
        Token(type=TokenType.COMMA, literal=",", position=42),
        Token(type=TokenType.IDENT, literal="y", position=44),
        Token(type=TokenType.RPAREN, literal=")", position=45),
        Token(type=TokenType.LBRACE, literal="{", position=47),
        Token(type=TokenType.IDENT, literal="x", position=49),
        Token(type=TokenType.PLUS, literal="+", position=51),
        Token(type=TokenType.IDENT, literal="y", position=53),
        Token(type=TokenType.SEMICOLON, literal=";", position=54),
        Token(type=TokenType.RBRACE, literal="}", position=56),
        Token(type=TokenType.SEMICOLON, literal=";", position=57),
        Token(type=TokenType.LET, literal="let", position=59),
        Token(type=TokenType.IDENT, literal="result", position=63),
        Token(type=TokenType.ASSIGN, literal="=", position=70),
        Token(type=TokenType.IDENT, literal="add", position=72),
        Token(type=TokenType.LPAREN, literal="(", position=75),
        Token(type=TokenType.IDENT, literal="five", position=76),
        Token(type=TokenType.COMMA, literal=",", position=80),
        Token(type=TokenType.IDENT, literal="ten", position=82),
        Token(type=TokenType.RPAREN, literal=")", position=85),
        Token(type=TokenType.SEMICOLON, literal=";", position=86),
    ]


def test_operators():
    assert input_to_tokens("!-/*5; 5 < 10 > 5;") == [
        Token(type=TokenType.BANG, literal="!", position=0),
        Token(type=TokenType.MINUS, literal="-", position=1),
        Token(type=TokenType.SLASH, literal="/", position=2),
        Token(type=TokenType.ASTERISK, literal="*", position=3),
        Token(type=TokenType.INT, literal=5, position=4),
        Token(type=TokenType.SEMICOLON, literal=";", position=5),
        Token(type=TokenType.INT, literal=5, position=7),
        Token(type=TokenType.LT, literal="<", position=9),
        Token(type=TokenType.INT, literal=10, position=11),
        Token(type=TokenType.GT, literal=">", position=14),
        Token(type=TokenType.INT, literal=5, position=16),
        Token(type=TokenType.SEMICOLON, literal=";", position=17),
    ]


def test_if_statements():
    input = "if (5 < 10) { return true; } else { return false; }"
    assert input_to_tokens(input) == [
        Token(type=TokenType.IF, literal="if", position=0),
        Token(type=TokenType.LPAREN, literal="(", position=3),
        Token(type=TokenType.INT, literal=5, position=4),
        Token(type=TokenType.LT, literal="<", position=6),
        Token(type=TokenType.INT, literal=10, position=8),
        Token(type=TokenType.RPAREN, literal=")", position=10),
        Token(type=TokenType.LBRACE, literal="{", position=12),
        Token(type=TokenType.RETURN, literal="return", position=14),
        Token(type=TokenType.TRUE, literal="true", position=21),
        Token(type=TokenType.SEMICOLON, literal=";", position=25),
        Token(type=TokenType.RBRACE, literal="}", position=27),
        Token(type=TokenType.ELSE, literal="else", position=29),
        Token(type=TokenType.LBRACE, literal="{", position=34),
        Token(type=TokenType.RETURN, literal="return", position=36),
        Token(type=TokenType.FALSE, literal="false", position=43),
        Token(type=TokenType.SEMICOLON, literal=";", position=48),
        Token(type=TokenType.RBRACE, literal="}", position=50),
    ]


def test_string_literals():
    assert input_to_tokens('"hello", "world"') == [
        Token(type=TokenType.STRING, literal="hello", position=0),
        Token(type=TokenType.COMMA, literal=",", position=7),
        Token(type=TokenType.STRING, literal="world", position=9),
    ]


def test_equality_operators():
    assert input_to_tokens("5 != 5") == [
        Token(type=TokenType.INT, literal=5, position=0),
        Token(type=TokenType.NOT_EQ, literal="!=", position=2),
        Token(type=TokenType.INT, literal=5, position=5),
    ]
