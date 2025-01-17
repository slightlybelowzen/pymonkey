from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.token import Token


@dataclass
class Node(ABC):
    token: Token

    def token_literal(self) -> str:
        assert self.token.literal is not None
        return self.token.literal

    def __str__(self) -> str:
        return f"Node(literal={self.token.literal.__repr__()}, type={self.token.type.value})"


@dataclass
class Statement(Node):
    @abstractmethod
    def statement_node(self) -> Statement:
        pass


@dataclass
class Expression(Node):
    @abstractmethod
    def expression_node(self) -> Expression:
        pass


@dataclass
class Program:
    statements: list[Statement] = field(default_factory=list)

    def token_literal(self) -> str:
        return self.__repr__()

    def __str__(self) -> str:
        return (
            f"Program("
            f"\n  {'\n  '.join(str(statement) for statement in self.statements)}"
            f"\n)"
        )


@dataclass
class Identifier(Expression):
    value: str = None

    def expression_node(self):
        return self

    def __str__(self) -> str:
        return f"Identifier(value={self.value.__repr__()})"


@dataclass
class LetStatement(Statement):
    name: Identifier = None
    value: Expression = None

    def statement_node(self):
        return self

    def __str__(self) -> str:
        return f"LetStatement(name={self.name}, value={self.value})"


@dataclass
class ReturnStatement(Statement):
    return_value: Expression = None

    def statement_node(self):
        return self

    def __str__(self) -> str:
        return f"ReturnStatement(return_value={self.return_value})"


@dataclass
class ExpressionStatement(Statement):
    expression: Expression = None

    def statement_node(self):
        return self

    def __str__(self) -> str:
        return f"ExpressionStatement(expression={self.expression})"


@dataclass
class IntegerLiteral(Expression):
    value: int = None

    def expression_node(self):
        return self

    def __str__(self) -> str:
        return f"IntegerLiteral(value={self.value.__repr__()})"


@dataclass
class PrefixExpression(Expression):
    operator: str = None
    right: Expression = None

    def expression_node(self):
        return self

    def __str__(self) -> str:
        return f"PrefixExpression(operator={self.operator}, right={self.right})"


@dataclass
class InfixExpression(Expression):
    operator: str = None
    left: Expression = None
    right: Expression = None

    def expression_node(self):
        return self

    def __str__(self) -> str:
        return f"InfixExpression(left={self.left}, operator={self.operator}, right={self.right})"
