import ply.yacc as yacc
from tokens import *


# Ambiguity checking?
# Remove the Lexer error that Goutham said
# Pointer Type Statement in Grammar?
# Do we need to expand rules like Identifier, which is a token?

# As step 1, mapping directly from the pdf file
def p_Goal(p):
    ''' Goal : Program SEMICOLON '''

def p_Program(p):
    ''' Program : '''

def p_ProgramBlock(p):
    ''' ProgramBlock : '''

def p_Block(p):
    ''' Block : '''

def p_DeclSection(p):
    ''' DeclSection : '''

def p_CompoundStmt(p):
    ''' CompoundStmt : '''

def p_StmtList(p):
    ''' StmtList : '''

def p_Statement(p):
    ''' Statement : '''

def p_SimpleStatement(p):
    ''' SimpleStatement : '''

def p_StructStmt(p):
    ''' StructStmt : '''

def p_ConditionalStmt(p):
    ''' ConditionalStmt : '''

def p_IfStmt(p):
    ''' IfStmt : '''

def p_CaseStmt(p):
    ''' CaseStmt : '''

def p_CaseSelector(p):
    ''' CaseSelector : '''

def p_CaseLabel(p):
    ''' CaseLabel : '''

def p_LoopStmt(p):
    ''' LoopStmt : '''

def p_RepeatStmt(p):
    ''' RepeatStmt : '''

def p_WhileStmt(p):
    ''' WhileStmt : '''

def p_Expression(p):
    ''' Expression : '''

def p_SimpleExpression(p):
    ''' SimpleExpression : '''

def p_Term(p):
    ''' Term : '''

def p_Factor(p):
    ''' Factor : '''

def p_Type(p):
    ''' Type : '''

def p_SimpleType(p):
    ''' SimpleType : '''

def p_PointerType(p):
    ''' PointerType : '''

def p_StringType(p):
    ''' StringType : '''

def p_ProcedureType(p):
    ''' ProcedureType : '''

def p_TypeArgs(p):
    ''' TypeArgs : '''

def p_TypeID(p):
    ''' TypeID : '''

def p_OrdinalType(p):
    ''' OrdinalType : '''

def p_RealType(p):
    ''' RealType : '''

def p_TypeSection(p):
    ''' TypeSection : '''

def p_TypeDecl(p):
    ''' TypeDecl : '''

def p_RestrictedType(p):
    ''' RestrictedType : '''

def p_RelOp(p):
    ''' RelOp : '''

def p_AddOp(p):
    ''' AddOp : '''

def p_MulOp(p):
    ''' MulOp : '''

def p_ExprList(p):
    ''' ExprList : '''

def p_Designator(p):
    ''' Designator : '''

def p_DesignatorSubElem(p):
    ''' DesignatorSubElem : '''

def p_ConstSection(p):
    ''' ConstSection : '''

def p_ConstDecl(p):
    ''' ConstDecl : '''

def p_TypedConst(p):
    ''' TypedConst : '''

def p_Array(p):
    ''' Array : '''

def p_TypeArray(p):
    ''' TypeArray : '''

def p_ArrayConst(p):
    ''' ArrayConst : '''

def p_ConstExpr(p):
    ''' ConstExpr : '''

def p_Ident(p):
    ''' Ident : ID SEMICOLON'''

# WARNING
def p_Identifier(p):
    ''' Identifier : ID'''

def p_VarSection(p):
    ''' VarSection : '''

def p_VarDecl(p):
    ''' VarDecl : '''

def p_ProcedureDeclSection(p):
    ''' ProcedureDeclSection : '''

def p_ConstrucDecl(p):
    ''' ConstrucDecl : '''

def p_ConstrucHeading(p):
    ''' ConstrucHeading : '''

def p_FuncDecl(p):
    ''' FuncDecl : '''

def p_FuncHeading(p):
    ''' FuncHeading : '''

def p_FormalParams(p):
    ''' FormalParams : '''

def p_ProcedureDecl(p):
    ''' ProcedureDecl : '''

def p_ProcedureHeading(p):
    ''' ProcedureHeading : '''

### ---------------- LAMBDA DEFS -------------- ###

def p_LambFuncDecl(p):
    ''' LambFuncDecl : '''

def p_LambFunc(p):
    ''' LambFunc : '''

### ------------------------------------------- ###


### ---------------- OBJECT DEFS -------------- ###

def p_ObjType(p):
    ''' ObjType : '''

def p_ObjVis(p):
    ''' ObjVis :  '''

def p_ObjTypeSection(p):
    ''' ObjTypeSection : '''

def p_ObjConstSection(p):
    ''' ObjConstSection : '''

def p_ObjVarSection(p):
    ''' ObjVarSection : '''

def p_ObjMethodList(p):
    ''' ObjMethodList : '''

def p_ObjMethodHeading(p):
    ''' ObjMethodHeading : '''
### ------------------------------------------- ###

### --------------------- CLASS DEFS ------------ ###

def p_ClassType(p):
    ''' ClassType : '''

def p_ClassHeritage(p):
    ''' ClassHeritage : '''

def p_ClassVis(p):
    ''' ClassVis : '''

def p_ClassTypeSection(p):
    ''' ClassTypeSection : '''

def p_ClassConstSection(p):
    ''' ClassConstSection : '''

def p_ClassVarSection(p):
    ''' ClassVarSection : '''

def p_ClassMethodList(p):
    ''' ClassMethodList : '''

def p_ClassMethodHeading(p):
    ''' ClassMethodHeading : '''

### ---------------------------------------- ###


### ------------ INPUT / OUTPUT ------------ ###

def p_Input(p):
    ''' Input : '''

def p_Output(p):
    ''' Output : '''

### -------------------------------- ###



def main():
    parser = yacc.yacc()

    # Do the things that we want to here

if __name__ == '__main__':
    main()
