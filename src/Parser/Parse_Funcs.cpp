#pragma once

#include "../Lexer/TokenTypes.hpp"
#include "../Ast/Stmt.hpp"
#include "../Ast/Expr.hpp"
#include "Parser.hpp"


#include <unordered_map>



enum class BindingPower{
    default_bp = 0,
    comma,
    assignment,
    logical,
    relational,
    additive,
    multiplicitive,
    power,
    unary,
    call,
    memeber,
    primary
};
typedef std::shared_ptr<Ast::Stmt> (*stmt_handler)(Parser&);
typedef std::shared_ptr<Ast::Expr> (*nud_handler)(Parser&);
typedef std::shared_ptr<Ast::Expr> (*led_handler)(Parser&, std::shared_ptr<Ast::Expr>, BindingPower);


std::unordered_map<TokenKind, stmt_handler> stmt_lu;
std::unordered_map<TokenKind, nud_handler> nud_lu;
std::unordered_map<TokenKind, led_handler> led_lu;
std::unordered_map<TokenKind, BindingPower> bp_lu;

void led(TokenKind Kind, BindingPower bp, led_handler led_fn){
    bp_lu[Kind] = bp;
    led_lu[Kind] = led_fn;
}

void nud(TokenKind Kind, BindingPower bp, nud_handler nud_fn){
    bp_lu[Kind] = bp;
    nud_lu[Kind] = nud_fn;
}

void stmt(TokenKind Kind, stmt_handler stmt_fn){
    bp_lu[Kind] = BindingPower::default_bp;
    stmt_lu[Kind] = stmt_fn;
}




std::shared_ptr<Ast::Expr> Parse_Expr(Parser& p, BindingPower bp){
    auto TokenKind = p.CurrentTkKind();
    auto Nud_Fn = nud_lu.find(TokenKind);

    if(Nud_Fn == nud_lu.end()){
        //Some Error
    }

    auto Left = Nud_Fn->second(p);

    while(static_cast<int>(bp_lu[p.CurrentTkKind()]) > static_cast<int>(bp)){
        TokenKind = p.CurrentTkKind();
        auto Led_Fn = led_lu.find(TokenKind);

        
        Left = Led_Fn->second(p, Left, bp_lu[p.CurrentTkKind()]);
    }

    return Left;
}

std::shared_ptr<Ast::Expr> Parse_Primary_Expr(Parser& p){
    switch(p.CurrentTkKind()){
        case TokenKind::int_lit:
            return std::make_shared<Ast::IntLit>(p.Advance().Value);
    }
    return std::make_shared<Ast::IntLit>("0");
}

std::shared_ptr<Ast::Expr> Parse_BinExpr(Parser& p, std::shared_ptr<Ast::Expr> left, BindingPower bp){
    auto Op = p.Advance();
    auto right = Parse_Expr(p, bp);

    return std::make_shared<Ast::BinExpr>(left, right, Op.Kind); 
}



std::shared_ptr<Ast::Stmt> Parse_Stmt(Parser& p){
    auto Stmt_Fn = stmt_lu.find(p.CurrentTkKind());

    if(Stmt_Fn != stmt_lu.end()){
        return Stmt_Fn->second(p);
    };

    auto Expression = Parse_Expr(p, BindingPower::default_bp);
    p.Advance();
    
    return std::make_shared<Ast::ExprStmt>(Expression);
}

void CreateTokenLookUps(){
    led(TokenKind::plus, BindingPower::additive, &Parse_BinExpr);    
    led(TokenKind::star, BindingPower::multiplicitive, &Parse_BinExpr);    
    
    nud(TokenKind::int_lit, BindingPower::primary, &Parse_Primary_Expr);
}