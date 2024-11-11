#ifndef EXPR_HPP
#define EXPR_HPP

#include "Ast.hpp"
#include <memory>
#include <string>
#include "../Lexer/TokenTypes.hpp"

namespace Ast{

    struct IntLit : public Expr{
        std::string Value;

        IntLit(std::string Value_){
            Kind = NodeKind::IntLit;
            Value = Value_;
        };

        void debug(int& depth, bool F = false) override;
    };

    // struct FloatLit : public Expr{
    //     std::string Value;

    //     FloatLit(std::string Value_){
    //         Kind = NodeKind::FloatLit;
    //         Value = Value_;            
    //     };
    //     void debug(int& depth, bool F = false) override;
    // };


    struct BinExpr : public Expr{
        std::shared_ptr<Expr> Left;
        std::shared_ptr<Expr> Right;

        TokenKind Op;

        BinExpr(std::shared_ptr<Expr> Lhs, std::shared_ptr<Expr> Rhs, TokenKind Op_){
            Kind = NodeKind::BinExpr;
            Left = Lhs;
            Right = Rhs;
            Op = Op_;
        };     
        void debug(int& depth, bool F = false) override;
    };
};

#endif