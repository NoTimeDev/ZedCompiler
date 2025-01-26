from enum import Enum, auto

class NodeKind(Enum):
    IntExpr = auto()
    FloatExpr = auto() 
    BinExpr = auto()
    UnaryExpr = auto()


    Null = auto()
