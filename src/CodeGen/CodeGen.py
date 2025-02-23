from typing import cast

from src.Ast.Expr import *
from src.Ast.Stmt import *
from src.Ast.Ast import * 
from src.Ast.NodeKinds import *
from src.Lexer.TokenKind import * 

class CodeGen:
    def __init__(self, Ast: Program):
        self.Ast: Program = Ast

    def Generate(self):
        pass 
