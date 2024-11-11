#include "Parse_Funcs.cpp"
#include "Parser.hpp"


Parser::Parser(std::vector<Token>& Tokens_) : Tokens(Tokens_) {
    CreateTokenLookUps();
};

Ast::BlockStmt Parser::Parse(){
    std::vector<std::shared_ptr<Ast::Stmt>> Body;

    while(this->HasTokens()){
        Body.push_back(Parse_Stmt(*this));
    }

    return Ast::BlockStmt(Body);
}


Token Parser::CurrentTk(){
    return this->Tokens[this->Pos];
}

Token Parser::Advance(){
    auto tk = this->CurrentTk();
    this->Pos++;
    return tk;
}

TokenKind Parser::CurrentTkKind(){
    return this->CurrentTk().Kind;
}

bool Parser::HasTokens(){
    return this->Pos < this->Tokens.size() && this->CurrentTkKind() != TokenKind::eof; 
}