from src.token import Token, TokenType

class Lexer():
    def __init__(self, input: str) -> None:
        self.input: str = input
        self.position: int = 0
        self.read_position: int = 0
        self.character: str | None = None
        self.input_len: int = 0
        self._post_init()
    
    def _post_init(self) -> None:
        self.input_len = len(self.input)
        self.read_char()
    
    def __repr__(self) -> str:
        return f"Lexer(\n" \
            f"  input: '{self.input[0:10]}'..,\n" \
            f"  position: {self.position},\n" \
            f"  read_position: {self.read_position},\n" \
            f"  character: {self.character.__repr__()},\n" \
            f"  input_len: {self.input_len}\n" \
            f")"
    
    def read_char(self) -> None:
        self.peek_char()
        self.position = self.read_position
        self.read_position += 1
    
    def peek_char(self) -> None:
        if self.read_position >= self.input_len:
            self.character = None
        else:
            self.character = self.input[self.read_position]
    
    def next_token(self) -> Token:
        token = Token(TokenType.ILLEGAL, "", 0)
        match self.character:
            case None:
                token = Token(TokenType.EOF, "", self.position) 
            case "=":
                token = Token(TokenType.ASSIGN, "=", self.position)
            case ",":
                token = Token(TokenType.COMMA, ",", self.position)
            case "{":
                token = Token(TokenType.LBRACE, "{", self.position)
            case "}":
                token = Token(TokenType.RBRACE, "}", self.position)
            case "+":
                token = Token(TokenType.PLUS, "+", self.position)
            case "*":
                token = Token(TokenType.ASTERISK, "*", self.position)
            case ";":
                token = Token(TokenType.SEMICOLON, ";", self.position)
            case "(":
                token = Token(TokenType.LPAREN, "(", self.position)
            case ")":
                token = Token(TokenType.RPAREN, ")", self.position)
            case _:
                pass
        self.read_char()
        return token
