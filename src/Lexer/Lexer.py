from src.Lexer.TokenKind import *
from src.Utils.Utils import *

class Lexer:
    def __init__(self, FileName: str, SourceCode: str, ImportingFrom: list[str] = []):
        self.FileName: str = FileName
        self.SourceCode: str = SourceCode
        self.SourceLines: list[str] = SourceCode.split('\n')
        self.ImportingFrom: list[str] = ImportingFrom
        self.Err: int = 0 

        self.Alphas: dict[str, TokenKind] = {
            "func":TokenKind.Func,
            "struct": TokenKind.Struct,
            "union" : TokenKind.Union,
            "impl" : TokenKind.Impl,
            "interface" : TokenKind.Interface,

            "for" : TokenKind.For,
            "while" : TokenKind.While,

            "const" : TokenKind.Const,
            "mut" : TokenKind.Mut,
            "static" : TokenKind.Static,

            "if" : TokenKind.If,
            "elif" : TokenKind.Elif,
            "else" : TokenKind.Else,

            "match" : TokenKind.Match,
            "break" : TokenKind.Break,
            "continue" : TokenKind.Continue,

            "char" : TokenKind.Type,
            "i28" : TokenKind.Type,
            "i64" : TokenKind.Type,
            "i32" : TokenKind.Type,
            "i16" : TokenKind.Type,
            "i8" : TokenKind.Type,

            "ui28" : TokenKind.Type,
            "u64" : TokenKind.Type,
            "u32" : TokenKind.Type,
            "u16" : TokenKind.Type,
            "u8" : TokenKind.Type,

            "Self" : TokenKind.Type,
            "String" : TokenKind.Type,

            "enum" : TokenKind.ENUM,
            "pub" : TokenKind.Pub,
            "priv" : TokenKind.Priv,
            "new" : TokenKind.New,
            "del" : TokenKind.Del,
            "as" : TokenKind.As,
            "mod" : TokenKind.Module,
            "import" : TokenKind.Import,
            "asm" : TokenKind.Asm,
            "return" : TokenKind.Return,
            "in" : TokenKind.In,
            "extern" : TokenKind.Extern,
            "from" : TokenKind.From,
            "defer" : TokenKind.Defer,
            "def" : TokenKind.Def
        }

    def Lex(self) -> list[Token]:
        Tokens: list[Token] = []

        def Add(Token):
            Tokens.append(Token)
            
        Pos: int = 0
        Coloum: int = 1
        Line: int = 1
        
        def Peek(num: int=1):
            return self.SourceCode[Pos + 1 + num - 1: Pos + 1 + num]
        
        while Pos < len(self.SourceCode):
            match self.SourceCode[Pos]:
                case ' ' | '\t':
                    Pos+=1; Coloum+=1
                case '\n':
                    Line+=1
                    Coloum = 1
                    Pos+=1

                case '+':
                    if Peek() == "+":
                        Add(Token(TokenKind.Inc, "++", Coloum, Coloum + 1, Line)) 
                        Coloum+=2; Pos+=2
                    elif Peek() == "=":
                        Add(Token(TokenKind.Add_Assingnment, '+=', Coloum, Coloum + 1, Line))
                        Coloum+=2; Pos+=2
                    else:
                        Add(Token(TokenKind.Add, "+", Coloum, Coloum, Line))
                        Coloum+=1; Pos+=1
                case '-':
                    if Peek() == '-':
                        Add(Token(TokenKind.Dec, '--', Coloum, Coloum + 1, Line))
                        Coloum+=2; Pos+=2;
                    elif Peek() == '=':
                        Add(Token(TokenKind.Sub_Assingnment, '-=', Coloum, Coloum + 1, Line))
                        Coloum+=2; Pos+=2
                    elif Peek() == ">":
                        Add(Token(TokenKind.SArrow, "->", Coloum, Coloum + 1, Line))
                        Coloum+=2; Pos+=2
                    else:
                        Add(Token(TokenKind.Sub, "-", Coloum, Coloum, Line))
                        Coloum+=1; Pos+=1
                case "*":
                    if Peek() == '*':
                        if Peek(2) == '=':
                            Add(Token(TokenKind.Exponent_Assignment, "**=", Coloum, Coloum + 2, Line))
                            Coloum+=3; Pos+=3
                        else:
                            (Peek(2))
                            Add(Token(TokenKind.Exponent, "**", Coloum, Coloum + 1, Line))
                            Coloum+=2; Pos+=2
                    elif Peek() == '=':
                        Add(Token(TokenKind.Mul_Assingnment, "*=", Coloum, Coloum + 1, Line))
                        Coloum+=2; Pos+=2
                    else:
                        Add(Token(TokenKind.Mul, "*", Coloum, Coloum, Line))
                        Coloum+=1; Pos+=1 
                case '/':
                    if Peek() == '/':
                        Pos+=2
                        Coloum+=2

                        while self.SourceCode[Pos] != '\n':
                            Pos+=1
                            Coloum+=1
                        
                        (self.SourceCode[Pos])
                        Pos-=1
                        Coloum-=1
                        (self.SourceCode[Pos])
                    elif Peek() == "*":
                        Pos+=2
                        Coloum+=2
                        
                        while self.SourceCode[Pos] != '*' and Peek(2) != '/':
                            if self.SourceCode[Pos] == '\n':
                                Line+=1
                                Coloum = 0
                            Pos+=1 
                            Coloum+=1

                        if self.SourceCode[Pos] == '\n':
                            Line+=1
                            Coloum = 1
                        Pos+=3
                        Coloum+=3

                        (self.SourceCode[Pos])
                    elif Peek() == "=":
                        Add(Token(TokenKind.Div_Assignment, "/=", Coloum, Coloum + 1, Line))
                        Pos+=2 
                        Coloum+=2
                    else:
                        Add(Token(TokenKind.Div, '/', Coloum, Coloum, Line))
                        Pos+=1
                        Coloum+=1
                case '%':
                    if Peek() == "=":
                        Add(Token(TokenKind.Mod_Assignment, '%=', Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    else:
                        Add(Token(TokenKind.Mod, '%', Coloum, Coloum, Line))
                        Pos+=1; Coloum+=1
                case '=':
                    if Peek() == "=":
                        Add(Token(TokenKind.Equality, "==", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    elif Peek() == ">":
                        Add(Token(TokenKind.DArrow, "=>", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    else:
                        Add(Token(TokenKind.Equal, "=", Coloum, Coloum, Line))
                        Pos+=1; Coloum+=1
                case '!':
                    if Peek() == '=':
                        Add(Token(TokenKind.Not_eq, "!=", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    else:
                        Add(Token(TokenKind.Log_Not, '!', Coloum, Coloum, Line))
                        Pos+=1; Coloum+=1
                case '<':
                    if Peek() == "<":
                        if Peek(2) == "=":
                            Add(Token(TokenKind.LShift_Assignmet, "<<=", Coloum, Coloum + 1, Line))
                            Pos+=3; Coloum+=3
                        
                        else:
                            Add(Token(TokenKind.LShift, "<<", Coloum, Coloum + 1, Line))
                            Pos+=2; Coloum+=2
                    elif Peek() == "=":
                        Add(Token(TokenKind.Less_Than_oeqt, "<=", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    else: 
                        Add(Token(TokenKind.Less_Than, "<", Coloum, Coloum, Line))
                        Pos+=1; Coloum+=1
                case '>':
                    if Peek() == ">":
                        if Peek(2) == "=":
                            Add(Token(TokenKind.RShift_Assignment   , ">>=", Coloum, Coloum + 2, Line))
                            Pos+=3; Coloum+=3
                        
                        else:
                            Add(Token(TokenKind.RShift, ">>", Coloum, Coloum + 1, Line))
                            Pos+=2; Coloum+=2
                    elif Peek() == "=":
                        Add(Token(TokenKind.Greater_Than_oeqt, ">=", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    else: 
                        Add(Token(TokenKind.Greater_Than, ">", Coloum, Coloum, Line))
                        Pos+=1; Coloum+=1
                case '&':
                    if Peek() == "=":
                        Add(Token(TokenKind.Bit_And_Assingment, "&=", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    elif Peek() == "&":
                        Add(Token(TokenKind.Log_And, "&&", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    else:
                        Add(Token(TokenKind.Bit_And, "&", Coloum, Coloum, Line))
                        Pos+=1; Coloum+=1
                case '|':
                    if Peek() == "|":
                        Add(Token(TokenKind.Log_Or, "||", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    elif Peek() == "=":
                        Add(Token(TokenKind.Bit_Or_Assigment, "|=", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    else:
                        Add(Token(TokenKind.Bit_Or, "|", Coloum, Coloum, Line))
                        Pos+=1; Coloum+=1
                case '^':
                    if Peek() == "=":
                        Add(Token(TokenKind.Bit_Xor_Assignment, "^=", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    else:
                        Add(Token(TokenKind.Bit_Xor, "^", Coloum, Coloum, Line))
                        Pos+=1; Coloum+=1
                case '~':
                    Add(Token(TokenKind.Bit_Not, "~", Coloum, Coloum, Line))
                    Pos+=1; Coloum+=1
                case ".":
                    Add(Token(TokenKind.Dot, ".", Coloum, Coloum, Line))
                    Pos+=1; Coloum+=1
                case ":":
                    if Peek() == ":":
                        Add(Token(TokenKind.DColon, "::", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    elif Peek() == "=":
                        Add(Token(TokenKind.Walrus, ":=", Coloum, Coloum + 1, Line))
                        Pos+=2; Coloum+=2
                    else:
                        Add(Token(TokenKind.Colon, ":", Coloum, Coloum, Line))
                        Pos+=1; Coloum+=1
                case ",":
                    Add(Token(TokenKind.Comma, ",", Coloum, Coloum, Line))
                    Pos+=1; Coloum+=1
                case "(":
                    Add(Token(TokenKind.Open_Brack, "(", Coloum, Coloum, Line))
                    Pos+=1; Coloum+=1 
                case ")":
                    Add(Token(TokenKind.Close_Brack, ")", Coloum, Coloum, Line))
                    Pos+=1; Coloum+=1 
                case "{":
                    Add(Token(TokenKind.Curly_Open_Brack, "{", Coloum, Coloum, Line))
                    Pos+=1; Coloum+=1
                case "}":
                    Add(Token(TokenKind.Curly_Close_Brack, "}", Coloum, Coloum, Line))
                    Pos+=1; Coloum+=1  
                case "[":
                    Add(Token(TokenKind.Square_Open_Brack, "[", Coloum, Coloum, Line))
                    Pos+=1; Coloum+=1
                case "]":
                    Add(Token(TokenKind.Square_Close_Brack, "]", Coloum, Coloum, Line))
                    Pos+=1; Coloum+=1
                case "#":
                    Predefines: dict[str, TokenKind] = {
                        "#define" : TokenKind.Pre_Define,
                        "#if" : TokenKind.Pre_If,
                        "#elif" : TokenKind.Pre_Elif,
                        "#else" : TokenKind.Pre_Else,
                        "#end" : TokenKind.Pre_End
                    }

                    PreDef: str = "#" 
                    Start: int = Coloum
                    Pos+=1; Coloum+=1
                    while self.SourceCode[Pos].isalpha():
                            PreDef+=self.SourceCode[Pos]

                            Pos+=1; Coloum+=1
                    
                    
                    if Predefines.get(PreDef) != None:
                        Add(Token(Predefines[PreDef], PreDef, Start, Coloum - 1, Line))
                    else:
                        perr("Not A PreProcess")                   
                case _:
                    if self.SourceCode[Pos].isdigit():
                        NUMBERLIST = '0123456789abcdefABCDEF_.Xx'
                        NUMBERHEXLIST = "abcdefxABCDEFX"
                        Number: str = ""
                        DotCount: int = 0
                        Start: int = Coloum
                        Dots = []

                        while self.SourceCode[Pos] in NUMBERLIST:
                            if self.SourceCode[Pos] != '_':
                                if self.SourceCode[Pos] == '.':
                                    DotCount+=1
                                    Dots.append(Coloum)

                                Number+=self.SourceCode[Pos]
                            Pos+=1; Coloum+=1

                        if DotCount >= 1:
                            if DotCount > 1:
                                perr("To Much Dots")
                                self.Err+=1

                            else:
                                try:
                                    float(Number)
                                except ValueError:
                                    perr("Float can be hexi decimal")
                                    self.Err+=1
                                
                            Add(Token(TokenKind.Float, Number, Start, Coloum - 1, Line))
                        else: 
                            if Number.lower().startswith('0x'):
                                Number = str(int(Number, 16))

                            ishex = False
                            for i in Number:
                                if i in NUMBERHEXLIST:
                                    ishex = True

                            if ishex == True:
                                perr("Not Valid Hex")
                                self.Err+=1             
                            Add(Token(TokenKind.Int, Number, Start, Coloum - 1, Line))
                    elif self.SourceCode[Pos].isalpha() or self.SourceCode[Pos] == '_':
                        Start: int = Coloum
                        Alpha: str = ""
                        while self.SourceCode[Pos].isalnum() or self.SourceCode[Pos] == '_':
                            Alpha+=self.SourceCode[Pos]

                            Pos+=1; Coloum+=1
                        
                        if self.Alphas.get(Alpha) != None:
                            Add(Token(self.Alphas[Alpha], Alpha, Start, Coloum - 1, Line))            
                        else:
                            Add(Token(TokenKind.Identifier, Alpha, Start, Coloum - 1, Line))
                    elif self.SourceCode[Pos] == '"':
                        Start: int = Coloum
                        String: str = "\""
                        Got_Unterminated: bool = False
                        Pos+=1; Coloum+=1
                        while True:
                            if String[-1] != '\\' and self.SourceCode[Pos] == '"':
                                break
                            if self.SourceCode[Pos] == '\n':
                                perr("Mising String Term")
                                Got_Unterminated = True
                                self.Err+=1
                                break
                                 
                            String+=self.SourceCode[Pos]
                            Pos+=1; Coloum+=1
                        
                        if Got_Unterminated == False:
                            Pos+=1; Coloum+=1
                        
                        Add(Token(TokenKind.String, String + '"', Start, Coloum - 1, Line))
                    elif self.SourceCode[Pos] == "'":
                        Start: int = Coloum
                        Character: str = "'"
                        Got_Unterminated: bool = False
                        Pos+=1; Coloum+=1
                        while True:
                            if Character[-1] != '\\' and self.SourceCode[Pos] == "'":
                                break
                            elif self.SourceCode[Pos] == '\n':
                                perr("Misiing Termiate Character")
                                Got_Unterminated = True
                                self.Err+=1
                                break

                            Character+=self.SourceCode[Pos]
                            Pos+=1; Coloum+=1
                        
                        if Got_Unterminated == False:
                            Pos+=1; Coloum+=1

                        if Got_Unterminated == False:
                            if len(Character) > 2:
                                if len(Character) != 1 and Character[1] != "\\":
                                    perr("Multi Chracter character")
                                    self.Err+=1

                        Add(Token(TokenKind.Char, Character + "'", Start, Coloum - 1, Line))
                    else:
                        perr("idk what ts is ")
                        self.Err+=1             
                        Pos+=1; Coloum+=1                                    

        if self.Err > 0:
            exit(1)

        if len(Tokens) != 0:
            Add(Token(TokenKind.EOF, "end of file", Tokens[-1].Start + 1, Tokens[-1].Start + 1, Tokens[-1].Line))
        return Tokens
