class NumberNode:

    def __init__(self, value):
        self.value = value

    def to_dict(self):

        return {
            "type": "NumberNode",
            "value": self.value
        }


class StringNode:

    def __init__(self, value):
        self.value = value

    def to_dict(self):

        return {
            "type": "StringNode",
            "value": self.value
        }


class BoolNode:

    def __init__(self, value):
        self.value = value

    def to_dict(self):

        return {
            "type": "BoolNode",
            "value": self.value
        }


class VariableNode:

    def __init__(self, name):
        self.name = name

    def to_dict(self):

        return {
            "type": "VariableNode",
            "name": self.name
        }


class BinOpNode:

    def __init__(self, left, op, right):

        self.left = left
        self.op = op
        self.right = right

    def to_dict(self):

        return {
            "type": "BinOpNode",
            "operator": self.op,
            "left": self.left.to_dict(),
            "right": self.right.to_dict()
        }


class AssignNode:

    def __init__(self, name, value):

        self.name = name
        self.value = value

    def to_dict(self):

        return {
            "type": "AssignNode",
            "name": self.name,
            "value": self.value.to_dict()
        }


class PrintNode:

    def __init__(self, expr):
        self.expr = expr

    def to_dict(self):

        return {
            "type": "PrintNode",
            "expr": self.expr.to_dict()
        }


class BlockNode:

    def __init__(self, statements):
        self.statements = statements

    def to_dict(self):

        return {
            "type": "BlockNode",
            "statements": [
                stmt.to_dict()
                for stmt in self.statements
            ]
        }
    
class IfNode:
    def __init__(self,condition,then_block,else_block=None):
        self.condition=condition
        self.then_block = then_block
        self.else_block = else_block
    def to_dict(self):
        return {
            "type": "IfNode",
            "condition": self.condition.to_dict(),
            "then_block": self.then_block.to_dict(),
            "else_block": self.else_block.to_dict() if self.else_block else None
        }
class UnaryOpNode:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
        
    def to_dict(self):
        return {
            "type": "UnaryOpNode",
            "operator": self.op,
            "expr": self.expr.to_dict()
        }
#Nodeo para la sentencia while
class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def to_dict(self):
        return {
            "type": "WhileNode",
            "condition": self.condition.to_dict(),
            "body": self.body.to_dict()
        }