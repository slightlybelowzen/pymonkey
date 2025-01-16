import sys

from src.ast import Program
from src.lexer import Lexer
from src.parser import Parser


def main():
    def get_ast(inp: str) -> Program:
        lexer = Lexer(inp)
        parser = Parser(lexer)
        return parser.parse_program()

    def run_interpreter():
        print("Pymonkey 0.1.0")
        while True:
            try:
                user_inp = input(">>> ")
                prog = get_ast(user_inp)
                print(prog)
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
            except EOFError:
                exit(0)

    args = sys.argv[1:]
    if not args:
        run_interpreter()
    file = args[0]
    with open(file, "r") as f:
        content = f.read()
    program = get_ast(content)
    print(program)


if __name__ == "__main__":
    main()
