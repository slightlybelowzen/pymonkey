from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TokenType(Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # identifiers and literals
    IDENT = "IDENT"
    INT = "INT"

    # operators
    ASSIGN = "="
    PLUS = "+"

    # Delimiters
    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Keywords
    FUNCTION = "FUNCTION"
    LET = "LET"


@dataclass
class Token:
    token_type: TokenType
    literal: Optional[str]


class Lexer:
    def __init__(self, input: str) -> None:
        self.input_len = len(input)
        self.input = input
        self.position = 0
        self.read_position = 0
        self.ch = ""
        self.read_char()

    # TODO: only works with ascii text, support unicode
    def read_char(self):
        self.ch = (
            self.input[self.read_position]
            if self.read_position < self.input_len
            else ""
        )
        self.position = self.read_position
        self.read_position += 1

    def next_token(self) -> Token:
        token = Token(TokenType.EOF, "")
        match self.ch:
            case "=":
                token = Token(TokenType.ASSIGN, "=")
            case "+":
                token = Token(TokenType.PLUS, "+")
            case ",":
                token = Token(TokenType.COMMA, ",")
            case ";":
                token = Token(TokenType.SEMICOLON, ";")
            case "(":
                token = Token(TokenType.LPAREN, "(")
            case ")":
                token = Token(TokenType.RPAREN, ")")
            case "{":
                token = Token(TokenType.LBRACE, "{")
            case "}":
                token = Token(TokenType.RBRACE, "}")
            case _:
                token = Token(TokenType.EOF, "")
        self.read_char()
        return token
