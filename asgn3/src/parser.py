import ply.yacc as yacc
from tokens import *

### ------------ ISSUES ----------- ###

# Ambiguity checking?
# Remove the Lexer error that Goutham said
# Use of Pointer Type Statement in Grammar? Since we are not working with pointers[?]
# Do we need to expand rules like Identifier, which is a token? NO

### ------------------------------- ###

# As step 1, mapping directly from the pdf file
def p_Goal(p):
    ''' Goal : Program '''

def p_Program(p):
    ''' Program : PROGRAM ID LPAREN IdentList RPAREN SEMICOLON ProgramBlock DOT '''
    # The rule in pdf is wrong as Ident has following semicolon

def p_ProgramBlock(p):
    ''' ProgramBlock : Block '''

def p_Block(p):
    ''' Block : DeclSection CompoundStmt'''

def p_DeclSection(p):
    ''' DeclSection : '''
    # Involves star over OR

def p_CompoundStmt(p):
    ''' CompoundStmt : BEGIN StmtList END SEMICOLON'''

def p_StmtList(p):
    ''' StmtList : Statement SEMICOLON
                | StmtList Statement SEMICOLON'''

def p_Statement(p):
    ''' Statement : SimpleStatement
                | StructStmt '''

def p_SimpleStatement(p):
    ''' SimpleStatement : '''

def p_StructStmt(p):
    ''' StructStmt : CompoundStmt
                    | ConditionalStmt 
                    | LoopStmt '''

def p_ConditionalStmt(p):
    ''' ConditionalStmt : IfStmt SEMICOLON
                        | CaseStmt SEMICOLON '''

def p_IfStmt(p):
    ''' IfStmt : IF THEN ELSE'''

def p_CaseStmt(p):
    ''' CaseStmt : '''

def p_CaseSelector(p):
    ''' CaseSelector : '''

def p_CaseLabel(p):
    ''' CaseLabel : ConstExpr DOTDOT ConstExpr SEMICOLON '''

def p_LoopStmt(p):
    ''' LoopStmt : RepeatStmt 
                | WhileStmt '''

def p_RepeatStmt(p):
    ''' RepeatStmt : REPEAT Statement UNTIL Expression SEMICOLON '''

def p_WhileStmt(p):
    ''' WhileStmt : WHILE Expression DO Statement SEMICOLON '''

def p_Expression(p):
    ''' Expression : SimpleExpression '''

def p_SimpleExpression(p):
    ''' SimpleExpression : '''

def p_Term(p):
    ''' Term : Factor '''

def p_Factor(p):
    ''' Factor : Designator '''

def p_Type(p):
    ''' Type : TypeID
            | SimpleType
            | PointerType
            | StringType
            | ProcedureType '''

def p_SimpleType(p):
    ''' SimpleType : OrdinalType
                | RealType '''

def p_PointerType(p):
    ''' PointerType : POWER ID '''

def p_StringType(p):
    ''' StringType : STRING
                | STRING LSQUARE ConstExpr RSQUARE '''

def p_ProcedureType(p):
    ''' ProcedureType : '''

def p_TypeArgs(p):
    ''' TypeArgs : '''

def p_TypeID(p):
    ''' TypeID : INTEGER
                | REAL
                | CHAR '''

def p_OrdinalType(p):
    ''' OrdinalType : INTEGER'''

def p_RealType(p):
    ''' RealType : DOUBLE'''

def p_TypeSection(p):
    ''' TypeSection : '''

def p_TypeDecl(p):
    ''' TypeDecl : '''

def p_RestrictedType(p):
    ''' RestrictedType : ObjType
                    | ClassType '''

def p_RelOp(p):
    ''' RelOp : '''

def p_AddOp(p):
    ''' AddOp : PLUS
            | MINUS
            | OR
            | XOR '''

def p_MulOp(p):
    ''' MulOp : MULTIPLY
            | DIVIDE
            | MOD
            | AND
            | SHL
            | SHR '''

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
    ''' TypedConst : ConstExpr
                    | ArrayConst '''

def p_Array(p):
    ''' Array : '''

def p_TypeArray(p):
    ''' TypeArray : TypeID
                | PointerType '''

def p_ArrayConst(p):
    ''' ArrayConst : '''

def p_ConstExpr(p):
    ''' ConstExpr : '''


def p_IdentList(p):
    ''' IdentList : '''

def p_VarSection(p):
    ''' VarSection : '''

def p_VarDecl(p):
    ''' VarDecl : '''

def p_ProcedureDeclSection(p):
    ''' ProcedureDeclSection : ProcedureDecl
                            | FuncDecl
                            | ConstrucDecl
                            | LambFuncDecl '''

def p_ConstrucDecl(p):
    ''' ConstrucDecl : ConstrucHeading SEMICOLON Block SEMICOLON '''

def p_ConstrucHeading(p):
    ''' ConstrucHeading : CONSTRUCTOR ID FormalParams '''

def p_FuncDecl(p):
    ''' FuncDecl : FuncHeading SEMICOLON Block SEMICOLON '''

def p_FuncHeading(p):
    ''' FuncHeading : FUNCTION ID LPAREN FormalParams RPAREN'''

def p_FormalParams(p):
    ''' FormalParams : IdentList '''

def p_ProcedureDecl(p):
    ''' ProcedureDecl : ProcedureHeading SEMICOLON Block SEMICOLON '''

def p_ProcedureHeading(p):
    ''' ProcedureHeading : PROCEDURE ID FormalParams '''

### ---------------- LAMBDA DEFS -------------- ###

def p_LambFuncDecl(p):
    ''' LambFuncDecl : ID COLON SimpleExpression '''

def p_LambFunc(p):
    ''' LambFunc : ID LPAREN ConstExpr RPAREN '''

### ------------------------------------------- ###


### ---------------- OBJECT DEFS -------------- ###

def p_ObjType(p):
    ''' ObjType : '''

def p_ObjVis(p):
    ''' ObjVis : PUBLIC '''

def p_ObjTypeSection(p):
    ''' ObjTypeSection : TypeSection '''

def p_ObjConstSection(p):
    ''' ObjConstSection : ConstSection '''

def p_ObjVarSection(p):
    ''' ObjVarSection : VarSection '''

def p_ObjMethodList(p):
    ''' ObjMethodList : '''

def p_ObjMethodHeading(p):
    ''' ObjMethodHeading : ProcedureHeading
                        | FuncHeading '''
### ------------------------------------------- ###

### --------------------- CLASS DEFS ------------ ###

def p_ClassType(p):
    ''' ClassType : '''

def p_ClassHeritage(p):
    ''' ClassHeritage : LPAREN IdentList RPAREN'''

def p_ClassVis(p):
    ''' ClassVis : PUBLIC'''

def p_ClassTypeSection(p):
    ''' ClassTypeSection : TypeSection '''

def p_ClassConstSection(p):
    ''' ClassConstSection : ConstSection '''

def p_ClassVarSection(p):
    ''' ClassVarSection : VarSection '''

def p_ClassMethodList(p):
    ''' ClassMethodList : '''

def p_ClassMethodHeading(p):
    ''' ClassMethodHeading : ProcedureHeading
                        | FuncHeading '''

### ---------------------------------------- ###


### ------------ INPUT / OUTPUT ------------ ###

def p_Input(p):
    ''' Input : READ
            | READLN LPAREN IdentList RPAREN '''

def p_Output(p):
    ''' Output : WRITE
            | WRITELN LPAREN IdentList RPAREN '''

### -------------------------------- ###



def main():
    parser = yacc.yacc()

    # Do the things that we want to here

if __name__ == '__main__':
    main()
