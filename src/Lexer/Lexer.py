from src.Lexer.TokenTypes import *
from src.Utils.Utils import * 


def AddIf(Line : str, Pos: int, Replace : str):
    if(len(Line) < Pos):
        Line += ((Pos  + 1) * " ")
    
    Line = Line[:Pos] + Replace + Line[Pos + len(Replace):]
    return Line
    
KeyWords: dict[str, TokenType] = {
    "let" : TokenType.Let,
    "mut" : TokenType.Mut
}

Types: list[str] = [
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

class Lexer:
    def __init__(self, SourceCode: str, FileName: str, Notes: list[str]):
        self.SourceCode : str = SourceCode
        self.FileName : str = FileName
        self.Tokens : list = [{"Type":TokenType.NULL}]
        self.Pos : int = 0
        self.Line : int = 1
        self.SourceLines : list[str] = SourceCode.split('\n')
        self.Errors : int = 0
        self.Notes: list[str] = Notes

    def Lex(self) -> list:
        def Push_Back(Line : int, Start : int , End : int , Type : TokenType, Value : str):
            self.Tokens.append({"Line":Line, "Start":Start, "End":End, "Type":Type, "Value":Value})

        def Peek(PeekTo: int = 1) -> str:
            try:
                self.SourceCode[self.Pos + PeekTo]
            except IndexError:
                return " "
            else:
                return self.SourceCode[self.Pos + PeekTo]
        
        Coloum : int = 1

        while(self.Pos < len(self.SourceCode)):
            match(self.SourceCode[self.Pos]):
                case " ":
                    Coloum+=1
                    self.Pos+=1
                case "\n":
                    Coloum = 1
                    self.Pos+=1
                    self.Line+=1
                case "+":
                    Push_Back(self.Line, Coloum, Coloum, TokenType.Plus, "+")
                    Coloum+=1
                    self.Pos+=1
                case "-":
                    if(Peek().isdigit() and self.Tokens[-1].get("Type") not in [TokenType.Int_Literal, TokenType.Str_Literal, TokenType.Identifier, TokenType.Float_Literal]):
                        print("ll")
                        Coloum+=1; self.Pos+=1

                        Number : str = "-"
                        Start : int = Coloum

                        while(self.SourceCode[self.Pos].isdigit() or self.SourceCode[self.Pos] == '_'):
                            if(self.SourceCode[self.Pos] != '_'):
                                Number+=self.SourceCode[self.Pos]
                            self.Pos+=1
                            Coloum+=1
                        Push_Back(self.Line, Start, Coloum - 1, TokenType.Int_Literal, Number)

                    else:
                        Push_Back(self.Line, Coloum, Coloum, TokenType.Minus, "-")
                        Coloum+=1
                        self.Pos+=1
                case "/":
                    Push_Back(self.Line, Coloum, Coloum, TokenType.Forward_Slash, "/")
                    Coloum+=1
                    self.Pos+=1
                case "*":
                    Push_Back(self.Line, Coloum, Coloum, TokenType.Star, "*")
                    Coloum+=1
                    self.Pos+=1
                case ";":
                    Push_Back(self.Line, Coloum, Coloum, TokenType.Semi, ";")
                    Coloum+=1
                    self.Pos+=1
                case "<":
                    Push_Back(self.Line, Coloum, Coloum, TokenType.Open_Arrow, "<")
                    Coloum+=1
                    self.Pos+=1
                case ">":
                    Push_Back(self.Line, Coloum, Coloum, TokenType.Close_Arrow, ">")
                    Coloum+=1
                    self.Pos+=1
                case "[":
                    Push_Back(self.Line, Coloum, Coloum, TokenType.Open_Square_Paren, "[")
                    Coloum+=1
                    self.Pos+=1
                case "]":
                    Push_Back(self.Line, Coloum, Coloum, TokenType.Close_Square_Paren, "]")
                    Coloum+=1
                    self.Pos+=1
                case ":":
                    if(Peek() == "="):
                        Push_Back(self.Line, Coloum, Coloum, TokenType.Colon_Equals, ":=")
                        Coloum+=2
                        self.Pos+=2
                    else:
                        Push_Back(self.Line, Coloum, Coloum, TokenType.Colon, ":")
                        Coloum+=1
                        self.Pos+=1
                case "=":
                        Push_Back(self.Line, Coloum, Coloum, TokenType.Equal, "=")
                        Coloum+=1
                        self.Pos+=1
                case _:
                    if(self.SourceCode[self.Pos].isdigit()):
                        Number : str = ""
                        Start : int = Coloum

                        while(self.SourceCode[self.Pos].isdigit() or self.SourceCode[self.Pos] == '_'):
                            if(self.SourceCode[self.Pos] != '_'):
                                Number+=self.SourceCode[self.Pos]
                            self.Pos+=1
                            Coloum+=1
                        
                        Push_Back(self.Line, Start, Coloum - 1, TokenType.Int_Literal, Number)
                    elif(self.SourceCode[self.Pos].isalpha() or self.SourceCode[self.Pos] == '_'):
                        Word : str = ""
                        Start : int = Coloum

                        while(self.SourceCode[self.Pos].isalnum() or self.SourceCode[self.Pos] == '_'):
                            Word+=self.SourceCode[self.Pos]
                            self.Pos+=1
                            Coloum+=1 

                        if(KeyWords.get(Word) != None):
                            Push_Back(self.Line, Start, Coloum - 1, KeyWords.get(Word), Word)
                        elif(Word in Types):
                            Push_Back(self.Line, Start, Coloum - 1, TokenType.Type_, Word)
                        else:
                            Push_Back(self.Line, Start, Coloum - 1, TokenType.Identifier, Word)

                    elif(self.SourceCode[self.Pos] == '"'):
                        String : str = "\""
                        Start : int = Coloum

                        self.Pos+=1; Coloum+=1
                        
                        while(self.Pos < len(self.SourceCode)):
                            if(self.SourceCode[self.Pos] == '"'):
                                String+=self.SourceCode[self.Pos]
                                break
                            elif(self.SourceCode[self.Pos] == "\n"):
                                
                                printf(f"{Colour['BrightWhite']}{self.FileName}:{self.Line}:{Coloum}{Colour['BrightRed']} error:{Colour['BrightWhite']} unterminated string (\"){Colour['Reset']}")
                                printf(f"{self.Line}|{self.SourceLines[self.Line - 1]}")
                                printf(f"{len(str(self.Line)) * ' '}|{(Coloum - 1) * ' '}{Colour['BrightRed']}^{Colour['Reset']}")
                                printf(f"{len(str(self.Line)) * ' '}|{(Coloum - 1) * ' '}{Colour['BrightBlue']}\"{Colour['Reset']}")
                                self.Pos+=1
                                Coloum+=1 
                                self.Errors+=1
                                break

                            String+=self.SourceCode[self.Pos]
                            self.Pos+=1; Coloum+=1
                        
                        self.Pos+=1; Coloum+=1


                        Push_Back(self.Line, Start, Coloum - 1, TokenType.Str_Literal, String)
                    else:
                        printf(f"{Colour['BrightWhite']}{self.FileName}:{self.Line}:{Coloum}{Colour['BrightRed']} error:{Colour['BrightWhite']} unknow token found '{self.SourceCode[self.Pos]}'{Colour['Reset']}")
                        printf(f"{self.Line}|{self.SourceLines[self.Line - 1]}")
                        printf(f"{len(str(self.Line)) * ' '}|{(Coloum - 1) * ' '}{Colour['BrightRed']}^{Colour['Reset']}")
                        self.Pos+=1
                        Coloum+=1 
                        self.Errors+=1

        Push_Back(self.Line - 1, self.Tokens[-1].get("Start") + 1, self.Tokens[-1].get("Start") + 1, TokenType.EOF, "EOF")

        if(self.Errors != 0):
            exit(1)

        return self.Tokens[1:]