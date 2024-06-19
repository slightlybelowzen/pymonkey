from typing import Optional
from pymonkey.lexer import Token


class Node:
    """Base class for all AST nodes. Contains methods for debugging the value of the node token literal."""

    def __init__(self):
        raise NotImplementedError

    def token_literal(self) -> str:
        raise NotImplementedError


class Statement(Node):
    """Base class for all statement nodes."""

    def __init__(self):
        super().__init__()

    def statement_node():
        raise NotImplementedError


class Expression(Node):
    """Base class for all expression nodes."""

    def __init__(self):
        super().__init__()

    def expression_node():
        raise NotImplementedError


class Program(Node):
    """Represents a program. Root node of the AST. Contains a list of statements."""

    def __init__(self, statements: list[Statement] = []):
        self.statements = statements

    def token_literal(self) -> str:
        return "" if len(self.statements) == 0 else self.statements[0].token_literal()


class Identifier(Expression):
    """Represents an identifier node in the program. Contains the token and the value of the identifier."""

    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node():
        raise NotImplementedError


class LetStatement(Statement):
    """Represents a node for a let statement in the program. Contains the token representing let, an identifier node and the expression value."""

    def __init__(
        self,
        token: Token,
        identifier: Optional[Identifier] = None,
        value: Optional[Expression] = None,
    ):
        self.token = token
        self.identifier = identifier
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node():
        raise NotImplementedError


class ReturnStatement(Statement):
    """Represents a node for a return statement in the program. Contains the token representing return, and an expression value."""

    def __init__(self, token: Token, value: Optional[Expression] = None):
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node():
        raise NotImplementedError
