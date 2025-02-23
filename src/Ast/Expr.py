from src.Ast.Ast import *
from src.Ast.NodeKinds import * 
from src.Lexer.TokenKind import *

class NullExpr(Expr):
    def __init__(self):
        self.Kind: NodeKind = NodeKind.NullExpr

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "NullExpr"
        }

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
    def __init__(self, expression: Expr, Loc: dict = {}):
        self.Kind: NodeKind = NodeKind.UnaryExpr
        self.Loc: dict = Loc
        self.expression: Expr = expression

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "Unary Expression",
            "Expression" : self.expression.__ToJson__()
        }
        
class ParameterExpr(Expr):
    def __init__(self, Name: str, Mut: bool, VarType: Type, Loc: dict = {}, Val: Expr = NullExpr()):
        self.Kind: NodeKind = NodeKind.ParameterExpr
        self.Name: str = Name
        self.Mut: bool = Mut
        self.VarType: Type = VarType
        self.Val: Expr = Val 
        self.Loc: dict = Loc

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "Parameter Expression",
            "Name" : self.Name,
            "Type" : self.VarType.__ToJson__(),
            "Mutatable" : self.Mut ,
            "Value" : self.Val,
        }

class DefArg(Expr):
    def __init__(self, Val: Expr, Name: str, Loc: dict = {}):
        self.Kind: NodeKind = NodeKind.DefArg
        self.Name: str = Name
        self.Val: Expr = Val
        self.Loc: dict = Loc

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "Default Argument Expr",
            "Name" : self.Name,
            "Value" : self.Val
        }

class ArgumentExpr(Expr):
    def __init__(self, Val: Expr, Loc: dict = {}, Name: str = "!PositionalArg"):
        self.Kind: NodeKind = NodeKind.ArgExpr 
        self.Name: str = Name
        self.Value: Expr = Val
        self.Loc: dict = Loc

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "ArgumentExpr",
            "Name" : self.Name,
            "Value" : self.Value,
        }

class IdentifierExpr(Expr):
    def __init__(self, Name: str, Args: list[ArgumentExpr], HasArgs: bool, Loc: dict= {}):
        self.Kind: NodeKind = NodeKind.IdentifierExpr
        self.Name: str = Name 
        self.Args: list[ArgumentExpr] = Args
        self.Loc: dict = Loc 
        self.HasArgs: bool = HasArgs

    def __ToJson__(self) -> dict:
        return {
            "Kind" : "Identifier Expr",
            "Name" : self.Name,
            "Params" : self.Args,
            "HasArgs" : self.HasArgs
        }

