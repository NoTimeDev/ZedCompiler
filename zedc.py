from datetime import datetime
StartTime = datetime.now()

import sys
import json 

#---Local Imports---
from src.Utils.Utils import *
from src.Lexer.Lexer import * 
from src.Error.Error import *
from src.Parser.Parser import *
from src.TypeChecker.TypeChecker import *
#------------------- 

class AstEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Expr):
            return o.__ToJson__()
        elif isinstance(o, Stmt):
            return o.__ToJson__()
        elif isinstance(o, Type):
            return o.__ToJson__()
        elif isinstance(o, Program):
            return o.__ToJson__()
        else:
            return o 


def main(argv=sys.argv, argc=len(sys.argv)):
    if argc == 1:
        perr(f"{BrightWhite}zedc: {BrightRed}fatal error: {Reset} no input files")
        exit(1)
    
    Flags: dict[str, bool] = {
        "-dbgast": False,
        "-dbgtks" : False,
        "dbgtc" : False,

        "-tks-break" : False,
        "-ast-break" : False,
        "-tc-break" : False, 

        "--emit-ir":False,
        "--emit-obj":False,
        "--emit-shared":False,
        "--emit-Lib":False,
        "--emit-asm":False
    }

    ExecutableName: str = argv[1][:argv[1].find(".")]

    Wrong: list[str] = []

    for i in argv[2:]:
        if i in list(Flags.keys()):
            Flags[i] = True 
        else:
            Wrong.append(i)

    if len(Wrong) != 0:
        if len(Wrong) == 1:
            perr(f"{BrightWhite}zedc: {BrightRed}error:{Reset} unrecognized flag {Wrong[0]}")
        else:
            perr(f"{BrightWhite}zedc: {BrightRed}error:{Reset} unrecognized flags {', '.join(Wrong)}")
        exit(1)
    

    #-------------------------------
    #Get SourceCode
    try:
        with open(argv[1], "r") as File:
            SourceCode = File.read()
    except FileNotFoundError:
        perr(f"{BrightWhite}zedc: {BrightRed}error:{Reset} cannot find file '{argv[1]}'")
        exit(1)
    
    SourceCode+="\n"
    #--ErrHandle--
    ErrorClass: Error = Error(SourceCode.split("\n"), argv[1])
    #--lexer--
    LexerClass: Lexer = Lexer(ErrorClass, SourceCode)
    LexedTokens: list[Token] = LexerClass.Lex()

    if Flags["-dbgtks"] == True:
        for i in LexedTokens:
            print(i)
    
    if Flags["-tks-break"] == True:
        exit(0)

    if len(LexedTokens) == 0:
        perr(f"{BrightWhite}zedc:{Reset} No tokens generated")
        exit(1)
 
    #--Parser--
    ParserClass: Parser = Parser(ErrorClass, LexedTokens)
    Ast: Program = ParserClass.Parse()

    if Flags["-dbgast"] == True:
        print(json.dumps(Ast, indent=4, cls=AstEncoder))
    
    if Flags["-ast-break"] == True:
        exit(0)

    #---TypeChecker---
    TypeCheckerClass: TypeChecker = TypeChecker(Ast, ErrorClass, argv[1])
    Ast = TypeCheckerClass.Check()
    
    if Flags["-tc-break"] == True:
        sys.exit(0)
    #-------------------------------
    

if __name__ == '__main__':
    main()
    EndTime = datetime.now()
    TotalTime = EndTime - StartTime

    print(f"Mins:{TotalTime.seconds // 60}, Secs:{TotalTime.seconds}, Ms:{TotalTime.microseconds // 1000}")
