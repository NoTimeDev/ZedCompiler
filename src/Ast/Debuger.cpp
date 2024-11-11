#ifndef DEBUGER_CPP
#define DEBUGER_CPP

#include "Expr.hpp"
#include "Stmt.hpp"
#include <iostream>
#include <string>

void Ast::BlockStmt::debug(int& depth, bool F){
    if(F == false){
        std::cout << std::string(depth*2, ' ') <<  "{\n";
    }else{
        std::cout << "{\n";
    }

    depth++;

    std::cout << std::string(depth*2, ' ') <<  "\"Kind\" : \"BlockStmt\"\n";
    std::cout << std::string(depth*2, ' ') <<  "\"Body\" : [\n";
    
    depth++;

    for(auto& i : Body){
        i->debug(depth);
    }

    depth--;
    std::cout << std::string(depth*2, ' ') <<  "]\n";
    depth--;
    
    std::cout << std::string(depth*2, ' ') <<  "}\n";
};


void Ast::ExprStmt::debug(int& depth, bool F){
    Expression->debug(depth);
};

void Ast::IntLit::debug(int& depth, bool F){
    if(F == false){
        std::cout << std::string(depth*2, ' ') <<  "{\n";
    }else{
        std::cout << "{\n";
    }

    depth++;

    std::cout << std::string(depth*2, ' ') <<  "\"Kind\" : \"Integer Literal\"\n";
    std::cout << std::string(depth*2, ' ') <<  "\"Value\" : " << Value << "\n";
 
    depth--;
    
    std::cout << std::string(depth*2, ' ') <<  "}\n";
};


void Ast::BinExpr::debug(int& depth, bool F){
    if(F == false){
        std::cout << std::string(depth*2, ' ') <<  "{\n";
    }else{
        std::cout << "{\n";
    }


    depth++;

    std::cout << std::string(depth*2, ' ') <<  "\"Kind\" : \"Binary Expression\"\n";
    std::cout << std::string(depth*2, ' ') <<  "\"Left\" : ";
    depth++;
    Left->debug(depth, true);
    depth--;
    
    std::cout << std::string(depth*2, ' ') <<  "\"Right\" : ";
    depth++;
    Right->debug(depth, true);
    depth--;

    std::cout << std::string(depth*2, ' ') <<  "\"Operator\" : ";
    switch(Op){
        case TokenKind::plus:
            std::cout << "\"+\"\n";
            break;
        case TokenKind::star:
            std::cout << "\"*\"\n";
            break;
    }



    depth--;
    
    std::cout << std::string(depth*2, ' ') <<  "}\n";
}

#endif