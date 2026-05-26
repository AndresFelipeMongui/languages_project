##Visualizacion del AST
def print_ast(node,indent=0):
    prefix=" " * indent 

    if isinstance(node,ProgramNode):
        print(prefix + "ProgramNode")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    elif isinstance(node, ProgramNode):
        print(prefix + "ProgramNode")
        for stm in node.statements:
            print_ast(stmt,indent + 1)

    elif isinstance(node,IfNode):
        print_ast(prefix+ "PrintNode")
        print_ast(node.expr, indent +1)
    
    elif isinstance(node,IfNode):
        print(prefix + "IfNode")
        print(prefix + " Condicion:")
        print_ast(node.condition, indent + 2)
        print(prefix + " Then: ")
        print_ast(node.then_block, indent + 2)
        if node.else_block:
            print(prefix + " Else:")
            print_ast(node.else_block,indent +2)
    
    elif isinstance(node,WhileNode):
        print(prefix + "WhileNode")
        print(prefix + " Condicion")
        print_ast(node.condition, indent +2)
        print(prefix + " Body:")
        print_ast(node.body,indent +2 )
    
    elif isinstance(node, FuncDefNode):
        print(prefix + f"FuncDefNode({node.name}, parametros {node.params})")
        print_ast(node.body,indent + 1)
    
    elif isinstance(node,ReturnNode):
        print(prefix + "ReturnNode")
        print_ast(node.expr, indent + 1)

    elif isinstance(node,FuncCallNode):
        print(prefix + f"CallNode({node.name})")
        for arg in node.args:
            print_ast(arg, indent + 1)
    
    elif isinstance(node, VariableNode):
        print(prefix + f"VariableNode({node.name})")
    
    elif isinstance(node,NumberNode):
        print(prefix+ f"NumberNode({node.value})")
    
    elif isinstance(node,StringNode):
        print(prefix+ f"StringNode({node.value})")
    
    elif isinstance(node, BoolNode):
        print(prefix + f"BoolNode({node.value})")
    
    elif isinstance(node, UnaryOpNode):
        print(prefix + f"UnitaryOpNode({node.op})")
    
    elif isinstance(node,BinOpNode):
        print(prefix + f"BinOpNode({node.op})")
        print_ast(node.left,indent + 1)
        print_ast(node.right,indent + 1)