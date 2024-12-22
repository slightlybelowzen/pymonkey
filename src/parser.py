from enum import Enum
from typing import Callable

from src.ast import (
    Expression,
    ExpressionStatement,
    Identifier,
    InfixExpression,
    IntegerLiteral,
    LetStatement,
    PrefixExpression,
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

        # Add precedence mapping
        self.precedences: dict[TokenType, Precedence] = {
            TokenType.EQ: Precedence.EQUALS,
            TokenType.NOT_EQ: Precedence.EQUALS,
            TokenType.LT: Precedence.LESS_GREATER,
            TokenType.GT: Precedence.LESS_GREATER,
            TokenType.PLUS: Precedence.SUM,
            TokenType.MINUS: Precedence.SUM,
            TokenType.SLASH: Precedence.PRODUCT,
            TokenType.ASTERISK: Precedence.PRODUCT,
        }

        self.prefix_parse_fns: dict[TokenType, Callable[[], Expression]] = {
            TokenType.IDENT: self.parse_identifier,
            TokenType.INT: self.parse_integet_literal,
            TokenType.BANG: self.parse_prefix_expression,
            TokenType.MINUS: self.parse_prefix_expression,
        }
        self.infix_parse_fns: dict[TokenType, Callable[[Expression], Expression]] = {
            TokenType.PLUS: self.parse_infix_expression,
            TokenType.MINUS: self.parse_infix_expression,
            TokenType.SLASH: self.parse_infix_expression,
            TokenType.ASTERISK: self.parse_infix_expression,
            TokenType.EQ: self.parse_infix_expression,
            TokenType.NOT_EQ: self.parse_infix_expression,
            TokenType.LT: self.parse_infix_expression,
            TokenType.GT: self.parse_infix_expression,
        }
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

    def parse_statement(self) -> Statement | None:
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
        assert self.current_token is not None
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

        while (
            self.peek_token is not None
            and self.peek_token.type == TokenType.SEMICOLON
            and precedence.value < self.peek_precedence().value
        ):
            infix = self.infix_parse_fns.get(self.peek_token.type, None)
            if not infix:
                return left_exp

            self.next_token()
            left_exp = infix(left_exp)

        return left_exp

    def parse_identifier(self) -> Expression:
        assert self.current_token is not None
        node = Identifier(token=self.current_token, value=self.current_token.literal)
        return node

    def parse_integet_literal(self) -> Expression:
        assert self.current_token is not None
        try:
            value = int(self.current_token.literal)
        except ValueError:
            raise ParserError(
                f"line {self.current_token.line}, col: {self.current_token.position}: could not parse {self.current_token.literal} as an integer"
            )
        literal = IntegerLiteral(token=self.current_token, value=value)
        return literal

    def parse_prefix_expression(self) -> Expression:
        assert self.current_token is not None
        expression = PrefixExpression(
            token=self.current_token, operator=self.current_token.literal
        )
        self.next_token()
        expression.right = self.parse_expression(Precedence.PREFIX)
        return expression

    def parse_infix_expression(self, left: Expression) -> Expression:
        assert self.current_token is not None

        expression = InfixExpression(
            token=self.current_token,
            operator=self.current_token.literal,
            left=left,
        )
        precedence = self.current_precedence()
        self.next_token()
        expression.right = self.parse_expression(precedence)
        return expression

    def parse_return_statement(self) -> ReturnStatement:
        assert self.current_token is not None
        statement = ReturnStatement(self.current_token)
        self.next_token()

        # This check is really annoying, is there a way to avoid it everywhere
        assert self.current_token is not None
        # TODO: parse the expression for the return value
        while self.current_token.type != TokenType.SEMICOLON:
            self.next_token()

        return statement

    def parse_let_statement(self) -> LetStatement | None:
        assert self.current_token is not None
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

    def peek_precedence(self) -> Precedence:
        assert self.peek_token is not None
        return self.precedences.get(self.peek_token.type, Precedence.LOWEST)

    def current_precedence(self) -> Precedence:
        assert self.current_token is not None
        return self.precedences.get(self.current_token.type, Precedence.LOWEST)
