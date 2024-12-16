import sys

from src.lexer import Lexer
from src.token import TokenType

def get_tokens(content: str):
    lexer = Lexer(content)
    token = lexer.next_token()
    while token.type != TokenType.EOF:
        yield token
        token = lexer.next_token()

def run_interpreter():
    print("Pymonkey 0.1.0")
    while True:
        try:
            content = input(">>> ")
            for token in get_tokens(content):
                print(token)
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
    for token in get_tokens(content):
        print(token)


if __name__ == "__main__":
    main()

