import math

from ast_nodes import *

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:

    def __init__(self):

        self.variables = {}
        self.functions = {}
        self.output = []
        self.builtins={
            "sin":lambda x:math.sin(x)
        }

    def visit(self, node):

        method_name = f"visit_{type(node).__name__}"

        method = getattr(self, method_name)

        return method(node)
    

    def visit_BlockNode(self, node):

        for statement in node.statements:
            self.visit(statement)

    def visit_NumberNode(self, node):

        return node.value

    def visit_StringNode(self, node):

        return node.value

    def visit_BoolNode(self, node):

        return node.value
    
    def get_symbol_table(self):
        return self.variables

    def visit_VariableNode(self, node):

        if node.name not in self.variables:
            raise Exception(
                f"Variable '{node.name}' no definida"
            )

        return self.variables[node.name]

    def visit_AssignNode(self, node):

        value = self.visit(node.value)

        self.variables[node.name] = value

    def visit_BinOpNode(self, node):

        left = self.visit(node.left)

        right = self.visit(node.right)

        if node.op == "PLUS":
            return left + right

        if node.op == "MINUS":
            return left - right

        if node.op == "MULT":
            return left * right

        if node.op == "DIV":
            return left / right
        if node.op == "EQUAL":
            return left == right

        if node.op == "NOTEQUAL":
            return left != right

        if node.op == "LESS":
            return left < right

        if node.op == "GREATER":
            return left > right

        if node.op == "LESSEQUAL":
            return left <= right

        if node.op == "GREATEREQUAL":
            return left >= right

        if node.op == "AND":
            return bool(left) and bool(right)

        if node.op == "OR":
            return bool(left) or bool(right)

        if node.op == "MOD":
            return left % right

        if node.op == "POW":
            return left ** right

        raise Exception(
            f"Operador desconocido {node.op}"
        )

    def visit_PrintNode(self, node):

        value = self.visit(node.expr)

        self.output.append(str(value))

        return value
    def visit_UnaryOpNode(self, node):
        value = self.visit(node.expr)

        if node.op == "NOT":
            return not bool(value)

        if node.op == "MINUS":
            return -value

        raise Exception(f"Operador unario desconocido {node.op}")
    def visit_IfNode(self, node):
        condition_value = self.visit(node.condition)

        if condition_value:
            return self.visit(node.then_block)
        elif node.else_block:
            return self.visit(node.else_block)
###While
    def visit_WhileNode(self, node):
        result = None
        while self.visit(node.condition):
            result = self.visit(node.body)
        return result
##Para definicion de funciones
    def visit_FuncDefNode(self, node):
        self.functions[node.name] = node
        return None
##Para return
    def visit_ReturnNode(self, node):
        value = self.visit(node.expr)
        raise ReturnException(value)
    
##Para la llamada de funciones
    def visit_FuncCallNode(self, node):
        arg_values = [self.visit(arg) for arg in node.args]


        if node.name in self.builtins:
            if len(arg_values) != 1:
                raise Exception(
                f"La función integrada '{node.name}' esperaba 1 argumento"
            )

            try:
                return self.builtins[node.name](*arg_values)
            except Exception:
                raise Exception(
                f"Argumento inválido para la función '{node.name}'"
            )

        if node.name not in self.functions:
            raise Exception(f"Función '{node.name}' no definida")

        func_def = self.functions[node.name]
        if len(node.args) != len(func_def.params):
            raise Exception(
                f"La función '{node.name}' esperaba {len(func_def.params)} argumentos "
        )

        arg_values = [self.visit(arg) for arg in node.args]

        previous_variables = self.variables.copy()

        local_env = {}
        for param_name, arg_value in zip(func_def.params, arg_values):
            local_env[param_name] = arg_value

        self.variables = local_env

        try:
            self.visit(func_def.body)
        except ReturnException as ret:
            self.variables = previous_variables
            return ret.value

        self.variables = previous_variables
        return None