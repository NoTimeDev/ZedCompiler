from enum import Enum, auto

class TokenType(Enum):
    #Operators
    Plus = auto() 
    Minus = auto() 
    Star = auto() 
    Forward_Slash = auto() 
    
    #Symbols
    Open_Paren = auto() 
    Close_Paren = auto() 

    Open_Square_Paren = auto()
    Close_Square_Paren = auto()
    
    Semi = auto()
    Equal = auto()
    
    Colon = auto()
    Colon_Equals = auto()

    Open_Arrow = auto()
    Close_Arrow = auto()


    #Types
    Type_ = auto()

    #KeyWords
    Let = auto()
    Mut = auto()

    #Literals
    Int_Literal = auto()
    Str_Literal = auto()
    Float_Literal = auto()

    #Other
    Identifier = auto()
    EOF = auto()
    NULL = auto()