from pymonkey.lexer import Lexer
from pymonkey.parser import Parser
from pymonkey.version import VERSION


def main():
    print(f"monkey v{VERSION}")
    while True:
        try:
            code = input(">> ")
            lexer = Lexer(code)
            parser = Parser(lexer)
            program = parser.parse_program()
            for statement in program.statements:
                print(statement)
        except KeyboardInterrupt:
            print("")
            break


if __name__ == "__main__":
    main()
