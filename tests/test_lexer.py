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
        )
    ],
)
def test_single_character_tokens(input, expected_tokens):
    lexer = Lexer(input)

    for expected_token in expected_tokens:
        token = lexer.next_token()
        assert token == expected_token
