import re

class Token:
    def __init__(self, type_, lexeme, line, column):
        self.type = type_
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        return f"[{self.type}, '{self.lexeme}', línea {self.line}, columna {self.column}]"


class Lexer:

    KEYWORDS = {
        "let": "LET",
        "def": "DEF",
        "return": "RETURN",
        "if": "IF",
        "else": "ELSE",
        "while": "WHILE",
        "print": "PRINT",
        "and": "AND",
        "or": "OR",
        "not": "NOT",
        "true": "BOOL",
        "false": "BOOL"
    }

    OPERATORS = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULT',
        '/': 'DIV',
        '%': 'MOD',
        '^': 'POW',
        '=': 'ASSIGN',
        '==': 'EQUAL',
        '!=': 'NOT_EQUAL',
        '<': 'LESS',
        '>': 'GREATER',
        '<=': 'LESS_EQUAL',
        '>=': 'GREATER_EQUAL'
    }

    DELIMITERS = {
        '(': 'LPAREN',
        ')': 'RPAREN',
        '{': 'LBRACE',
        '}': 'RBRACE',
        ',': 'COMMA',
        ';': 'SEMICOLON'
    }

    def __init__(self, text):
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[self.position] if self.text else None

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1

        if self.position >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.position]

    def peek(self):
        next_pos = self.position + 1
        if next_pos >= len(self.text):
            return None
        return self.text[next_pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char and self.current_char != '\n':
            self.advance()

    def number(self):
        start_column = self.column
        result = ""
        has_dot = False

        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_dot:
                    break
                has_dot = True

            result += self.current_char
            self.advance()

        if has_dot:
            return Token("REAL", result, self.line, start_column)

        return Token("INT", result, self.line, start_column)

    def identifier(self):
        start_column = self.column
        result = ""

        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        token_type = self.KEYWORDS.get(result, "ID")
        return Token(token_type, result, self.line, start_column)

    def string(self):
        start_column = self.column
        self.advance()

        result = ""

        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()

        if self.current_char != '"':
            print(f"Error léxico: cadena sin cerrar en línea {self.line}, columna {start_column}")
            return None

        self.advance()
        return Token("STRING", result, self.line, start_column)

    def get_next_token(self):

        while self.current_char:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '-' and self.peek() == '-':
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            if self.current_char == '"':
                return self.string()

            two_char = self.current_char + (self.peek() or '')

            if two_char in self.OPERATORS:
                token = Token(self.OPERATORS[two_char], two_char, self.line, self.column)
                self.advance()
                self.advance()
                return token

            if self.current_char in self.OPERATORS:
                token = Token(self.OPERATORS[self.current_char], self.current_char, self.line, self.column)
                self.advance()
                return token

            if self.current_char in self.DELIMITERS:
                token = Token(self.DELIMITERS[self.current_char], self.current_char, self.line, self.column)
                self.advance()
                return token

            print(f"Error léxico: carácter inválido '{self.current_char}' en línea {self.line}, columna {self.column}")
            self.advance()

        return Token("EOF", "EOF", self.line, self.column)

    def tokenize(self):
        tokens = []

        while True:
            token = self.get_next_token()
            tokens.append(token)

            if token.type == "EOF":
                break

        return tokens

code = """
let x =20;

if x >= 15 {
    print("Hola");
}
"""

lexer = Lexer(code)

tokens = lexer.tokenize()

for token in tokens:
    print(token)