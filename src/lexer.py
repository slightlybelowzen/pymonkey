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

    # operators
    ASSIGN = "="
    PLUS = "+"

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

    def __repr__(self) -> str:
        return f"TokenType.{self.name}"

    @staticmethod
    def lookup_identifier(identifier: str) -> TokenType:
        match identifier:
            case "fn":
                return TokenType.FUNCTION
            case "let":
                return TokenType.LET
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
            case "=":
                return lexer.advance(), Token(
                    type=TokenType.ASSIGN, literal="=", position=lexer.position
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

    def read_while(self, condition: Callable[[str], bool]) -> tuple[Lexer, str]:
        lexer = self
        start = lexer.position
        lexer, end = self.seek(condition)
        return lexer, self.input[start:end]

    def read_identifier(self) -> tuple[Lexer, Token | None]:
        position = self.position
        lexer, identifier = self.read_while(self.is_identifier)
        return lexer, Token(
            type=TokenType.lookup_identifier(identifier),
            literal=identifier,
            position=position,
        )

    def read_number(self) -> tuple[Lexer, Token | None]:
        position = self.position
        lexer, number = self.read_while(self.is_digit)
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

    def skip_whitespace(self) -> Lexer:
        lexer, _ = self.seek(self.is_whitespace)
        return lexer

    def is_alpha(self, ch: str) -> bool:
        return ch.isalpha()

    def is_digit(self, ch: str) -> bool:
        return ch.isdigit()

    def is_whitespace(self, ch: str) -> bool:
        return ch.isspace()

    def is_identifier(self, ch: str) -> bool:
        return ch.isalpha() or ch == "_"
