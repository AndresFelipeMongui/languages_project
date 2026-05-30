class Token:

    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "line": self.line,
            "column": self.column
        }

    def __str__(self):
        return f"{self.type}:{self.value}"


class Lexer:

    KEYWORDS = {
        "let": "LET",
        "if": "IF",
        "else": "ELSE",
        "while": "WHILE",
        "print": "PRINT",
        "true": "BOOL",
        "false": "BOOL",
        "and": "AND",
        "or": "OR",
        "not": "NOT"
    }

    SINGLE = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULT',
        '/': 'DIV',
        '(': 'LPAREN',
        ')': 'RPAREN',
        '{': 'LBRACE',
        '}': 'RBRACE',
        ';': 'SEMICOLON',
        '=': 'ASSIGN',
        '%': 'MOD',
        '^': 'POW',
        '<': 'LESS',
        '>': 'GREATER'
    }

    DOUBLE = {
    "==": "EQUAL",
    "!=": "NOTEQUAL",
    "<=": "LESSEQUAL",
    ">=": "GREATEREQUAL",
    }

    def __init__(self, text):

        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1

        self.current = self.text[self.pos] if text else None

        self.errors = []

    def advance(self):

        if self.current == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.pos += 1

        if self.pos < len(self.text):
            self.current = self.text[self.pos]
        else:
            self.current = None

    def skip_whitespace(self):

        while self.current and self.current.isspace():
            self.advance()

    def number(self):

        start_col = self.column

        result = ""

        while self.current and (
            self.current.isdigit() or self.current == '.'
        ):
            result += self.current
            self.advance()

        if '.' in result:
            return Token("FLOAT", float(result), self.line, start_col)

        return Token("INT", int(result), self.line, start_col)

    def identifier(self):

        start_col = self.column

        result = ""

        while self.current and (
            self.current.isalnum() or self.current == '_'
        ):
            result += self.current
            self.advance()

        token_type = self.KEYWORDS.get(result, "ID")

        if token_type == "BOOL":
            return Token(
                "BOOL",
                result == "true",
                self.line,
                start_col
            )

        return Token(token_type, result, self.line, start_col)

    def string(self):

        start_col = self.column

        self.advance()

        result = ""

        while self.current and self.current != '"':
            result += self.current
            self.advance()

        self.advance()

        return Token("STRING", result, self.line, start_col)

    def tokenize(self):

        tokens = []

        while self.current:

            if self.current.isspace():
                self.skip_whitespace()
                continue

            if self.current.isdigit():
                tokens.append(self.number())
                continue

            if self.current.isalpha() or self.current == '_':
                tokens.append(self.identifier())
                continue

            if self.current == '"':
                tokens.append(self.string())
                continue

            if self.current in self.SINGLE:

                token = Token(
                    self.SINGLE[self.current],
                    self.current,
                    self.line,
                    self.column
                )

                tokens.append(token)

                self.advance()

                continue
            if self.current == '-' and self.peek() == '-':
                self.advance()
                self.advance()
                self.skip_comment()
                continue

            two_char = (self.current or '') + (self.peek() or '')
            if two_char in self.DOUBLE:
                tokens.append(Token(
                    self.DOUBLE[two_char],
                    two_char,
                    self.line,
                    self.column
                ))
                self.advance()
                self.advance()
                continue

            self.errors.append(
                f"Carácter ilegal '{self.current}' "
                f"en línea {self.line}"
            )

            self.advance()

        return tokens
    def peek(self):
        next_pos = self.pos + 1
        if next_pos < len(self.text):
            return self.text[next_pos]
        return None
    def skip_comment(self):
        while self.current and self.current != '\n':
            self.advance()