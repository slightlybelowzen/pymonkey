from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.token import Token


@dataclass
class Node(ABC):
    token: Token

    def token_literal(self) -> str:
        return self.token.literal
    
    def __str__(self) -> str:
        return f"Node(literal={self.token.literal.__repr__()}, type={self.token.type.value}, position={self.token.position})"


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

@dataclass
class Program:
    statements: list[Statement] = field(default_factory=list)

    def token_literal(self) -> str:
        return self.__repr__()
    
    def __str__(self) -> str:
        return f"Program(" \
            f"\n  {'\n  '.join(str(statement) for statement in self.statements)}" \
            f"\n)"

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

    def __str__(self) -> str:
        return f"LetStatement(name={self.name}, value={self.value})"