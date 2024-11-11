#ifndef AST_HPP
#define AST_HPP

enum class NodeKind{
    IntLit,
    FloatLit,

    BinExpr,

    ExprStmt,
    BlockStmt,
};

namespace Ast{
    
    
    struct Stmt{
        NodeKind Kind;
        virtual void debug(int& depth, bool F = false) = 0;
    };


    struct Expr{
        NodeKind Kind;
        virtual void debug(int& depth, bool F = false) = 0;
    };

};

#endif