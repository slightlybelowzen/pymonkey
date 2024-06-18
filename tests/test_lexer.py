import pytest

from pymonkey.lexer import Lexer, Token, TokenType


@pytest.mark.parametrize(
    "input, expected_tokens",
    [
        (
            "=+(){},;",
            [
                Token(TokenType.ASSIGN, "=", line=1),
                Token(TokenType.PLUS, "+", line=1),
                Token(TokenType.LPAREN, "(", line=1),
                Token(TokenType.RPAREN, ")", line=1),
                Token(TokenType.LBRACE, "{", line=1),
                Token(TokenType.RBRACE, "}", line=1),
                Token(TokenType.COMMA, ",", line=1),
                Token(TokenType.SEMICOLON, ";", line=1),
                Token(TokenType.EOF, "", line=1),
            ],
        ),
        ("", [Token(TokenType.EOF, "", line=1)]),
        (
            """let five = 5;
let ten = 10;
let add = fn(x, y) {
    x + y;
};
let result = add(five, ten);""",
            [
                Token(TokenType.LET, "let", line=1),
                Token(TokenType.IDENT, "five", line=1),
                Token(TokenType.ASSIGN, "=", line=1),
                Token(TokenType.INT, "5", line=1),
                Token(TokenType.SEMICOLON, ";", line=1),
                Token(TokenType.LET, "let", line=2),
                Token(TokenType.IDENT, "ten", line=2),
                Token(TokenType.ASSIGN, "=", line=2),
                Token(TokenType.INT, "10", line=2),
                Token(TokenType.SEMICOLON, ";", line=2),
                Token(TokenType.LET, "let", line=3),
                Token(TokenType.IDENT, "add", line=3),
                Token(TokenType.ASSIGN, "=", line=3),
                Token(TokenType.FUNCTION, "fn", line=3),
                Token(TokenType.LPAREN, "(", line=3),
                Token(TokenType.IDENT, "x", line=3),
                Token(TokenType.COMMA, ",", line=3),
                Token(TokenType.IDENT, "y", line=3),
                Token(TokenType.RPAREN, ")", line=3),
                Token(TokenType.LBRACE, "{", line=3),
                Token(TokenType.IDENT, "x", line=4),
                Token(TokenType.PLUS, "+", line=4),
                Token(TokenType.IDENT, "y", line=4),
                Token(TokenType.SEMICOLON, ";", line=4),
                Token(TokenType.RBRACE, "}", line=5),
                Token(TokenType.SEMICOLON, ";", line=5),
                Token(TokenType.LET, "let", line=6),
                Token(TokenType.IDENT, "result", line=6),
                Token(TokenType.ASSIGN, "=", line=6),
                Token(TokenType.IDENT, "add", line=6),
                Token(TokenType.LPAREN, "(", line=6),
                Token(TokenType.IDENT, "five", line=6),
                Token(TokenType.COMMA, ",", line=6),
                Token(TokenType.IDENT, "ten", line=6),
                Token(TokenType.RPAREN, ")", line=6),
                Token(TokenType.SEMICOLON, ";", line=6),
                Token(TokenType.EOF, "", line=6),
            ],
        ),
        (
            """!-/*5;
5 < 10 > 5;""",
            [
                Token(TokenType.BANG, "!", line=1),
                Token(TokenType.MINUS, "-", line=1),
                Token(TokenType.SLASH, "/", line=1),
                Token(TokenType.ASTERISK, "*", line=1),
                Token(TokenType.INT, "5", line=1),
                Token(TokenType.SEMICOLON, ";", line=1),
                Token(TokenType.INT, "5", line=2),
                Token(TokenType.LT, "<", line=2),
                Token(TokenType.INT, "10", line=2),
                Token(TokenType.GT, ">", line=2),
                Token(TokenType.INT, "5", line=2),
                Token(TokenType.SEMICOLON, ";", line=2),
                Token(TokenType.EOF, "", line=2),
            ],
        ),
        (
            """10 == 10;
10 != 9;""",
            [
                Token(TokenType.INT, "10", line=1),
                Token(TokenType.EQUAL_EQ, "==", line=1),
                Token(TokenType.INT, "10", line=1),
                Token(TokenType.SEMICOLON, ";", line=1),
                Token(TokenType.INT, "10", line=2),
                Token(TokenType.BANG_EQ, "!=", line=2),
                Token(TokenType.INT, "9", line=2),
                Token(TokenType.SEMICOLON, ";", line=2),
                Token(TokenType.EOF, "", line=2),
            ],
        ),
    ],
    ids=["simple", "simple-with-fn", "simple-with-ops", "if-else", "peek-ops"],
)
def test_lexer(input, expected_tokens):
    lexer = Lexer(input)

    for expected_token in expected_tokens:
        token = lexer.next_token()
        assert token == expected_token
