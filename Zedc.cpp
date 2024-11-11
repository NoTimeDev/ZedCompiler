#include <iostream>
#include <fstream>
#include "src/Lexer/Lexer.hpp"
#include "src/Utils/Utils.hpp"
#include "src/Parser/Parser.hpp"
#include "src/CodeGen/CodeGen.hpp"
#include <ostream>
#include <chrono>

std::ostream& operator<<(std::ostream& os, Token& tk){
    os << "{\"Value\" : \"" << tk.Value << "\", \"Kind\" : " << static_cast<int>(tk.Kind) << ", \"Line\" : " << tk.Line << ", \"Start\" : " << tk.Start << ", \"End\" : " << tk.End << "}";
    return os;
}

void printtime(std::chrono::milliseconds duration){
    auto mins = std::chrono::duration_cast<std::chrono::minutes>(duration);
    duration -= mins;

    auto secs = std::chrono::duration_cast<std::chrono::seconds>(duration);
    duration -= secs;

    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(duration);
    duration -= ms;

    if(mins.count() > 0){
        std::cout << mins.count() << " minute(s) "
                  << secs.count() << " second(s) "
                  << ms.count() << " millisecond(s)";
    }else if(secs.count() > 0){
        std::cout << secs.count() << " second(s) "
                  << ms.count() << " millisecond(s)";        
    }else{
        std::cout << ms.count() << " millisecond(s)";
    }

}

int main(int argc, char* argv[]){
    auto Start = std::chrono::high_resolution_clock::now();
    
    std::ifstream File(argv[1]);
    if(!File.is_open()){
        std::cout << BrightRed << "Error: " << BrightWhite << "No Such File '" << argv[1] << "'" << Reset;
        exit(1);
    }

    std::string Contents;
    {
        std::string Line;
        while(std::getline(File, Line)){
            Contents+=Line + "\n";
        }
    }
    File.close();
    Lexer LexerClass(Contents, argv[1]);
    
    auto LexedTokens = LexerClass.Lex();  

    // for(auto& i : LexedTokens){
    //     std::cout << i << "\n";
    // }


    Parser ParserClass(LexedTokens);
    auto Ast = ParserClass.Parse();


    CodeGen CodeGenClass(Ast);
    CodeGenClass.Gen();
    
    int x = 0;
    Ast.debug(x);

    auto End = std::chrono::high_resolution_clock::now();

    printtime(std::chrono::duration_cast<std::chrono::milliseconds>(End - Start));
}