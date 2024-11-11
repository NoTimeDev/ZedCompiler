#include "Lexer.hpp"
/*

THIS LEXER IS PROBABLY NOT OPTIMIZED BUT LIKE
ITS EASY AND ITS IN C++ SO IT SHOULDNT BE TOO SLOW
*/
Lexer::Lexer(std::string& SourceCode_, char* FileName_) : SourceCode(SourceCode_), FileName(FileName_) {};


std::vector<Token> Lexer::Lex(){
    std::vector<Token> Tokens;

    u64 Pos = 0;
    u64 Coloum = 1;
    u64 Line = 1;

    while(Pos < this->SourceCode.size()){
        switch(this->SourceCode[Pos]){
            case ' ':
                Pos++; Coloum++; break;
            case '\n':
                Pos++; Coloum = 1; break;
            case '+':
                Tokens.push_back(Token("+", TokenKind::plus, Line, Coloum, Coloum));
                Pos++; Coloum++; break;
            case '*':
                Tokens.push_back(Token("*", TokenKind::star, Line, Coloum, Coloum));
                Pos++; Coloum++; break;
            case ';':
                Tokens.push_back(Token(";", TokenKind::semicolon, Line, Coloum, Coloum));
                Pos++; Coloum++; break;
            default:
                if(std::isdigit(this->SourceCode[Pos])){
                    auto Start = Coloum;
                    std::string Number = "";
                    u16 DotCount = 0;

                    while(std::isxdigit(this->SourceCode[Pos]) || this->SourceCode[Pos] == '_' || this->SourceCode[Pos] == '.'){
                        if(this->SourceCode[Pos] != '_'){
                            if(this->SourceCode[Pos] == '.'){
                                DotCount++;
                            }
                            Number+=this->SourceCode[Pos];
                        }    
                        Pos++;
                        Coloum++;
                    }
                    if(DotCount > 0){
                        Tokens.push_back(Token(Number, TokenKind::f_lit, Line, Start, Coloum));
                    }else{
                        Tokens.push_back(Token(Number, TokenKind::int_lit, Line, Start, Coloum));
                    }
                    break;
                }else{
                    std::cerr << "Error!\n";
                    Pos++; Coloum++; break;
                }
        }
    }
    
    Tokens.push_back(Token(std::string("eof"), TokenKind::eof, Line, 1, Coloum));
    return Tokens;
}