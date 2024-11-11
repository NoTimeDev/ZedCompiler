#ifndef TOKENTYPES_HPP
#define TOKENTYPES_HPP

#include <string>
#include "../Utils/Utils.hpp"

enum class TokenKind{
    plus,   
    star,

    inc,
    dec,

    int_lit,
    f_lit,


    semicolon,
    eof,
};


struct Token{
    std::string Value;
    TokenKind Kind;

    u64 Line;
    u64 Start;
    u64 End;

    Token(const std::string value_, TokenKind Kin_, u64 Line_, u64 Start_, u64 End_){
        Value = value_;
        Kind = Kin_;
        Line = Line_;
        Start = Start_;
        End = End_;
    };
};



#endif