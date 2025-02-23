from src.Ast.NodeKinds import *

class Stmt:
    Kind: NodeKind = NodeKind.Null  
    Loc: dict = {}

    def __ToJson__(self) -> dict:
        return {}
    
class Expr:
    Kind: NodeKind = NodeKind.Null
    Loc: dict = {}

    def __ToJson__(self) -> dict:
        return {}

class Type:
    Kind: NodeKind = NodeKind.Null
    Loc: dict = {}

    def __ToJson__(self) -> dict:
        return {}

class Program:
    def __init__(self, Body: list[Stmt]):
        self.Body: list[Stmt] = Body
    
    def __ToJson__(self) -> dict:
        return {
            "Kind" : "Program",
            "Body" : self.Body
        }

