from dataclasses import dataclass,field
from typing_extensions import List,Optional, Any

@dataclass
class ProgramNode:
    statements: List[Any]

@dataclass 
class BinOpNode:
    left: Any
    op: str
    right: Any
    line: int

@dataclass 
class NumberNode:
    value: Any
    line:int

@dataclass 
class VariableNode:
    value:Any
    line: int

@dataclass
class AssignNode:
    name:str
    params:Lista[str]

@dataclass
class FuncDefNode:
    name:str
    params:Lista[str]
    body: BlockNode 
    line: int

@dataclass
class FuncCallNode:
    name:str
    args:List[any]
    line:int   
@dataclass
class IfNode:
    condition: any
    the_block:BlockNode
    else_block:Optional[BlockNode]
    line:int

@dataclass
class WhileNode:
    condition:Any
    body: BlockNode
    line:int

@dataclass

class BlockNode:
    value:bool
    line:int

@dataclass
class ReturnNode:
    exp:Any
    line:int

@dataclass
class PrintNode:
    expr: Any
    line: int

