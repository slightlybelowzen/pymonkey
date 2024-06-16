from pymonkey.lexer import Lexer, TokenType
from pymonkey.version import VERSION


def main():
    print(f"monkey v{VERSION}")
    while True:
        try:
            print(">> ", end="")
            code = input()
            lexer = Lexer(code)
            while True:
                token = lexer.next_token()
                if token.token_type == TokenType.EOF:
                    break
                print(token)
        except KeyboardInterrupt:
            print("")
            break


if __name__ == "__main__":
    main()
