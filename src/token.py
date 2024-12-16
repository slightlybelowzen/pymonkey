from __future__ import annotations
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
    def lookup_keyword(ident: str) -> TokenType:
        match ident:
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
