from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # identifiers, literals
    IDENT = "IDENT"
    INT = "INT"
    STRING = "STRING"

    # operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"
    LT = "<"
    GT = ">"
    EQ = "=="
    NOT_EQ = "!="

    # delimiters
    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # keywords
    FUNCTION = "FUNCTION"
    LET = "LET"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"

    def __repr__(self) -> str:
        return f"TokenType.{self.name}"

    @staticmethod
    def lookup_identifier(identifier: str) -> TokenType:
        match identifier:
            case "fn":
                return TokenType.FUNCTION
            case "let":
                return TokenType.LET
            case "true":
                return TokenType.TRUE
            case "false":
                return TokenType.FALSE
            case "if":
                return TokenType.IF
            case "else":
                return TokenType.ELSE
            case "return":
                return TokenType.RETURN
            case _:
                return TokenType.IDENT


@dataclass
class Token:
    type: TokenType
    literal: str | None = None
    position: int = 0


class Lexer:
    def __init__(self, input: str, position: int, character: str | None):
        self.input: str = input
        self.position: int = position
        self.character: str | None = character

    def __repr__(self) -> str:
        return f"Lexer(\n  position={self.position},\n  character={self.character!r}\n)"

    def next_token(self) -> tuple[Lexer, Token | None]:
        lexer = self.skip_whitespace()
        ch = lexer.character
        match ch:
            case None:
                return self, None
            case ";":
                return lexer.advance(), Token(
                    type=TokenType.SEMICOLON, literal=";", position=lexer.position
                )
            case "+":
                return lexer.advance(), Token(
                    type=TokenType.PLUS, literal="+", position=lexer.position
                )
            case "(":
                return lexer.advance(), Token(
                    type=TokenType.LPAREN, literal="(", position=lexer.position
                )
            case ")":
                return lexer.advance(), Token(
                    type=TokenType.RPAREN, literal=")", position=lexer.position
                )
            case "{":
                return lexer.advance(), Token(
                    type=TokenType.LBRACE, literal="{", position=lexer.position
                )
            case "}":
                return lexer.advance(), Token(
                    type=TokenType.RBRACE, literal="}", position=lexer.position
                )
            case ",":
                return lexer.advance(), Token(
                    type=TokenType.COMMA, literal=",", position=lexer.position
                )
            case "<":
                return lexer.advance(), Token(
                    type=TokenType.LT, literal="<", position=lexer.position
                )
            case ">":
                return lexer.advance(), Token(
                    type=TokenType.GT, literal=">", position=lexer.position
                )
            case "/":
                return lexer.advance(), Token(
                    type=TokenType.SLASH, literal="/", position=lexer.position
                )
            case "*":
                return lexer.advance(), Token(
                    type=TokenType.ASTERISK, literal="*", position=lexer.position
                )
            case "-":
                return lexer.advance(), Token(
                    type=TokenType.MINUS, literal="-", position=lexer.position
                )
            case "!":
                return lexer.match_peek("=", TokenType.NOT_EQ, TokenType.BANG)
            case "=":
                return lexer.match_peek("=", TokenType.EQ, TokenType.ASSIGN)
            case '"':
                return lexer.read_string()
            case ch if ch.isalpha():
                return lexer.read_identifier()
            case ch if ch.isdigit():
                return lexer.read_number()
            case _:
                return lexer.advance(), Token(
                    type=TokenType.ILLEGAL,
                    literal=lexer.character,
                    position=lexer.position,
                )

    def match_peek(
        self, expected_ch: str, default: TokenType, alternative: TokenType
    ) -> tuple[Lexer, Token]:
        lexer = self
        ch = lexer.character
        position = lexer.position
        if lexer.peek() == expected_ch:
            lexer = lexer.advance()
            return lexer.advance(), Token(
                type=default,
                literal="".join([ch, expected_ch]),
                position=position
            )
        return lexer.advance(), Token(
            type=alternative,
            literal=lexer.character,
            position=position,
        )

    def read_string(self) -> tuple[Lexer, Token | None]:
        lexer = self
        position = lexer.position
        # skip the first "
        lexer = lexer.advance()
        lexer, string = lexer.read_while(lambda ch: ch != '"')
        # skip the final "
        lexer = lexer.advance()
        return lexer, Token(type=TokenType.STRING, literal=string, position=position)

    def read_while(self, condition: Callable[[str], bool]) -> tuple[Lexer, str]:
        lexer = self
        start = lexer.position
        lexer, end = self.seek(condition)
        return lexer, self.input[start:end]

    def read_identifier(self) -> tuple[Lexer, Token | None]:
        position = self.position
        lexer, identifier = self.read_while(lambda ch: ch.isalpha() or ch == "_")
        return lexer, Token(
            type=TokenType.lookup_identifier(identifier),
            literal=identifier,
            position=position,
        )

    def read_number(self) -> tuple[Lexer, Token | None]:
        position = self.position
        lexer, number = self.read_while(lambda ch: ch.isdigit())
        return lexer, Token(type=TokenType.INT, literal=number, position=position)

    def advance(self) -> Lexer:
        if self.position >= len(self.input) - 1:
            return Lexer(self.input, self.position, None)
        pos = self.position + 1
        return Lexer(self.input, pos, self.input[pos])

    def seek(self, condition: Callable[[str], bool]) -> tuple[Lexer, int]:
        lexer = self
        while condition(lexer.character):
            lexer = lexer.advance()
            if lexer.character is None:
                # not sure about this, should it always be +1?
                return lexer, lexer.position + 1
        return lexer, lexer.position

    def peek(self) -> str | None:
        if self.position >= len(self.input) - 1:
            return None
        return self.input[self.position + 1]

    def skip_whitespace(self) -> Lexer:
        lexer, _ = self.seek(lambda ch: ch.isspace())
        return lexer
