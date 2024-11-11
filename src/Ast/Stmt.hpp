#ifndef STMT_HPP
#define STMT_HPP

#include "Ast.hpp"
#include <memory>
#include <vector>

namespace Ast{

    struct BlockStmt : public Stmt{
        std::vector<std::shared_ptr<Ast::Stmt>> Body;

        BlockStmt(std::vector<std::shared_ptr<Ast::Stmt>> body){
            Body = body;
            Kind = NodeKind::BlockStmt;
        };        
    
        void debug(int& depth, bool F = false) override;
    };

    struct ExprStmt : public Stmt{
        std::shared_ptr<Expr> Expression;

        ExprStmt(std::shared_ptr<Expr> Expression_){
            Kind = NodeKind::ExprStmt;
            Expression = Expression_;
        };
    
        void debug(int& depth, bool F = false) override;
    };
};

#endif