# from __future__ import annotations
from src.token import Token, TokenType

def shift(inp: str) -> tuple[str, str]:
    return bool(inp) and (inp[0], inp[1:])

def nothing(inp: str) -> tuple[str, str]:
    return (None, inp)

def filt(predicate):
    ...
