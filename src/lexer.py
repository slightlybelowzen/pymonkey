from src.token import Token, TokenType


class Lexer:
    def __init__(self, input: str) -> None:
        self.input: str = input
        self.position: int = 0
        self.read_position: int = 0
        self.line: int = 0
        self.character: str = "\0"
        self.input_len: int = 0
        self._post_init()

    def _post_init(self) -> None:
        self.input_len = len(self.input)
        self.read_char()

    def __repr__(self) -> str:
        return (
            f"Lexer(\n"
            f"  input: '{self.input[0:10]}'..,\n"
            f"  position: {self.position},\n"
            f"  read_position: {self.read_position},\n"
            f"  character: {self.character.__repr__()},\n"
            f"  input_len: {self.input_len}\n"
            f")"
        )

    def read_char(self) -> None:
        self.character = self.peek_char()
        self.position = self.read_position
        self.read_position += 1

    def peek_char(self) -> str:
        if self.read_position >= self.input_len:
            return "\0"
        else:
            return self.input[self.read_position]

    def next_token(self) -> Token:
        token = Token(TokenType.ILLEGAL, "", 0)
        self.skip_whitespace()
        match self.character:
            case "\0":
                token = Token(TokenType.EOF, "", self.position, self.line)
            case ",":
                token = Token(TokenType.COMMA, ",", self.position, self.line)
            case "{":
                token = Token(TokenType.LBRACE, "{", self.position, self.line)
            case "}":
                token = Token(TokenType.RBRACE, "}", self.position, self.line)
            case "+":
                token = Token(TokenType.PLUS, "+", self.position, self.line)
            case "*":
                token = Token(TokenType.ASTERISK, "*", self.position, self.line)
            case ";":
                token = Token(TokenType.SEMICOLON, ";", self.position, self.line)
            case "(":
                token = Token(TokenType.LPAREN, "(", self.position, self.line)
            case ")":
                token = Token(TokenType.RPAREN, ")", self.position, self.line)
            case "-":
                token = Token(TokenType.MINUS, "-", self.position, self.line)
            case "/":
                token = Token(TokenType.SLASH, "/", self.position, self.line)
            case "<":
                token = Token(TokenType.LT, "<", self.position, self.line)
            case ">":
                token = Token(TokenType.GT, ">", self.position, self.line)
            case "=":
                token = self.match_peek_token("=", TokenType.EQ, TokenType.ASSIGN)
            case "!":
                token = self.match_peek_token("=", TokenType.NOT_EQ, TokenType.BANG)
            case "\n":
                self.line += 1
            case '"':
                token.position = self.position
                token.literal = self.read_string()
                token.type = TokenType.STRING
                token.line = self.line
            case ch if ch.isalpha():
                token.position = self.position
                token.literal = self.read_identifier()
                token.type = TokenType.lookup_keyword(token.literal)
                token.line = self.line
                return token
            case ch if ch.isdigit():
                token.position = self.position
                token.literal = self.read_number()
                token.type = TokenType.INT
                token.line = self.line
                return token
            case _:
                pass
        self.read_char()
        return token

    def match_peek_token(
        self, expected_char: str, matched: TokenType, default: TokenType
    ) -> Token:
        if self.peek_char() == expected_char:
            # Is there a cleaner way to do this?
            character = self.character
            position = self.position
            self.read_char()
            literal = character + self.character
            return Token(matched, literal, position, self.line)
        return Token(default, self.character, self.position, self.line)

    def read_identifier(self) -> str:
        start_position = self.position
        while self.character.isalpha() or self.character == "_":
            self.read_char()
        return self.input[start_position : self.position]

    def read_string(self) -> str:
        # skip opening "
        self.read_char()
        start_position = self.position
        while self.character != '"':
            # TODO: handle escape characters
            # TODO: handle unterminated strings
            # skip closing "
            self.read_char()
        return self.input[start_position : self.position]

    def read_number(self) -> int:
        # TODO: handle floating point numbers
        start_position = self.position
        while self.character.isdigit():
            self.read_char()
        return int(self.input[start_position : self.position])

    def skip_whitespace(self) -> None:
        while self.character.isspace():
            match self.character:
                case "\n":
                    self.line += 1
                case _:
                    pass
            self.read_char()
