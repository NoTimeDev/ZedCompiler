from src.Utils.Utils import *

class Error:
    def __init__(self, SourceLines: list[str], FileName: str, Import: str = ""):
        self.SourceLines: list[str] = SourceLines
        self.FileName: str = FileName
        self.Import: str = Import
        
        self.ErrList: list[str] = []
        
        self.Errs: int = 0
    
    def Exit(self):
        if self.Errs > 0:
            perr(f"{BrightWhite}Total Errors: {BrightRed}{self.Errs}{Reset}")
            for i in self.ErrList:
                perr(i)
            
            exit(0)

    def ThrowErr(self, Line: int, Start: int, End: int, msg: str, Colour: str = BrightRed, Missing: str = "", MisColour = BrightRed):
        if Missing == "":
            self.ErrList.append(f"({Line} :: {Start}-{End}) {BrightRed}[Error] {BrightBlue}[{self.FileName}]{Reset}")
            self.ErrList.append(f"╰─▶{msg}")
            
            
            LineWithHighLight: str = ""
            Pos: int  = 0
            while Pos < len(self.SourceLines[Line - 1]):
                if Pos == Start - 1:
                    LineWithHighLight+=Colour
                    LineWithHighLight+=self.SourceLines[Line - 1][Pos]
                    Pos+=1

                    while Pos < End - 1:
                        LineWithHighLight+=self.SourceLines[Line - 1][Pos]
                        Pos+=1
                    LineWithHighLight+=Reset
                else:
                    LineWithHighLight+=self.SourceLines[Line - 1][Pos]
                    Pos+=1

            self.ErrList.append(f"   ╰─▶ {Line} ||{LineWithHighLight}\n")
            self.Errs+=1 
        elif Missing != "":
            self.ErrList.append(f"({Line} :: {Start}-{End}) {BrightRed}[Error] {BrightBlue}[{self.FileName}]{Reset}")
            self.ErrList.append(f"╰─▶{msg}")

            LineWithHighLight: str = ""
            Pos: int  = 0
            while Pos < len(self.SourceLines[Line - 1]):
                if Pos == Start - 1:
                    LineWithHighLight+=Colour
                    LineWithHighLight+=self.SourceLines[Line - 1][Pos]
                    Pos+=1

                    while Pos < End - 1:
                        LineWithHighLight+=self.SourceLines[Line - 1][Pos]
                        Pos+=1
                    LineWithHighLight+=Reset
                else:
                    LineWithHighLight+=self.SourceLines[Line - 1][Pos]
                    Pos+=1

            self.ErrList.append(f"   ╰─▶ {Line} ||{LineWithHighLight}")
            self.ErrList.append(f"       {len(str(Line)) * " "}   {(End - 1) * " "}{MisColour}{Missing}{Reset}\n")
            self.Errs+=1 

    def ThrowErrorInNewLine(self, Line: int, Start: int, End: int, msg: str, Colour: str = BrightRed, Missing: str = "", MisColour = BrightRed):
            self.ErrList.append(f"({Line} :: {Start}-{End}) {BrightRed}[Error] {BrightBlue}[{self.FileName}]{Reset}")
            self.ErrList.append(f"╰─▶{msg}")


            self.ErrList.append(f"       {(len(str(Line + 1)) - len(str(Line))) * " "}{Line} ||{self.SourceLines[Line - 1]}")
            self.ErrList.append(f"       {(len(str(Line + 1)) - len(str(Line))) * " "}{len(str(Line)) * " "} ||{(End) * " "}{MisColour}{Missing}{Reset}")
            
            LineWithHighLight: str = ""
            Pos: int  = 0
            while Pos < len(self.SourceLines[Line]):
                if Pos == 1 - 1:
                    LineWithHighLight+=MisColour
                    LineWithHighLight+=self.SourceLines[Line][Pos]
                    Pos+=1

                    while Pos < 1 - 1:
                        LineWithHighLight+=self.SourceLines[Line][Pos]
                        Pos+=1
                    LineWithHighLight+=Reset
                else:
                    LineWithHighLight+=self.SourceLines[Line][Pos]
                    Pos+=1

            self.ErrList.append(f"       {Line + 1} ||{LineWithHighLight}")
            self.ErrList.append(f"       {len(str(Line + 1)) * " "}   {(1 - 1) * " "}{MisColour}~{Reset}\n")
            
            self.Errs+=1



