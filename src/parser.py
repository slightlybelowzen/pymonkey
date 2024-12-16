from src.ast import Program
from src.lexer import Lexer
# from src.token import TokenType


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = None
        self.peek_token = None
        self._post_init()
    
    def _post_init(self):
        self.next_token()
        self.next_token()

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()
    
    def parse_program(self) -> Program:
        program = Program()
        return program

