class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def define(self, name, value):

        if name in self.symbols:
            raise Exception(
                f"Variable '{name}' redeclarada"
            )

        self.symbols[name] = value

    def lookup(self, name):

        if name not in self.symbols:
            raise Exception(
                f"Variable '{name}' no declarada"
            )

        return self.symbols[name]