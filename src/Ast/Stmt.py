from src.Ast.Ast import * 
from src.Ast.NodeKinds import * 

class NullStmt(Stmt):
    def __init__(self):
        pass 

class ExprStmt(Stmt):
    def __init__(self, Expression: Expr):
        self.Expression: Expr = Expression 

    def __ToJson__(self) -> dict:
        return self.Expression.__ToJson__()

   
