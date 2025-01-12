from datetime import datetime
StartTime = datetime.now()

import sys

#---Local Imports---
from src.Utils.Utils import *
from src.Lexer.Lexer import * 
#------------------- 


def main(argv=sys.argv, argc=len(sys.argv)):
    if argc == 1:
        perr(f"{BrightWhite}zedc: {BrightRed}fatal error: {Reset} no input files")
        exit(1)
    
    Flags: dict[str, bool] = {
        "--break-lex":False,
        "--break-parse":False,
        "--debug-tokens": False,

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

    #--lexer--
    LexerClass: Lexer = Lexer(argv[1], SourceCode)
    LexedTokens: list[Token] = LexerClass.Lex()
    if Flags["--debug-tokens"] == True:
        print(len(LexedTokens))
        for i in LexedTokens:
            print(i)
    if len(LexedTokens) == 0:
        perr(f"{BrightWhite}zedc:{Reset} No tokens generated")
        exit(0)
    #-------------------------------
    

if __name__ == '__main__':
    main()
    EndTime = datetime.now()
    TotalTime = EndTime - StartTime

    print(f"Mins:{TotalTime.seconds // 60}, Secs:{TotalTime.seconds}, Ms:{TotalTime.microseconds // 1000}")
