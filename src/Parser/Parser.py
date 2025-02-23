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
        
        nud(TokenKind.Identifier, self.ParseIdentifer)
        
        nud(TokenKind.Sub, self.ParseUnary)
        


        stmta(TokenKind.Return, self.ParseRet)
        stmta(TokenKind.Mut, self.ParseVarDec)
        stmta(TokenKind.Const, self.ParseVarDec)
        stmta(TokenKind.Func, self.ParseFunc)
    def Peek(self, Num):
        try:
            self.Tokens[self.Pos + Num]
        except IndexError:
            return NullToken
        else:
            return self.Tokens[self.Pos + Num]

    def Expect(self, Kind: TokenKind, Val: str, Colour=BrightRed, MisColour=BrightRed, expc: str = "\";\"") -> Token:
        tk: Token = self.Advance()
        if tk.Kind != Kind:
            if (tk.Line - self.Peek(-2).Line) == 0:
                self.Err.ThrowErr(tk.Line, tk.Start, tk.End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected {expc} but recived '{tk.Value}'){Reset}", Missing=Val, Colour=Colour, MisColour=MisColour)
            else:
                self.Err.ThrowErrorInNewLine(tk.Line, tk.Start, tk.End, self.Peek(-2).Line, self.Peek(-2).Start, self.Peek(-2).End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected {expc} but recived '{tk.Value}'){Reset}", Missing=Val, Colour=Colour, MisColour=MisColour)

            return NullToken
        return tk 
    def Eof_Err(self):
        tk = self.CurrentToken()
        self.Err.ThrowErr(tk.Line, tk.Start, tk.End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(end of file error){Reset}", Missing="^EOF", Colour=Red, MisColour=Green)
        self.Err.Exit()

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
    
    def ParseRet(self) -> Stmt:
        self.Advance()

        Val = self.ParseExpr(BindingPower.def_bp)
        self.Expect(TokenKind.Semi, ";", Colour=Green, expc="';'")
        return ReturnStmt(Val)

    def ParseArgs(self) -> list[ArgumentExpr]:
        self.Expect(TokenKind.Open_Brack, "(", MisColour=Green, expc="'('")
        
        Args = []

        while self.CurrentTokenKind() != TokenKind.Close_Brack or self.CurrentTokenKind() != TokenKind.EOF:
            if self.CurrentTokenKind() == TokenKind.EOF:
                self.Eof_Err()
            elif self.CurrentTokenKind() == TokenKind.Close_Brack:
                break
            elif self.CurrentTokenKind() == TokenKind.Comma:
                self.Advance()
            else: 
                tk = self.CurrentToken()
                expr = self.ParseExpr(BindingPower.def_bp)
                #later check if the current toke is = to do add like x = 4
                if self.CurrentTokenKind() == TokenKind.Equal:
                    self.Advance()
                    if expr.Kind != NodeKind.IdentifierExpr:
                        if (tk.Line - self.Peek(-2).Line) == 0:
                            self.Err.ThrowErr(tk.Line, tk.Start, tk.End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(a defualt variable must have a name){Reset}", Missing="", Colour=Green, MisColour=BrightRed)
                        else:
                            self.Err.ThrowErrorInNewLine(tk.Line, tk.Start, tk.End, self.Peek(-2).Line, self.Peek(-2).Start, self.Peek(-2).End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(a defualt variable must have a name){Reset}", Missing="", Colour=Green, MisColour=BrightRed)
                    else:
                       Args.append(DefArg(self.ParseExpr(BindingPower.def_bp), expr.Name)) 
                else: 
                    Args.append(expr)
        self.Expect(TokenKind.Close_Brack, ")", MisColour=Green, expc="')'")
        return Args 
    def ParseIdentifer(self) -> Expr:
        Name = self.Advance()
        if self.CurrentTokenKind() == TokenKind.Open_Brack:
            HArgs = True
            Args = self.ParseArgs()
        else:
            HArgs = False
            Args = []

        return IdentifierExpr(Name.Value, Args, HArgs, Loc={
            "Start_Name" : Name.Start,
            "Line_Name" : Name.Line,
            "End_Name" : Name.End
        })

    def ParseVarDec(self) -> Stmt:
        Mut = self.Advance().Kind == TokenKind.Mut
        Name = self.Expect(TokenKind.Identifier, "^Identifier", MisColour=Green, expc="an identifier")
                
        self.Expect(TokenKind.Colon, ":", MisColour=Green, expc="':'")
                
        VarType = self.ParseType()
        
        if self.CurrentTokenKind() == TokenKind.Semi:
            if Mut == False:
                tk = self.Advance()
                if (tk.Line - self.Peek(-2).Line) == 0:
                    self.Err.ThrowErr(tk.Line, tk.Start, tk.End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(A constant variable must have a value){Reset}", Missing="?", Colour=Green, MisColour=Red)
                else:
                    self.Err.ThrowErrorInNewLine(tk.Line, tk.Start, tk.End, self.Peek(-2).Line, self.Peek(-2).Start, self.Peek(-2).End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(A constant variable must have a value){Reset}", Missing="?", Colour=Green, MisColour=Red)
                return NullStmt()
            
            self.Advance()
            return VarDec(VarType, Mut, Name.Value, NullExpr(), Loc={
                "Line_Name" : Name.Line,
                "Start_Name" : Name.Start,
                "End_Name" : Name.End,
            })
        
        self.Expect(TokenKind.Equal, "=", MisColour=Green, expc="'='")
        Val = self.ParseExpr(BindingPower.def_bp)
        self.Expect(TokenKind.Semi, ';', MisColour=Green, expc="';'")

        return VarDec(VarType, Mut, Name.Value, Val, Loc={
            "Line_Name" : Name.Line,
            "Start_Name" : Name.Start,
            "End_Name" : Name.End,
        })

    def ParseType(self) -> Type:
        if self.CurrentTokenKind() == TokenKind.Type:
            BType = self.Advance()
            GetType: dict[str, BasicTypes] = {
                "i64" : BasicTypes.i64,
                "i32" : BasicTypes.i32,
                "i16" : BasicTypes.i16,
                "i8" : BasicTypes.i8,
                
                "f64" : BasicTypes.f64,
                "f32" : BasicTypes.f32,
            }

            return IntType(GetType[BType.Value])
        else:
            self.Expect(TokenKind.Type, "^type eg. i32, i64", MisColour=Green, expc="some type")
        
        return NullType()
    def ParseParams(self) -> list[ParameterExpr]:
        Params: list[ParameterExpr] = []
        self.Expect(TokenKind.Open_Brack, "(", MisColour=Green, expc="'('")
        while self.CurrentTokenKind() != TokenKind.Close_Brack or self.CurrentTokenKind() != TokenKind.EOF:
            if self.CurrentTokenKind() == TokenKind.EOF:
                self.Eof_Err()
            elif self.CurrentTokenKind() == TokenKind.Close_Brack:
                break
            elif self.CurrentTokenKind() not in [TokenKind.Const, TokenKind.Mut]:
                self.Expect(TokenKind.Mut, "^mut or const", MisColour=Green, expc="mut or const to define a parameter")
            else:
                Mut = self.Advance().Kind == TokenKind.Mut
                Name = self.Expect(TokenKind.Identifier, "^Identifier", MisColour=Green, expc="an identifier")
                
                self.Expect(TokenKind.Colon, ":", MisColour=Green, expc="':'")
                
                vType = self.ParseType()
                
                if self.CurrentTokenKind() == TokenKind.Equal:
                    self.Advance()

                    def_val = self.ParseExpr(BindingPower.def_bp)
                     
                    Params.append(ParameterExpr(Name.Value, Mut, vType, Val=def_val, Loc={
                        "Line_Name" : Name.Line,
                        "Start_Name" : Name.Start,
                        "End_Name" : Name.End,
                    }))
                else:
                    Params.append(ParameterExpr(Name.Value, Mut, vType, Loc={
                        "Line_Name" : Name.Line,
                        "Start_Name" : Name.Start,
                        "End_Name" : Name.End,
                    }))
                
                #--Later SUpport Defualt Vars SOON!--
                if self.CurrentTokenKind() == TokenKind.Comma:
                    self.Advance()


        self.Expect(TokenKind.Close_Brack, ")", MisColour=Green, expc="')'")
        return Params
    def ParseFunc(self) -> Stmt:
        self.Advance()

        Name = self.Expect(TokenKind.Identifier, "^Identifier", MisColour=Green, expc="an identifier")
        

        Params = self.ParseParams()
    
        self.Expect(TokenKind.SArrow, "->", MisColour=Green, expc="'->'")
        RetType = self.ParseType()

        Body: list[Stmt] = []

        self.Expect(TokenKind.Curly_Open_Brack, "{", MisColour=Green, expc="'{'")
        while self.CurrentTokenKind() != TokenKind.Curly_Close_Brack or self.CurrentTokenKind() != TokenKind.EOF:
            if self.CurrentTokenKind() == TokenKind.EOF:
                self.Eof_Err()
            elif self.CurrentTokenKind() == TokenKind.Curly_Close_Brack:
                break
            else:
                Body.append(self.ParseStmt())                
        self.Expect(TokenKind.Curly_Close_Brack, "}", MisColour=Green, expc="'}'")
        
        return FuncStmt(Name.Value, RetType,Params, Body, Loc={
            "Start_Name" : Name.Start,
            "End_Name" : Name.End,
            "Line_Name" : Name.Line
        })

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
            {}
        )

    def ParseUnary(self) -> Expr:
        tk: Token = self.Advance()
        expr: Expr = self.ParseExpr(BindingPower.def_bp)
        

        if expr.Kind == NodeKind.IntExpr:
            expr = cast(IntExpr, expr)
            if int(expr.Integer) < 129:
                return IntExpr(f"-{expr.Integer}", "i8", {}) 
            elif int(expr.Integer) < 32769:
                return IntExpr(f"-{expr.Integer}", "i16", {})
            elif int(expr.Integer) < 2_147_483_649:
                return IntExpr(f"-{expr.Integer}", "i32", {})
            else:
                return IntExpr(f"-{expr.Integer}", "i64", {})
        elif expr.Kind == NodeKind.FloatExpr:
            expr = cast(FloatExpr, expr)
            return FloatExpr(f"-{expr.Float}", expr.Size, {})
        else:
            return UnaryExpr(expr)
    
    def ParseExpr(self, bp: int) -> Expr:
        Tk_Kind: TokenKind = self.CurrentTokenKind()
        nud_fn = nud_lu.get(Tk_Kind)

        if nud_fn == None:
            tk: Token = self.CurrentToken()
            if (tk.Line - self.Peek(-2).Line) == 0:
                self.Err.ThrowErr(tk.Line, tk.Start, tk.End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected an expression but recived '{tk.Value}'){Reset}", Missing="^ Expression", MisColour=BrightGreen)
            else:
                self.Err.ThrowErrorInNewLine(tk.Line, tk.Start, tk.End, self.Peek(-2).Line, self.Peek(-2).Start, self.Peek(-2).End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected an expression but recived '{tk.Value}'){Reset}", Missing="^ Expression", MisColour=BrightGreen)

            return NullExpr() 

        left: Expr = nud_fn() #type: ignore

        while(bp_lu.get(self.CurrentTokenKind(), BindingPower.def_bp) > bp):
            led_fn = led_lu.get(self.CurrentTokenKind())
            if led_fn == None:
                tk: Token = self.CurrentToken()
                  
                if (tk.Line - self.Peek(-2).Line) == 0: 
                    self.Err.ThrowErr(tk.Line, tk.Start, tk.End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected \";\" but recived '{tk.Value}'){Reset}", Missing=";", MisColour=BrightGreen) 
                else:
                    self.Err.ThrowErrorInNewLine(tk.Line, tk.Start, tk.End, self.Peek(-2).Line, self.Peek(-2).Start, self.Peek(-2).End, f"{UBrightMagenta}Parser Error:{Reset} {BrightRed}(Expected \";\" but recived '{tk.Value}'){Reset}", Missing=";", MisColour=BrightGreen)
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


