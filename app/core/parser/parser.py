from app.core.parser.astNodes import(
    ProgramNode, BinOpNode, UnaryOpNode, NumberNode, StringNode, BoolNode,
    VariableNode, AssignNode, FuncDefNode, FuncCallNode, IfNode,
    WhileNode, BlockNode, PrintNode, ReturnNode
)





##Declaracion de el parsing de sentencias

def parse_statement(self):
    token = self.current()

    if token.type=="LET":
        return self.parse_assignment()
    elif token.type=="PRINT":
        return self.parse_print()
    elif token.type =="IF":
        return self.parse_if()
    elif token.type=="WHILE":
        return self.parse_while()
    elif token.type == "DEF":
        return self.parse_funcdef()
    elif token.type=="RETURN":
        return self.parse_return()
    elif token.type=="LBRACE":
        return self.parse_block()
    else:
        expr=self.parse_expression()
        if self.curent().type=="SEMICOLON":
            SELF.EAT("SEMICOLON")
        return expr
    

##Parsing de bloques y sentencias concretas

def parse_block(self):
    self.eat("LBRACE")
    statements=[]
    while self.current().type != "RBRACE":
        statements.append(self.parse_statement())
    self.eat("RBRACE")
    return BlockNode(statements)

def parse_assignment(self):
    let_token=self.eat("LET")
    name=self.eat("ID")
    self.eat("ASSIGN")
    expr=self.parse_expression()
    if self.current().type=="SEMICOLON":
        self.eat("SEMICOLON")
    return AssignNode(name.lexeme,expr,let_token.line)

def parse_print(self):
    token=self.eat("PRINT")
    self.eat("LPAREN")
    expr=self.parse_expression()
    self.eat("RPAREN")
    if self.current().type == "SEMICOLON":
        self.eat("SEMICOLON")
    return PrintNode(expr,token.line)

def parse_return(self):
    token=self.eat("RETURN")
    expr=self.parse_expression()
    if self.current().type=="SEMICOLON":
        self.eat("SEMICOLON")
    return REturnNode(expr,token.line)

def parse_if(self):
    token=self.eat("IF")
    condition=self.parse_expression()
    then_block=self.parse_block()
    else_block=None
    if self.current().type == "ELSE":
        self.eat("ELSE")
        else_block=self.parse_block()
    return IfNode(condition,then_block,else_block,token.line)

def parse_while(self):
    token=self.eat("WHILE")
    condition=self.parse_expression()
    body=self.parse_block()
    return WhileNode(condition,body,token.line)

def parse_funcdef(self):
    token=self.eat("DEF")
    name=self.eat("ID")
    self.eat("LPAREN")

    params=[]
    if self.current().type != "RPAREN":
        params.append(self.eat("ID").lexeme)
        while self.current().type=="COMMA":
            self.eat("COMMA")
            params.append(self.eat("ID").lexeme)

    self.eat("RPAREN")
    body=self.parse_block()
    return FuncDefNode(name.lexeme,params,body,token.line)



##parsing expreciones con precedencia
def parse_expression(self):
    return self.parse_or()


def parse_or(self):
    node=self.parse_and()
    while self.current().type=="OR":
        op=self.eat("OR")
        right=self.parse_and()
        node=BinOpNode(node,op.lexeme,right,op.line)
    return node

def parse_and(self):
    node=self.parse_equality()
    while self.current().type=="AND":
        op=self.eat("AND")
        right=self.parse_equality()
        node=BinOpNode(node,op.lexeme,rigth,op.line)
    return node

def parse_equality(self):
    node=self.parse_comparison()
    while self.current().type in ("EQUAL", "NOT_EQUAL"):
        op=self.current()
        self.advance()
        right=self.parse_comparison()
        node=BinOpNode(node, op.lexeme,right,op.line)
    return node

def parse_comparison(self):
    node = self.parse_term()
    while self.current().type in ("LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL"):
         op = self.current()
         self.advance()
         right = self.parse_term()
         node = BinOpNode(node, op.lexeme, right, op.line)
    return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current().type in ("PLUS", "MINUS"):
            op = self.current()
            self.advance()
            right = self.parse_factor()
            node = BinOpNode(node, op.lexeme, right, op.line)
        return node

    def parse_factor(self):
        node = self.parse_power()
        while self.current().type in ("MULT", "DIV", "MOD"):
            op = self.current()
            self.advance()
            right = self.parse_power()
            node = BinOpNode(node, op.lexeme, right, op.line)
        return node

    def parse_power(self):
        node = self.parse_unary()
        while self.current().type == "POW":
            op = self.eat("POW")
            right = self.parse_unary()
            node = BinOpNode(node, op.lexeme, right, op.line)
        return node

    def parse_unary(self):
        if self.current().type in ("MINUS", "NOT"):
            op = self.current()
            self.advance()
            expr = self.parse_unary()
            return UnaryOpNode(op.lexeme, expr, op.line)
        return self.parse_primary()
    