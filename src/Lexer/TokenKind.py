from enum import Enum, auto

class TokenKind(Enum):
    Add = auto()
    Add_Assingnment = auto()
    Inc = auto()

    Sub = auto()
    Sub_Assingnment = auto()
    Dec = auto()

    Mul = auto()
    Mul_Assingnment = auto()
    
    Exponent = auto()
    Exponent_Assignment = auto()

    Div = auto()
    Div_Assignment = auto()

    Mod = auto()
    Mod_Assignment = auto()

    Less_Than = auto()
    Less_Than_oeqt = auto()

    Greater_Than = auto()
    Greater_Than_oeqt = auto()
    
    Equal = auto()
    Equality = auto()
    Not_eq = auto()
    
    Bit_Not = auto()
    
    Bit_Xor = auto()
    Bit_Xor_Assignment = auto()

    LShift = auto()
    RShift = auto()
    
    LShift_Assignmet = auto()
    RShift_Assignment = auto()

    Log_Not = auto()
    
    Bit_Or = auto()
    Log_Or = auto()
    Bit_Or_Assigment = auto()

    Bit_And = auto()
    Log_And = auto()
    Bit_And_Assingment = auto()
    
    Comma = auto()
    Colon = auto()
    DColon = auto()
    Walrus = auto()
    
    DArrow = auto()

    Dot = auto()
    SArrow = auto()
    Tenary = auto()

    Open_Brack = auto()
    Close_Brack = auto()

    Curly_Open_Brack = auto()
    Curly_Close_Brack = auto()
    
    Square_Open_Brack = auto()
    Square_Close_Brack = auto()
    
    Type = auto()

    Func = auto()
    Struct = auto()
    Interface = auto() 
    Union = auto()
    Impl = auto()
    Const = auto()
    Static = auto()
    Mut = auto()
    ENUM = auto()
    Pub = auto()
    Priv = auto()


    Pre_If = auto()
    Pre_End = auto()
    Pre_Else = auto()
    Pre_Elif = auto()
    Pre_Define = auto()

    In = auto()
    Return = auto()
    New = auto()
    Del = auto()
    As = auto()
    Module = auto()
    Import = auto()
    Asm = auto()
    Extern = auto()
    From = auto()
    Def = auto()
    Defer = auto()

    If = auto()
    Elif = auto()
    Else = auto()
    For = auto()
    While = auto()
    Break = auto()
    Continue = auto()
    Match = auto()

    Int = auto()
    Float = auto()
    String = auto()
    Char = auto()
    Identifier = auto()
    EOF = auto()
  
    Semi = auto()
    Null = auto()
class Token:
    def __init__(self, Kind: TokenKind, Value: str, Start: int, End: int, Line: int):
        self.Kind: TokenKind = Kind
        self.Value: str = Value
        self.Start: int = Start
        self.End: int = End
        self.Line: int = Line

    def __repr__(self) -> str:
        return "{" + f'"Kind" : {self.Kind}, "Value" : "{self.Value}", "Line" : {self.Line}, "Start" : {self.Start}, "End" : {self.End}' + "}"

NullToken: Token = Token(TokenKind.Null, "Null", 0, 0, 0)
