from src.Lexer.TokenTypes import * 
from src.Parser.Ast import *
from src.Parser.LookUps import * 
from src.Environment.Environment import *
from src.Utils.Utils import *

class Parser:
    def __init__(self, Tokens: list, FileName : str, SourceLines : list[str], Notes : list[str], Env = None):
        self.Tokens : list = Tokens
        self.FileName : str = FileName
        self.Pos : int = 0
        self.SourceLines = SourceLines  

        self.Notes = Notes
        self.Err : int = 0

        self.Ast : dict = {
            "FileName" : FileName,
            "Body" : []
        }    


        self.NudLu : dict = {}
        self.LedLu : dict = {}
        self.StmtLu : dict = {}

        if Env == None:
            self.Env : Environment = Environment()
        else:
            self.Env : Environment = Env

        self.Environments : list[Environment] = []

        self.TokenLookUps()

    def CurrentToken(self) -> dict:
        return self.Tokens[self.Pos]
    
    def Advance(self) -> dict:
        Tk : dict = self.CurrentToken()
        self.Pos+=1

        return Tk
    
    def CurrentTokenKind(self):
        return self.CurrentToken().get("Type")
    
    def HasTokens(self) -> bool:
        return self.Pos < len(self.Tokens) and self.CurrentTokenKind() != TokenType.EOF
    
    def Parse(self) -> dict:
        while(self.HasTokens()):
            self.Ast['Body'].append(self.Parse_Stmt())

        if(self.Err != 0):
            exit(1)

        return self.Ast
    
    def Nud(self, TokType : TokenType, Bind : Binding_Power, Function) -> None:
        self.NudLu.update({TokType.value : Function})
        BpLookUp.update({TokType.value : Bind})

    def Led(self, TokType : TokenType, Bind : Binding_Power, Function) -> None:
        self.LedLu.update({TokType.value : Function})
        BpLookUp.update({TokType.value : Bind})

    def Stmt(self, TokType : TokenType, Function) -> None:
        self.StmtLu.update({TokType.value : Function})

    
    def TokenLookUps(self) -> None:
        self.Nud(TokenType.Int_Literal, Binding_Power.Primary, self.ParsePrimaryExpr)
        self.Nud(TokenType.Str_Literal, Binding_Power.Primary, self.ParsePrimaryExpr)
        self.Nud(TokenType.EOF, Binding_Power.Defualt_bp, self.ParsePrimaryExpr)
        self.Nud(TokenType.Identifier, Binding_Power.Call, self.ResovleCall)

        self.Led(TokenType.Plus, Binding_Power.Additive, self.ParseBinExpr)
        self.Led(TokenType.Minus, Binding_Power.Additive, self.ParseBinExpr)
        self.Led(TokenType.Star, Binding_Power.Multiplictive, self.ParseBinExpr)
        self.Led(TokenType.Forward_Slash, Binding_Power.Multiplictive, self.ParseBinExpr)
        
        self.Stmt(TokenType.Let, self.ParseVarDecStmt)
        self.Stmt(TokenType.Mut, self.ParseVarDecStmt)

    def GetType(self, Expr: dict):
        match(Expr.get("Kind")):
            case Literal.IntLit:
                ranges = {
                    "bool" : (0, 1),
                    "i8" : (-128, 127),
                    "i16" : (-32_768, 32_767),
                    "i32" : (-2_147_483_648, 2_147_483_647),
                    "i64" : (-9_223_372_036_854_775_808, 9_223_372_036_854_775_807),
                }

                for int_type, (min_val, max_val) in ranges.items():
                    if min_val <= int(Expr.get("Value")) <= max_val:
                        return [int_type]
                    
                return ["i64"]
                    
            case Literal.StrLit:
                return ["String"]
        
            case Expression.VarCall:
                return Expr.get("Type")
    
    def ResovleCall(self):
        #Is THis Calling A Fuction?, Class?, Struct?, Enum?, Variable?, Ect
        if(self.CurrentToken().get("Value") in list(self.Env.Variables.keys())):
            return self.ParseVarCallExpr()
    
    def ParseVarCallExpr(self):
        Identifer  = self.Advance()

        Stuff : dict = self.Env.GetVar(Identifer.get("Value"))

        return {
            "Kind" : Expression.VarCall,
            "Type" : Stuff.get("Type"),
            "Calling" : Identifer.get("Value"),
            "Mutable" : Stuff.get("Mutable"),
        }
    
    def ParseVarDecStmt(self) -> dict:
        KeyWord =  self.Advance()
        IsMut = KeyWord.get("Type") #If Let it is Constant Else it is Mutatable
        Identifer = self.Advance().get("Value")

        if(self.CurrentTokenKind() == TokenType.Colon_Equals):
            self.Advance()

            Value = self.Parse_Expr(Binding_Power.Defualt_bp)
            Type = self.GetType(Value)
            self.Expect(TokenType.Semi, ";")

            self.Env.DecVar(Identifer,
                            {
                "Kind" : Statement.VarDec,
                "Type" : Type,
                "Mutable" : True if IsMut == TokenType.Mut else False, #tenary operator but worse
                "Name" : Identifer,
                "Value" : Value,
            })
            return {
                "Kind" : Statement.VarDec,
                "Type" : Type,
                "Mutable" : True if IsMut == TokenType.Mut else False, #tenary operator but worse
                "Name" : Identifer,
                "Value" : Value,
            }
    
        else:
            self.Expect(TokenType.Colon, ":")


            Type = self.ParseType()
            if(self.CurrentTokenKind() == TokenType.Semi):
                if(IsMut != TokenType.Mut):
                    self.ErrorWithMsg(
                        "variable declartion must be mutable",
                        KeyWord.get("Line"),
                        KeyWord.get("Start"),
                        KeyWord.get("End"),
                        "mut",
                    )


                self.Expect(TokenType.Semi, ";")
                self.Env.DecVar(Identifer,
                            {
                    "Kind" : Statement.VarDec,
                    "Type" : Type,
                    "Mutable" : True if IsMut == TokenType.Mut else False, #tenary operator but worse
                    "Name" : Identifer,
                    "Value" : None,
                })
                
                return {
                    "Kind" : Statement.VarDec,
                    "Type" : Type,
                    "Mutable" : True,
                    "Name" : Identifer,
                    "Value" : None,
                }
    
        
            self.Expect(TokenType.Equal, "=")
        
            Value = self.Parse_Expr(Binding_Power.Defualt_bp)
            self.Expect(TokenType.Semi, ";")

            self.Env.DecVar(Identifer,
                        {
                "Kind" : Statement.VarDec,
                "Type" : Type,
                "Mutable" : True if IsMut == TokenType.Mut else False, #tenary operator but worse
                "Name" : Identifer,
                "Value" : Value,
            })

            return {
                "Kind" : Statement.VarDec,
                "Type" : Type,
                "Mutable" : True if IsMut == TokenType.Mut else False, #tenary operator but worse
                "Name" : Identifer,
                "Value" : Value,
            }
    
    def Expect(self, Type : TokenType, Name : str, Rep : str = "") -> dict:
        Token = self.Advance()

        if(Token.get("Type") != Type):
            printf(f"{Colour['BrightWhite']}{self.FileName}:{Token.get("Line")}:{Token.get("Start")} {Colour['BrightRed']}error:{Colour['BrightWhite']} Expected '{Name}' instead recived '{Token.get("Value")}'{Colour['Reset']}")
            printf(f"{Token.get("Line")}|{self.SourceLines[Token.get("Line") - 1]}")
            printf(f"{len(str(Token.get("Line"))) * ' '}|{(Token.get("Start") - 1) * ' '}{Colour['BrightRed']}{(int(Token.get("End")) - int(Token.get("Start")) + 1)  * '^'}{Colour['Reset']}")
            printf(f"{len(str(Token.get("Line"))) * ' '}|{(Token.get("Start") - 1) * ' '}{Colour['BrightBlue']}{Name}{Colour['Reset']}")
            self.Err+=1

        return Token

    def ErrorWithMsg(self, Msg : str, Line : int, Coloum : int, End : int , Rep : str, UnderLine : str = "^", ErrorName : str = "error"):
        printf(f"{Colour['BrightWhite']}{self.FileName}:{Line}:{Coloum} {Colour['BrightRed']}{ErrorName}:{Colour['BrightWhite']} {Msg}{Colour['Reset']}")
        printf(f"{Line}|{self.SourceLines[Line - 1]}")
        printf(f"{len(str(Line)) * ' '}|{(Coloum - 1) * ' '}{Colour['BrightRed']}{(int(End) - int(Coloum) + 1)  * UnderLine}{Colour['Reset']}")
        printf(f"{len(str(Line)) * ' '}|{(Coloum - 1) * ' '}{Colour['BrightGreen']}{Rep}{Colour['Reset']}")
        self.Err+=1


    def ParseType(self) -> list:
        Single = [
            "i64",
            "i32",
            "i16",
            "i8",

            "u64",
            "u32",
            "u16",
            "u8",

            "f32",
            "f64",

            "String",
    
            "bool",
        ]

        if(self.CurrentTokenKind() == TokenType.Type_):
            if(self.CurrentToken().get("Value") in Single):
                Type_ = self.Advance().get("Value")
                if(self.CurrentTokenKind() == TokenType.Open_Square_Paren):
                    Dimensions = []

                    self.Advance()

                    Dimensions.append(self.Advance().get("Value"))

                    self.Advance()
                    
                    
                    while(self.CurrentTokenKind() == TokenType.Open_Square_Paren):

                        self.Advance()

                        Dimensions.append(self.Advance().get("Value"))

                        self.Advance()

                    Type_ = {
                        "Type" : "Array",
                        "UnderType" : Type_,
                        "Dimensions" : len(Dimensions),
                        "Sizes" : Dimensions,
                    }
                return [Type_]
         
        #When Objects Are Added Do Something Else
    def ParsePrimaryExpr(self) -> dict:
        match(self.CurrentTokenKind()):
            case TokenType.Int_Literal:
                return {
                    "Kind" : Literal.IntLit,
                    "Value" : self.Advance().get("Value")
                }
            case TokenType.Str_Literal:
                return {
                    "Kind" : Literal.StrLit,
                    "Value" : self.Advance().get("Value")
                }
        
        return {}
    
    def Parse_Expr(self, Bp : Binding_Power):
        TokenKind = self.CurrentTokenKind()

        Nud_Fn = self.NudLu.get(TokenKind.value) # type: ignore

        Left = Nud_Fn() # type: ignore
        
        while(BpLookUp.get(self.CurrentTokenKind().value, TokenType.EOF).value > Bp.value): # type: ignore
            TokenKind = self.CurrentTokenKind()
            Led_Fn = self.LedLu.get(TokenKind.value) # type: ignore

            if(Led_Fn == None):
                return Left

            Left = Led_Fn(Left, BpLookUp.get(TokenKind.value)) # type: ignore
        
        return Left
    
    def ParseBinExpr(self, Left : dict, Bp : Binding_Power) -> dict:
        OpToken = self.Advance()
        Right = self.Parse_Expr(Bp)

        return {
            "Kind" : Expression.BinExpr,
            "Left" : Left,
            "Right" : Right,
            "Op" : OpToken.get("Type").name # type: ignore
        }   
    
    def Parse_Stmt(self):
        Stmt_Fn = self.StmtLu.get(self.CurrentTokenKind().value)
        if(Stmt_Fn != None):
            return Stmt_Fn()

        Expr = self.Parse_Expr(Binding_Power.Defualt_bp)
        self.Expect(TokenType.Semi, ";")
        return Expr

