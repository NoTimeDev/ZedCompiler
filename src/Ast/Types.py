from .NodeKinds import *
from .Ast import *
from enum import Enum, auto

class BasicTypes(Enum):
    i64 = auto()
    i32 = auto()
    i16 = auto()
    i8 = auto()
    
    f64 = auto()
    f32 = auto()

class NullType(Type):
    def __init__(self):
        self.Kind: NodeKind = NodeKind.NullType
    def __ToJson__(self) -> dict:
        return {
            "Kind" : "NullType"
        }
class IntType(Type):
    def __init__(self, IntType: BasicTypes):
        self.Kind: NodeKind = NodeKind.IntType 
        self.IntType: BasicTypes = IntType
    
    def __ToJson__(self) -> dict:
        return {
            "Kind" : "IntType",
            "IntType" : self.IntType.name
        } 

