import pytest

from pymonkey.lexer import Lexer, Token, TokenType


@pytest.mark.parametrize(
    "input, expected_tokens",
    [
        (
            "=+(){},;",
            [
                Token(TokenType.ASSIGN, "="),
                Token(TokenType.PLUS, "+"),
                Token(TokenType.LPAREN, "("),
                Token(TokenType.RPAREN, ")"),
                Token(TokenType.LBRACE, "{"),
                Token(TokenType.RBRACE, "}"),
                Token(TokenType.COMMA, ","),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.EOF, ""),
            ],
        ),
        ("", [Token(TokenType.EOF, "")]),
        (
            """let five = 5;
let ten = 10;
   let add = fn(x, y) {
     x + y;
};
let result = add(five, ten);""",
            [
                Token(TokenType.LET, "let"),
                Token(TokenType.IDENT, "five"),
                Token(TokenType.ASSIGN, "="),
                Token(TokenType.INT, "5"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.LET, "let"),
                Token(TokenType.IDENT, "ten"),
                Token(TokenType.ASSIGN, "="),
                Token(TokenType.INT, "10"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.LET, "let"),
                Token(TokenType.IDENT, "add"),
                Token(TokenType.ASSIGN, "="),
                Token(TokenType.FUNCTION, "fn"),
                Token(TokenType.LPAREN, "("),
                Token(TokenType.IDENT, "x"),
                Token(TokenType.COMMA, ","),
                Token(TokenType.IDENT, "y"),
                Token(TokenType.RPAREN, ")"),
                Token(TokenType.LBRACE, "{"),
                Token(TokenType.IDENT, "x"),
                Token(TokenType.PLUS, "+"),
                Token(TokenType.IDENT, "y"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.RBRACE, "}"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.LET, "let"),
                Token(TokenType.IDENT, "result"),
                Token(TokenType.ASSIGN, "="),
                Token(TokenType.IDENT, "add"),
                Token(TokenType.LPAREN, "("),
                Token(TokenType.IDENT, "five"),
                Token(TokenType.COMMA, ","),
                Token(TokenType.IDENT, "ten"),
                Token(TokenType.RPAREN, ")"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.EOF, ""),
            ],
        ),
        (
            """!-/*5;
5 < 10 > 5;""",
            [
                Token(TokenType.BANG, "!"),
                Token(TokenType.MINUS, "-"),
                Token(TokenType.SLASH, "/"),
                Token(TokenType.ASTERISK, "*"),
                Token(TokenType.INT, "5"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.INT, "5"),
                Token(TokenType.LT, "<"),
                Token(TokenType.INT, "10"),
                Token(TokenType.GT, ">"),
                Token(TokenType.INT, "5"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.EOF, ""),
            ],
        ),
        (
            """10 == 10;
10 != 9;""",
            [
                Token(TokenType.INT, "10"),
                Token(TokenType.EQUAL_EQ, "=="),
                Token(TokenType.INT, "10"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.INT, "10"),
                Token(TokenType.BANG_EQ, "!="),
                Token(TokenType.INT, "9"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.EOF, ""),
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
