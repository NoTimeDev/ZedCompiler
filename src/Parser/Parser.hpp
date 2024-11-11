#ifndef PARSER_HPP
#define PARSER_HPP

#include "../Lexer/TokenTypes.hpp"
#include "../Ast/Stmt.hpp"
#include "../Ast/Expr.hpp"


class Parser{
    public:
        u64 Pos = 0;
        std::vector<Token>& Tokens;
        Token CurrentTk();
        Token Advance();
        bool HasTokens();
        TokenKind CurrentTkKind();
        Parser(std::vector<Token>& Tokens_);
        Ast::BlockStmt Parse();       
};

#endif