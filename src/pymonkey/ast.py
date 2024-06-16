from pymonkey.lexer import Token


class Node:
    def __init__(self):
        raise NotImplementedError

    def token_literal(self) -> str:
        raise NotImplementedError


class Statement(Node):
    def __init__(self):
        super().__init__()

    def statement_node():
        raise NotImplementedError


class Expression(Node):
    def __init__(self):
        super().__init__()

    def expression_node():
        raise NotImplementedError


class Program(Node):
    def __init__(self, statements: list[Statement]):
        self.statements = statements

    def token_literal(self) -> str:
        return "" if len(self.statements) == 0 else self.statements[0].token_literal()


class Identifier(Expression):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node():
        raise NotImplementedError


class LetStatement(Statement):
    def __init__(self, token: Token, identifier: Identifier, value: Expression):
        self.token = token
        self.identifier = identifier
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node():
        raise NotImplementedError
