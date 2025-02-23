from src.Ast.Ast import * 
from src.Ast.NodeKinds import * 
from src.Ast.Expr import * 
from src.Ast.Types import *

class NullStmt(Stmt):
    def __init__(self):
        self.Kind: NodeKind = NodeKind.NullStmt 
    
    def __ToJson__(self) -> dict:
        return {
            "Kind" : "NullStmt"
        }
class ExprStmt(Stmt):
    def __init__(self, Expression: Expr):
        self.Expression: Expr = Expression 
        self.Kind: NodeKind = NodeKind.ExprStmt 

    def __ToJson__(self) -> dict:
        return self.Expression.__ToJson__()

class VarDec(Stmt):
    def __init__(self, VarType: Type, Mut: bool, Name: str, Value: Expr, Loc: dict = {}):
        self.Kind: NodeKind = NodeKind.VarDec
        self.VarType: Type = VarType
        self.Mut: bool = Mut
        self.Name: str = Name
        self.Val: Expr = Value
        self.Loc: dict = Loc

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "Variable Declaration",
            "VariableType" : self.VarType.__ToJson__(),
            "Mutatable" : self.Mut,
            "Name" : self.Name,
            "Value" : self.Val 
        } 

class ReturnStmt(Stmt):
    def __init__(self, RetVal: Expr, Loc: dict = {}):
        self.Kind: NodeKind = NodeKind.RetStmt 
        self.Val: Expr = RetVal
        self.Loc: dict = Loc

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "Return Expression",
            "Returning" : self.Val
        }

class FuncStmt(Stmt):
    def __init__(self, Name: str, RetType: Type, Parameters: list[ParameterExpr], Body: list[Stmt], Loc: dict = {}):
        self.Kind: NodeKind = NodeKind.FuncStmt
        self.RetType: Type = RetType 
        self.Parameters: list[ParameterExpr] = Parameters
        self.Body: list[Stmt] = Body
        self.Name: str = Name
        self.Loc: dict = Loc

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "FunctionExpression",
            "Name" : self.Name,
            "ReturnType" : self.RetType.__ToJson__(),
            "Parameters" : self.Parameters,
            "Body" : self.Body 
        }
