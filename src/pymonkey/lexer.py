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
    MINUS = "-"
    ASTERISK = "*"
    SLASH = "/"
    LT = "<"
    GT = ">"
    EQUAL_EQ = "=="
    BANG_EQ = "!="
    BANG = "!"

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
    RETURN = "RETURN"
    IF = "IF"
    ELSE = "ELSE"
    TRUE = "TRUE"
    FALSE = "FALSE"


KEYWORDS_MAP = {
    "let": TokenType.LET,
    "fn": TokenType.FUNCTION,
    "return": TokenType.RETURN,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}


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

    def next_token(self) -> Token:
        token = Token(TokenType.EOF, "")
        self.skip_whitespace()
        match self.ch:
            case "=":
                if self.peek_char() == "=":
                    self.read_char()
                    token = Token(TokenType.EQUAL_EQ, "==")
                else:
                    token = Token(TokenType.ASSIGN, "=")
            case "+":
                token = Token(TokenType.PLUS, "+")
            case "-":
                token = Token(TokenType.MINUS, "-")
            case "!":
                if self.peek_char() == "=":
                    self.read_char()
                    token = Token(TokenType.BANG_EQ, "!=")
                else:
                    token = Token(TokenType.BANG, "!")
            case "/":
                token = Token(TokenType.SLASH, "/")
            case "*":
                token = Token(TokenType.ASTERISK, "*")
            case "<":
                token = Token(TokenType.LT, "<")
            case ">":
                token = Token(TokenType.GT, ">")
            case ";":
                token = Token(TokenType.SEMICOLON, ";")
            case ",":
                token = Token(TokenType.COMMA, ",")
            case "(":
                token = Token(TokenType.LPAREN, "(")
            case ")":
                token = Token(TokenType.RPAREN, ")")
            case "{":
                token = Token(TokenType.LBRACE, "{")
            case "}":
                token = Token(TokenType.RBRACE, "}")
            case _:
                if self.ch.isalpha():
                    literal = self.read_identifier()
                    token = Token(self.lookup_ident_literal_type(literal), literal)
                elif self.ch.isdigit():
                    token = Token(TokenType.INT, self.read_int())
                else:
                    token = Token(TokenType.EOF, "")
                return token
        self.read_char()
        return token

    # @todo: only works with ascii text, support unicode
    def read_char(self):
        self.ch = (
            self.input[self.read_position]
            if self.read_position < self.input_len
            else ""
        )
        self.position = self.read_position
        self.read_position += 1

    def read_identifier(self) -> str:
        start_position = self.position
        while self.ch.isalpha() or self.ch.isdigit():
            self.read_char()
        return self.input[start_position : self.position]

    def lookup_ident_literal_type(self, identifier: str) -> TokenType:
        return (
            KEYWORDS_MAP[identifier]
            if identifier in KEYWORDS_MAP.keys()
            else TokenType.IDENT
        )

    def skip_whitespace(self):
        while self.ch.isspace():
            self.read_char()

    # @todo: only works with integers, support floats and hexadecimal
    def read_int(self) -> str:
        start_position = self.position
        while self.ch.isdigit():
            self.read_char()
        return self.input[start_position : self.position]

    def peek_char(self) -> str:
        return (
            ""
            if self.read_position >= self.input_len
            else self.input[self.read_position]
        )
