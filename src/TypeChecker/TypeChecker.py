from re import I, S
from src.Ast.Ast import * 
from src.Ast.Expr import * 
from src.Ast.Stmt import * 
from src.Ast.Types import * 
from src.Ast.NodeKinds import * 
from src.Lexer.TokenKind import * 
from src.Error.Error import * 
from typing import NoDefault, cast
from enum import STRICT, Enum, auto

class ScopeErrors(Enum):
    AlreadyExist = auto()
    DosentExist = auto()

    Func_Exist_For_Var = auto()
    Var_Exist_For_Func = auto()

class ScopeManager:
    def __init__(self, ParentScope = None):
        self.Vars: dict = {}
        self.Funcs: dict = {}
        self.ParentScope = ParentScope

    def MakeVar(self, Name : str, Info):
        if Name in list(self.Vars.keys()):
            return ScopeErrors.AlreadyExist 
        elif Name in list(self.Funcs.keys()):
            return ScopeErrors.Func_Exist_For_Var
        else: 
            self.Vars.update({Name : Info})

    def GetVar(self, Name : str):
        if Name not in list(self.Vars.keys()):
            if self.ParentScope == None: 
                return ScopeErrors.DosentExist 
            else:
                return self.ParentScope.GetVar(Name)
        elif Name in list(self.Vars.keys()):
            return self.Vars.get(Name)
    
    def MakeFunc(self, Name : str, Info):
        if Name in list(self.Funcs.keys()):
            return ScopeErrors.AlreadyExist 
        else: 
            self.Funcs.update({Name : Info})

    def GetFunc(self, Name : str):
        if Name not in list(self.Funcs.keys()):
            if self.ParentScope == None: 
                return ScopeErrors.DosentExist
            else:
                return self.ParentScope.GetFunc(Name)
        elif Name in list(self.Funcs.keys()):
            return self.Funcs.get(Name)


class TypeChecker:
    def __init__(self, Ast: Program, Err: Error, Name: str) -> None:
        self.Ast: Program = Ast 
        self.Err: Error = Err
        self.Name: str = Name


        self.Pos: int  = 0
        
        self.Scope = ScopeManager()
        
        self.Scopes: list[ScopeManager] = []

    def Check(self):
        while self.Pos < len(self.Ast.Body):
            self.TypeCheckStmt(self.Ast.Body[self.Pos])
            self.Pos+=1
        
        self.Err.Exit()
        return self.Ast
    
    def TypeCheckStmt(self, Statement: Stmt):
        if Statement.Kind == NodeKind.ExprStmt:
            Statement = cast(ExprStmt, Statement) #fucking bloat but i have to do this so pyright dosent complian
            self.TypeCheckExpr(Statement.Expression)
        elif Statement.Kind == NodeKind.FuncStmt:
            Statement = cast(FuncStmt, Statement)
            self.TypeCheckFuncDec(Statement)
        elif Statement.Kind == NodeKind.RetStmt:
            Statement = cast(ReturnStmt, Statement)
            self.TypeCheckRetStmt(Statement)
        elif Statement.Kind == NodeKind.VarDec:
            Statement = cast(VarDec, Statement)
            self.TypeCheckVarDec(Statement)
    def TypeCheckExpr(self, Expr: Expr):
        if Expr.Kind == NodeKind.BinExpr:
            self.TypeCheckBinExpr(cast(BinExpr, Expr))  
        elif Expr.Kind == NodeKind.IdentifierExpr:
            self.TypeCheckIdentExpr(cast(IdentifierExpr, Expr))
    
    def TypeCheckVarDec(self, Var: VarDec):
        vr = self.Scope.MakeVar(Var.Name, Var)
        if vr == ScopeErrors.AlreadyExist:
            alrdef = self.Scope.GetVar(Var.Name)
            self.Err.ThrowErr(Var.Loc["Line_Name"], Var.Loc["Start_Name"], Var.Loc["End_Name"], f"{UBrightMagenta}TypeChecker Error:{Reset} {BrightRed}(Variable '{Var.Name}' has already been defined on line {alrdef.Loc['Line_Name']}){Reset}", Missing="", MisColour=BrightGreen)
            
    def TypeCheckFunc(self, Ident: IdentifierExpr):
        pass 

    def TypeCheckVar(self, Ident: IdentifierExpr):
        pass 

    def TypeCheckIdentExpr(self, Ident: IdentifierExpr):
        #strong idents -- structs, func, vars
        if self.Scope.GetFunc(Ident.Name) != ScopeErrors.DosentExist:
            return self.TypeCheckFunc(Ident)
        elif self.Scope.GetVar(Ident.Name) != ScopeErrors.DosentExist:
            return self.TypeCheckVar(Ident)
        else:
            self.Err.ThrowErr(Ident.Loc["Line_Name"], Ident.Loc["Start_Name"], Ident.Loc["End_Name"], f"{UBrightMagenta}TypeChecker Error:{Reset} {BrightRed}('{Ident.Name}' is not defined){Reset}", Missing="", MisColour=BrightGreen)
            return NullType()

    def TypeCheckRetStmt(self, Ret: ReturnStmt):
        self.TypeCheckExpr(Ret.Val)

    def TypeCheckFuncDec(self, Func: FuncStmt):   
        Addscope = self.Scope.MakeFunc(Func.Name,Func)

        if Addscope == ScopeErrors.AlreadyExist:
            alrdef = self.Scope.GetFunc(Func.Name)
            alrdeftypes = []
            functypes = []

            for i in Func.Parameters:
                functypes.append(i.VarType.Kind)

            for i in alrdef.Parameters:
                alrdeftypes.append(i.VarType.Kind)
            
            if functypes == alrdeftypes:
                self.Err.ThrowErr(Func.Loc["Line_Name"], Func.Loc["Start_Name"], Func.Loc["End_Name"], f"{UBrightMagenta}TypeChecker Error:{Reset} {BrightRed}(Function '{Func.Name}' has already been defined on line {alrdef.Loc['Line_Name']}){Reset}", Missing="", MisColour=BrightGreen)

        self.Scopes.append(self.Scope)
        self.Scope = ScopeManager(ParentScope=self.Scope) 
            
        for i in Func.Parameters:
            vr = self.Scope.MakeVar(i.Name, i)
            if vr == ScopeErrors.AlreadyExist:
                alrdef = self.Scope.GetVar(i.Name)
                self.Err.ThrowErr(i.Loc["Line_Name"], i.Loc["Start_Name"], i.Loc["End_Name"], f"{UBrightMagenta}TypeChecker Error:{Reset} {BrightRed}(Variable '{i.Name}' has already been defined on line {alrdef.Loc['Line_Name']}){Reset}", Missing="", MisColour=BrightGreen)
                
            
        for i in Func.Body:
            self.TypeCheckStmt(i)

        self.Scope = self.Scopes.pop()
            

   
    def TypeCheckBinExpr(self, BExpr: BinExpr):
        Op1_Type = self.TypeCheckExpr(BExpr.Left)
        Op2_Type = self.TypeCheckExpr(BExpr.Right)
