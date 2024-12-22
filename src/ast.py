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
    value: str

    def expression_node(self):
        return self

    def __str__(self) -> str:
        return f"Identifier(value={self.value.__repr__()})"


@dataclass
class LetStatement(Statement):
    name: Identifier
    value: Expression

    def statement_node(self):
        return self

    def __str__(self) -> str:
        return f"LetStatement(name={self.name}, value={self.value})"


@dataclass
class ReturnStatement(Statement):
    return_value: Expression

    def statement_node(self):
        return self

    def __str__(self) -> str:
        return f"ReturnStatement(return_value={self.return_value})"


@dataclass
class ExpressionStatement(Statement):
    expression: Expression

    def statement_node(self):
        return self

    def __str__(self) -> str:
        return f"ExpressionStatement(expression={self.expression})"


@dataclass
class IntegerLiteral(Expression):
    value: int

    def expression_node(self):
        return self

    def __str__(self) -> str:
        return f"IntegerLiteral(value={self.value.__repr__()})"


@dataclass
class PrefixExpression(Expression):
    operator: str
    right: Expression

    def expression_node(self):
        return self

    def __str__(self) -> str:
        return f"PrefixExpression(operator={self.operator}, right={self.right})"


@dataclass
class InfixExpression(Expression):
    operator: str
    left: Expression
    right: Expression

    def expression_node(self):
        return self

    def __str__(self) -> str:
        return f"InfixExpression(left={self.left}, operator={self.operator}, right={self.right})"
