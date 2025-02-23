from enum import Enum, auto

class NodeKind(Enum):
    IntExpr = auto()
    FloatExpr = auto() 
    BinExpr = auto()
    UnaryExpr = auto()

    ExprStmt = auto()
    ParameterExpr = auto()
    
    FuncStmt = auto()
    VarDec = auto()
    IntType = auto()
        
    IdentifierExpr = auto()
    
    VariableCallExpr = auto()
    FunctionCallExpr = auto()
    

    RetStmt = auto()
    DefArg = auto()
    ArgExpr = auto()

    NullExpr = auto()
    NullStmt = auto()
    NullType = auto()
    Null = auto()
