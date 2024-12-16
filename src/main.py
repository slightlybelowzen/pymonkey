import sys

from src.ast import Program
from src.lexer import Lexer
from src.parser import Parser

def get_ast(content: str) -> Program:
    lexer = Lexer(content)
    parser = Parser(lexer)
    return parser.parse_program()

def run_interpreter():
    print("Pymonkey 0.1.0")
    while True:
        try:
            content = input(">>> ")
            program = get_ast(content)
            print(program)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
        except EOFError:
            exit(0)


def main():
    args = sys.argv[1:]
    if args == []:
        run_interpreter()
    file = args[0]
    with open(file, "r") as f:
        content = f.read()
    program = get_ast(content)
    print(program)


if __name__ == "__main__":
    main()

