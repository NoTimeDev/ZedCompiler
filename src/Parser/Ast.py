#These Classes Really Just Works As NameSpaces
class Statement:
    VarDec : str = "VariableDeclarationStatement"

class Expression:
    BinExpr : str = "BinaryExpression"
    VarCall : str = "VariableCallExpression"

class Literal:
    IntLit : str = "IntegerLiteral"
    StrLit : str = "StringLiteral"
    FlLit : str = "FloatLiteral"

