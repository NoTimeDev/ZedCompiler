from time import time, sleep
Start = time()


import sys
from src.Utils.Utils import *


#Compile Shit
from src.Lexer.Lexer import  *
from src.Parser.Parser import *
from src.Environment.Environment import * 

def main(argv=sys.argv, argc=len(sys.argv)) -> None:
    if(argc == 1):
        print(f"{Colour['BrightRed']}fatal error: {Colour['BrightWhite']}no input files{Colour['Reset']}", file=sys.stderr)
        exit(1)
    if(argc == 2 and argv[1] in ["-v", "--version"]):
        print("Zedc Version 0.0.1")
        exit(0)
    if(argc == 2 and argv[1] in ["-h", "--help"]):
        print("Options")
        exit(0)

    #Compile
    try:
        with open(argv[1], "r") as File:
            SourceCode : str = File.read()
    except FileNotFoundError:
        print(f"{Colour['BrightRed']}fatal error: {Colour['BrightWhite']}'{argv[1]}' does not exist{Colour['Reset']}", file=sys.stderr)
        exit(1)

    Notes = []
    if("--no--notes" in argv):
        Notes += ["--Nonote-VarDec"]

    LexerClass : Lexer = Lexer(SourceCode + "\n", argv[1], Notes)
    LexedTokens : list = LexerClass.Lex()

    ParserClass : Parser = Parser(LexedTokens, argv[1], SourceCode.split('\n'), Notes)
    Ast : dict = ParserClass.Parse()

    # CodeGenClass : CodeGen = CodeGen(Ast)
    # CodeGenClass.Gen()
    # CodeGenClass.Module.MakeFile("Exe")


    if("--debug--compiler--lexer" in argv):
        for i in LexedTokens:
            print(i)
    if("--debug--compiler--parser" in argv):
        from json import dumps
        print(dumps(Ast, indent=2))

    


if __name__ == '__main__':
    main()
    End = time()


    if(End - Start < 60):
        print(int(End - Start), "seconds")
    else:
        print(int(End - Start // 60), "minutes", int((End - Start / 60) * 60 - End - Start), "seconds")
    exit(0)
