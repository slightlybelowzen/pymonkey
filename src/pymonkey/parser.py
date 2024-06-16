from pymonkey.ast import Program
from pymonkey.lexer import Lexer


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token
        self.peek_token

        # another hack to get the current and peek token set
        self.next_token()
        self.next_token()

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self):
        program = Program([])
        return program
