from src.Lexer.TokenKind import *


num: int = -1
def auto():
    global num
    num+=1
    return num 

class BindingPower:
    def_bp = auto()
    comma = auto()
    assigment = auto()
    logical = auto()
    relational = auto()
    additive = auto()
    multiplicative = auto()
    power = auto()
    unary = auto()
    call = auto()
    member = auto()
    primary = auto()


bp_lu: dict[TokenKind, int] = {} 
nud_lu: dict = {} 
led_lu: dict = {} 
stmt_lu: dict = {} 

def led(Kind: TokenKind, Bp: int, led_fn):
    bp_lu[Kind] = Bp 
    led_lu[Kind] = led_fn

def nud(Kind: TokenKind, nud_fn):
    bp_lu[Kind] = BindingPower.primary
    nud_lu[Kind] = nud_fn

def stmta(Kind: TokenKind, stmt_fn):
    bp_lu[Kind] = BindingPower.def_bp
    stmt_lu[Kind] = stmt_fn


        
