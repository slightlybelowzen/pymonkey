from src.ast import Identifier, LetStatement, Program, ReturnStatement, Statement
from src.lexer import Lexer
from src.token import Token, TokenType


class ParserError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token: Token | None = None
        self.peek_token: Token | None = None
        self.errors: list[str] = []
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
                return None

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
