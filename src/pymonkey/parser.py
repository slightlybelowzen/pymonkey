from typing import Optional
from pymonkey.ast import Identifier, LetStatement, Program, ReturnStatement, Statement
from pymonkey.lexer import Lexer, Token, TokenType


class Parser:
    """Parser class that contains the functionality to parse a program."""

    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token: Token = None
        self.peek_token: Token = None
        self.errors: list[str] = []

        # another hack to get the current and peek token set
        self.next_token()
        self.next_token()

    def next_token(self):
        """Consumes the current token and sets the peek token to the next token consumed by the lexer."""
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> Program:
        """Parses a program and returns an AST of type Program."""
        program = Program([])
        while self.current_token.token_type != TokenType.EOF:
            statement = self.parse_statement()
            if statement:
                program.statements.append(statement)
            self.next_token()
        if self.errors:
            for error in self.errors:
                print(error)
            raise Exception("Could not parse program")
        return program

    def parse_statement(self) -> Optional[Statement]:
        """Parses a statement and returns a Statement object of the appropriate subclass."""
        match self.current_token.token_type:
            case TokenType.LET:
                return self.parse_let_statement()
            case TokenType.RETURN:
                return self.parse_return_statement()
            case _:
                return None

    def parse_let_statement(self) -> Optional[LetStatement]:
        """Parses a let statement and returns a LetStatement object. Of the form, let <identifier> = <value>"""
        statement = LetStatement(token=self.current_token)
        # the next token should be an identifier
        if not self.expect_peek_token(TokenType.IDENT):
            self.errors.append(
                f"line {self.current_token.line}: expected next token to be {TokenType.IDENT.value}, got {self.peek_token.literal} instead"
            )
        statement.identifier = Identifier(
            token=self.current_token, value=self.current_token.literal
        )
        # the next token should be '='
        if not self.expect_peek_token(TokenType.ASSIGN):
            self.errors.append(
                f"line {self.current_token.line}: expected next token to be {TokenType.ASSIGN.value}, got {self.peek_token.literal} instead"
            )
        # skip the expression until the next semicolon for now (ignore the expression on the RHS of =)
        while self.current_token.token_type != TokenType.SEMICOLON:
            self.next_token()
        return statement

    def parse_return_statement(self) -> Optional[ReturnStatement]:
        """Parses a return statement and returns a ReturnStatement object. Of the form, return <expression>"""
        statement = ReturnStatement(token=self.current_token)
        self.next_token()
        while self.current_token.token_type != TokenType.SEMICOLON:
            self.next_token()
        return statement

    def expect_peek_token(self, expected_token_type: TokenType) -> bool:
        """Checks if the next token is of the given type and if so, consumes it."""
        if self.peek_token.token_type == expected_token_type:
            self.next_token()
            return True
        return False
