import sys

from src.lexer import Lexer


def main():
    args = sys.argv[1:]
    file = args[0]
    with open(file, "r") as f:
        content = f.read()
    lexer = Lexer(
        content.strip(), position=0, character=content[0] if len(content) > 0 else None
    )
    while lexer.character is not None:
        lexer, token = lexer.next_token()
        print(token)


if __name__ == "__main__":
    main()
