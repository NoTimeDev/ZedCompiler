from src.Error.Error import *
from src.Parser.Lookups import *
from src.Utils.Utils import *
from src.Lexer.TokenKind import *
from typing import cast

from src.Ast.Expr import *
from src.Ast.Ast import *
from src.Ast.Stmt import * 

class Parser:
    def __init__(self, ErrorClass: Error, Tokens: list[Token]):
        self.Err: Error = ErrorClass
        self.Tokens: list[Token] = Tokens
        
        self.Pos: int = 0

        self.Ast: Program = Program([])
        self.CreateTokenLookups()

    def CreateTokenLookups(self):
        #Additive, Powers & Multiplicitive

        led(TokenKind.Add, BindingPower.additive ,self.Parse_Binary_Expr)
        led(TokenKind.Sub, BindingPower.additive ,self.Parse_Binary_Expr)

        led(TokenKind.Mul, BindingPower.multiplicative, self.Parse_Binary_Expr)
        led(TokenKind.Div, BindingPower.multiplicative, self.Parse_Binary_Expr)
        led(TokenKind.Mod, BindingPower.multiplicative, self.Parse_Binary_Expr)
       
        led(TokenKind.Exponent, BindingPower.power, self.Parse_Binary_Expr)
        
        nud(TokenKind.Int, self.ParsePrimary)
        nud(TokenKind.Float, self.ParsePrimary)
        
        nud(TokenKind.Sub, self.ParseUnary)
    def Peek(self, Num):
        try:
            self.Tokens[self.Pos + Num]
        except IndexError:
            return NullToken
        else:
            return self.Tokens[self.Pos + Num]

    def Expect(self, Kind: TokenKind, Val: str, Colour=BrightRed, MisColour=BrightRed) -> Token:
        tk: Token = self.Advance()
        if tk.Kind != Kind:
            if (tk.Line - self.Peek(-1).Line) == 0:
                self.Err.ThrowErr(tk.Line, tk.Start, tk.End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected \";\" but recived '{tk.Value}'){Reset}", Missing=Val, Colour=Colour, MisColour=MisColour)
            else:
                self.Err.ThrowErrorInNewLine(self.Peek(-1).Line, self.Peek(-1).Start, self.Peek(-1).End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected \";\" but recived '{tk.Value}'){Reset}", Missing=Val, Colour=Colour, MisColour=MisColour)

            self.Enter_Error_Recovery()
            return NullToken

    def Enter_Error_Recovery(self):
        while self.HasTokens() and self.CurrentTokenKind() != TokenKind.Semi:
            self.Advance()
        

    def CurrentToken(self) -> Token:
        return self.Tokens[self.Pos]
    
    def Advance(self) -> Token:
        tk: Token = self.CurrentToken()
        self.Pos+=1
        return tk 
    
    def CurrentTokenKind(self) -> TokenKind:
        return self.CurrentToken().Kind

    def HasTokens(self) -> bool:
        return self.Pos < len(self.Tokens) and self.CurrentTokenKind() != TokenKind.EOF


    def Parse(self) -> Program:
        
        while self.HasTokens():
            self.Ast.Body.append(self.ParseStmt())
        
        self.Err.Exit()
        return self.Ast
     
    def ParsePrimary(self) -> Expr:
        match self.CurrentTokenKind():
            case TokenKind.Int:
                tk: Token = self.Advance()
                Size: str = ""
                
                if int(tk.Value) < 2:
                    Size = "i1"
                elif int(tk.Value) < 256:
                    Size = "u8"
                elif int(tk.Value) < 65_536:
                    Size = "u16"
                elif int(tk.Value) < 4_294_967_296:
                    Size = "u32"
                else: 
                    #Expand Elif Statements if i128+ will be added 
                    Size = "u64"

                return IntExpr(tk.Value, Size, {"Start": tk.Start, "End": tk.End})
            case TokenKind.Float:
                tk: Token = self.Advance()
                Size: str = ""

                if float(tk.Value) < 16_777_217:
                    Size = "f32"
                else:
                    Size = "f64"

                return IntExpr(tk.Value, Size, {"Start": tk.Start, "End": tk.End})

        return Expr()
    
    def Parse_Binary_Expr(self, left: Expr, bp: int) -> Expr:
        op_tk: Token = self.Advance()
        right: Expr = self.ParseExpr(BindingPower.def_bp)

        return BinExpr( 
            left,
            right,
            op_tk,
            {"rightLocs": right.Loc, "LeftLocs" : left.Loc, "OpStart" : op_tk.Start, "OpEnd" : op_tk.End}
        )

    def ParseUnary(self) -> Expr:
        tk: Token = self.Advance()
        expr: Expr = self.ParseExpr(BindingPower.def_bp)
        

        if expr.Kind == NodeKind.IntExpr:
            expr = cast(IntExpr, expr)
            if int(expr.Integer) < 129:
                return IntExpr(f"-{expr.Integer}", "i8", {"Start": tk.Start, "End" : expr.Loc.get("End")}) 
            elif int(expr.Integer) < 32769:
                return IntExpr(f"-{expr.Integer}", "i16", {"Start": tk.Start, "End" : expr.Loc.get("End")})
            elif int(expr.Integer) < 2_147_483_649:
                return IntExpr(f"-{expr.Integer}", "i32", {"Start": tk.Start, "End" : expr.Loc.get("End")})
            else:
                return IntExpr(f"-{expr.Integer}", "i64", {"Start": tk.Start, "End" : expr.Loc.get("End")})
        elif expr.Kind == NodeKind.FloatExpr:
            expr = cast(FloatExpr, expr)
            return FloatExpr(f"-{expr.Float}", expr.Size, {"Start": tk.Start, "End" : expr.Loc.get("End")})
        else:
            return UnaryExpr(expr)
    
    def ParseExpr(self, bp: int) -> Expr:
        Tk_Kind: TokenKind = self.CurrentTokenKind()
        nud_fn = nud_lu.get(Tk_Kind)

        if nud_fn == None:
            tk: Token = self.CurrentToken()
            if (tk.Line - self.Peek(-1).Line) == 0:
                self.Err.ThrowErr(tk.Line, tk.Start, tk.End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected an expression but recived '{tk.Value}'){Reset}", Missing="^ Expression", MisColour=BrightGreen)
            else:
                self.Err.ThrowErr(self.Peek(-1).Line, self.Peek(-1).Start, self.Peek(-1).End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected an expression but recived '{tk.Value}'){Reset}", Missing="^ Expression", MisColour=BrightGreen)

            self.Enter_Error_Recovery()
            return NullExpr() 

        left: Expr = nud_fn() #type: ignore

        while(bp_lu.get(self.CurrentTokenKind(), BindingPower.def_bp) > bp):
            led_fn = led_lu.get(self.CurrentTokenKind())
            if led_fn == None:
                tk: Token = self.CurrentToken()
                
                if (tk.Line - self.Peek(-1).Line) == 0: 
                    self.Err.ThrowErr(tk.Line, tk.Start, tk.End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected \";\" but recived '{tk.Value}'){Reset}", Missing=";", MisColour=BrightGreen) 
                else:
                    self.Err.ThrowErrorInNewLine(self.Peek(-1).Line, self.Peek(-1).Start, self.Peek(-1).End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected \";\" but recived '{tk.Value}'){Reset}", Missing=";", MisColour=BrightGreen)
                self.Enter_Error_Recovery()
                return NullExpr()
                
            left = led_fn(left, bp_lu[self.CurrentTokenKind()]) #type: ignore

        return left 
    
    def ParseStmt(self) -> Stmt: #type: ignore
        stmt_fn = stmt_lu.get(self.CurrentTokenKind())
        if stmt_fn != None:
            return stmt_fn()
        
        expr: Expr = self.ParseExpr(BindingPower.def_bp)
        self.Expect(TokenKind.Semi, ";", MisColour=Green)

        return ExprStmt(
            expr 
        )


