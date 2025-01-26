from src.Ast.Ast import *
from src.Ast.NodeKinds import * 
from src.Lexer.TokenKind import *

class NullExpr(Expr):
    def __init__(self):
        pass 

class IntExpr(Expr):
    def __init__(self, Integer: str, Size: str, Loc: dict): 
        self.Kind = NodeKind.IntExpr
        self.Integer: str = Integer
        self.Size: str = Size
        self.Loc: dict = Loc #TypeChecker wow

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "Integer Expression",
            "Value" : self.Integer,
            "Size" : self.Size,
            "Locations" : self.Loc 
        }
    
  

class FloatExpr(Expr):
    def __init__(self, Float: str, Size: str, Loc: dict):
        self.Kind = NodeKind.FloatExpr
        self.Float: str = Float
        self.Size: str = Size 
        self.Loc: dict = Loc
    
    def __ToJson__(self) -> dict:
        return {
            "Kind" : "Float Expression",
            "Value" : self.Float,
            "Size" : self.Size,
            "Locations" : self.Loc
        }
    
class BinExpr(Expr):
    def __init__(self, Left: Expr, Right: Expr, Op: Token, Loc: dict):
        self.Kind = NodeKind.BinExpr 
        self.Left: Expr = Left
        self.Right: Expr = Right
        self.Op: Token = Op 
        self.Loc: dict = Loc

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "Binary Expression",
            "Left" : self.Left.__ToJson__(),
            "Right" : self.Right.__ToJson__(),
            "Op" : self.Op.Value  
        }
    
class UnaryExpr(Expr):
    def __init__(self, expression: Expr):
        self.Kind = NodeKind.UnaryExpr
        self.expression: Expr = expression

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "Unary Expression",
            "Expression" : self.expression.__ToJson__()
        }
        
