from ast import Expression
from collections.abc import Callable
from enum import Enum
from src.ast import (
    ExpressionStatement,
    Identifier,
    LetStatement,
    Program,
    ReturnStatement,
    Statement,
)
from src.lexer import Lexer
from src.token import Token, TokenType


class Precedence(Enum):
    LOWEST = 1
    EQUALS = 2
    LESS_GREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7


class ParserError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token: Token | None = None
        self.peek_token: Token | None = None
        self.prefix_parse_fns: dict[TokenType, Callable[[], Expression]] = {
            TokenType.IDENT: self.parse_identifier,
        }
        self.infix_parse_fns: dict[TokenType, Callable[[Expression], Expression]] = {}
        self._post_init()

    def _post_init(self):
        self.next_token()
        self.next_token()

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> Program:
        program = Program()
        # to satisfy pyright, and also a good sanity check to have
        assert self.current_token is not None
        assert self.peek_token is not None
        while self.current_token.type != TokenType.EOF:
            statement = self.parse_statement()
            if statement:
                program.statements.append(statement)
            self.next_token()
        return program

    def parse_statement(self) -> Statement:
        # same thing as above
        assert self.current_token is not None
        match self.current_token.type:
            case TokenType.LET:
                return self.parse_let_statement()
            case TokenType.RETURN:
                return self.parse_return_statement()
            case _:
                return self.parse_expression_statement()

    def parse_expression_statement(self) -> ExpressionStatement:
        statement = ExpressionStatement(self.current_token)
        statement.expression = self.parse_expression(Precedence.LOWEST)

        assert self.peek_token is not None
        if self.peek_token.type == TokenType.SEMICOLON:
            self.next_token()

        return statement

    def parse_expression(self, precedence: Precedence) -> Expression:
        assert self.current_token is not None
        prefix = self.prefix_parse_fns.get(self.current_token.type, None)
        if not prefix:
            raise ParserError(f"no prefix parse function for {self.current_token.type}")
        left_exp = prefix()

        return left_exp

    def parse_identifier(self) -> Expression:
        assert self.current_token is not None
        node = Identifier(token=self.current_token, value=self.current_token.literal)
        return node

    def parse_return_statement(self) -> ReturnStatement:
        statement = ReturnStatement(self.current_token)
        self.next_token()

        # This check is really annoying, is there a way to avoid it everywhere
        assert self.current_token is not None
        # TODO: parse the expression for the return value
        while self.current_token.type != TokenType.SEMICOLON:
            self.next_token()

        return statement

    def parse_let_statement(self) -> LetStatement:
        statement = LetStatement(self.current_token)
        if not self.expect_peek(TokenType.IDENT):
            return None
        assert self.current_token is not None
        statement.name = Identifier(self.current_token, self.current_token.literal)
        if not self.expect_peek(TokenType.ASSIGN):
            return None
        # TODO: parse the expression for the value
        while not self.current_token.type == TokenType.SEMICOLON:
            self.next_token()
        return statement

    def expect_peek(self, token_type: TokenType) -> bool:
        # same thing as above
        assert self.peek_token is not None
        if self.peek_token.type != token_type:
            raise ParserError(
                f"line {self.peek_token.line}, col: {self.peek_token.position}: expected {token_type}, got {self.peek_token.type} instead"
            )
        self.next_token()
        return True
