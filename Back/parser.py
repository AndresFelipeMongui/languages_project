from ast_nodes import *


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.pos = 0

        self.current = (
            self.tokens[self.pos]
            if tokens else None
        )

    def advance(self):

        self.pos += 1

        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = None

    def parse(self):

        statements = []

        while self.current:
            statements.append(self.statement())

        return BlockNode(statements)

    def statement(self):

        if self.current.type == "LET":
            return self.assignment()

        if self.current.type == "PRINT":
            return self.print_statement()

        raise Exception(
            f"Sentencia inesperada: {self.current.type}"
        )

    def assignment(self):

        self.advance()

        if self.current.type != "ID":
            raise Exception("Se esperaba identificador")

        var_name = self.current.value

        self.advance()

        if self.current.type != "ASSIGN":
            raise Exception("Se esperaba '='")

        self.advance()

        expr = self.expr()

        if self.current and self.current.type == "SEMICOLON":
            self.advance()

        return AssignNode(var_name, expr)

    def print_statement(self):

        self.advance()

        if self.current.type != "LPAREN":
            raise Exception("Se esperaba '('")

        self.advance()

        expr = self.expr()

        if self.current.type != "RPAREN":
            raise Exception("Se esperaba ')'")

        self.advance()

        if self.current and self.current.type == "SEMICOLON":
            self.advance()

        return PrintNode(expr)

    def expr(self):

        node = self.term()

        while self.current and self.current.type in (
            "PLUS",
            "MINUS"
        ):

            op = self.current.type

            self.advance()

            right = self.term()

            node = BinOpNode(node, op, right)

        return node

    def term(self):

        node = self.factor()

        while self.current and self.current.type in (
            "MULT",
            "DIV"
        ):

            op = self.current.type

            self.advance()

            right = self.factor()

            node = BinOpNode(node, op, right)

        return node

    def factor(self):

        token = self.current

        if token.type == "INT":
            self.advance()
            return NumberNode(token.value)

        if token.type == "FLOAT":
            self.advance()
            return NumberNode(token.value)

        if token.type == "STRING":
            self.advance()
            return StringNode(token.value)

        if token.type == "BOOL":
            self.advance()
            return BoolNode(token.value)

        if token.type == "ID":
            self.advance()
            return VariableNode(token.value)

        if token.type == "LPAREN":

            self.advance()

            node = self.expr()

            if self.current.type != "RPAREN":
                raise Exception("Se esperaba ')'")

            self.advance()

            return node

        raise Exception(
            f"Factor inesperado: {token.type}"
        )