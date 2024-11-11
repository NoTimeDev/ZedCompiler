#ifndef LEXER_HPP
#define LEXER_HPP

#include "../Utils/Utils.hpp"
#include "TokenTypes.hpp"
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

class Lexer{
    private:
        std::string& SourceCode;
        char* FileName;

    public:
        Lexer(std::string& SourceCode_, char* FileName_);
        std::vector<Token> Lex();
};

#endif