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
            """let five = 5;
let ten = 10;
   let add = fn(x, y) {
     x + y;
};
let result = add(five, ten);
!-/*5;
5 < 10 > 5;""",
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
            """let five = 5;
let ten = 10;
let add = fn(x, y) {
    x + y;
};
let result = add(five, ten);
!-/*5;
5 < 10 > 5;
if (5 < 10) {
    return true;
} else {
    return false;
}""",
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
                Token(TokenType.IF, "if"),
                Token(TokenType.LPAREN, "("),
                Token(TokenType.INT, "5"),
                Token(TokenType.LT, "<"),
                Token(TokenType.INT, "10"),
                Token(TokenType.RPAREN, ")"),
                Token(TokenType.LBRACE, "{"),
                Token(TokenType.RETURN, "return"),
                Token(TokenType.TRUE, "true"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.RBRACE, "}"),
                Token(TokenType.ELSE, "else"),
                Token(TokenType.LBRACE, "{"),
                Token(TokenType.RETURN, "return"),
                Token(TokenType.FALSE, "false"),
                Token(TokenType.SEMICOLON, ";"),
                Token(TokenType.RBRACE, "}"),
                Token(TokenType.EOF, ""),
            ],
        ),
    ],
)
def test_lexer(input, expected_tokens):
    lexer = Lexer(input)

    for expected_token in expected_tokens:
        token = lexer.next_token()
        assert token == expected_token
