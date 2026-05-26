





    ##parsing  de primarios y llamadasde funciones

def parse_primary(self):
    token=self.current()

    if token.type == "INT":
        self.advance()
        return NumberNode(int(token.lexeme),token.line)
    
    if token.type =="REAL":
        self.advance()
        return StringNode(token.lexeme,token.line)
    
    if token.type == "STRING":
        self.advance()
        return StringNode(token.lexeme,token.line)
    
    if token.type=="BOOL":
        self.advance()
        return BoolNode(token.lexeme=="true",token.line)
    if token.type=="ID":
        self.advance()
        if self.current().type=="LPAREN":
            self.eat("LPAREN")
            args=[]
            if self.current().type != "RPAREN":
                args.append(self.parse_expression())
                while self.current().type=="COMMA":
                    self.eat("COMMA")
                    args.append(self.parse_expression())
            self.eat("RPAREN")
            return FuncCallNode(token.lexeme,args,token.line)
        return VariableNode(token.lexeme, token.line)
    
    if token.type=="LPAREN":
        self.eat("LPAREN")
        expr=self.parse_expression()
        self.eat("RPAREN")
        return expr
    raise ParserError(f"Error en linea{token.line},columna{token.column}:" f"token inseperado {token.type}")

