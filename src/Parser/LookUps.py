from enum import Enum
from src.Lexer.TokenTypes import * 

class Binding_Power(Enum):
    Defualt_bp = 0
    Comma = 1
    Assingment = 2
    Logical = 3
    Relational = 4
    Additive = 5
    Multiplictive = 6 
    Unary = 7
    Call = 8
    Member = 9
    Primary = 10


BpLookUp : dict = {

}