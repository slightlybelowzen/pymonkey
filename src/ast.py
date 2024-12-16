from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.token import Token


@dataclass
class Node(ABC):
    token: Token

    def token_literal(self) -> str:
        return self.token.literal


@dataclass
class Statement(Node):
    @abstractmethod
    def statement_node(self):
        pass

@dataclass
class Expression(Node):
    @abstractmethod
    def expression_node(self):
        pass

class Program:
    def __init__(self):
        self.statements: list[Statement] = []

    def token_literal(self) -> str:
        return self.statements[0].token_literal() if self.statements else ""

@dataclass
class Identifier(Expression):
    value: str

    def expression_node(self):
        return self


@dataclass
class LetStatement(Statement):
    name: Identifier = None
    value: Expression = None

    def statement_node(self):
        pass
