import ply.yacc as yacc
import sys
import ply.lex as lex
from tokens import *
from lexer import *

### ------------ ISSUES ----------- ###

# Ambiguity checking?
# Remove the Lexer error that Goutham said
# Use of Pointer Type Statement in Grammar? Since we are not working with pointers[?]
# Do we need to expand rules like Identifier, which is a token? NO

### ------------------------------- ###

def p_Goal(p):
    ''' Goal : Program '''

def p_Program(p):
    ''' Program : PROGRAM ID  SEMICOLON Block '''

def p_Block(p):
    ''' Block : CompoundStmt
    | DeclSection CompoundStmt'''

def p_DeclSection(p):
    ''' DeclSection : DeclSection WhichSection
    | '''

def p_WhichSection(p):
    ''' WhichSection : ConstSection
    | TypeSection
    | VarSection
    | ProcedureDeclSection '''

def p_CompoundStmt(p):
    ''' CompoundStmt : BEGIN StmtList END SEMICOLON '''

def p_StmtList(p):
    ''' StmtList : StmtList Statement SEMICOLON
    | Statement SEMICOLON '''

def p_Statement(p):
    ''' Statement : SimpleStatement
    | StructStmt 
    | '''

def p_SimpleStatement(p):
    ''' SimpleStatement : Designator
    | Designator LPAREN ExprList RPAREN
    | Designator ASSIGNTO Expression
    | INHERITED
    | LPAREN Expression RPAREN'''

def p_StructStmt(p):
    ''' StructStmt : CompoundStmt
    | ConditionalStmt 
    | LoopStmt '''

def p_ConditionalStmt(p):
    ''' ConditionalStmt : IfStmt SEMICOLON
    | CaseStmt SEMICOLON '''

def p_IfStmt(p):
    ''' IfStmt : IF Expression THEN Statement 
    | IF Expression THEN Statement ELSE Statement '''

def p_CaseStmt(p):
    ''' CaseStmt : CASE Expression OF CaseSelector ColonCaseSelector END
    | CASE Expression OF CaseSelector ColonCaseSelector ELSE Statement SEMICOLON END '''

def p_ColonCaseSelector(p):
    ''' ColonCaseSelector : ColonCaseSelector SEMICOLON CaseSelector 
    | '''

def p_CaseSelector(p):
    ''' CaseSelector : CaseLabel COLON Statement '''


def p_CaseLabel(p):
    # THIS IS NOT CORRECT. WILL PUT INTEGER/NUMBER
    ''' CaseLabel : NUMBER '''

def p_LoopStmt(p):
    ''' LoopStmt : RepeatStmt
    | WhileStmt '''

def p_RepeatStmt(p):
    ''' RepeatStmt : REPEAT Statement UNTIL Expression SEMICOLON '''

def p_WhileStmt(p):
    ''' WhileStmt : WHILE Expression DO Statement SEMICOLON '''

def p_Expression(p):
    ''' Expression : SimpleExpression RelSimpleStar '''

def p_RelSimpleStar(p):
    ''' RelSimpleStar : RelOp SimpleExpression RelSimpleStar
    | '''

def p_SimpleExpression(p):
    ''' SimpleExpression : PLUS Term AddTermStar
    | MINUS Term AddTermStar 
    | Term AddTermStar '''

def p_AddTermStar(p):
    ''' AddTermStar : AddOp Term AddTermStar
    | '''

def p_Term(p):
    ''' Term : Factor MulFacStar '''

def p_MulFacStar(p):
    ''' MulFacStar : MulOp Factor MulFacStar
    | '''

def p_Factor(p):
    ''' Factor : Designator 
    | Designator LPAREN ExprList RPAREN
    | USERSTRING
    | NUMBER
    | LPAREN Expression RPAREN
    | NOT Factor
    | INHERITED Designator
    | INHERITED
    | TypeID LPAREN Expression RPAREN
    | LPAREN LambFunc RPAREN '''

# Added ID as a form of type for handling objects and classes
def p_Type(p):
    ''' Type : TypeID
    | SimpleType
    | PointerType
    | StringType
    | ProcedureType 
    | Array 
    | ID'''

def p_SimpleType(p):
    ''' SimpleType : OrdinalType
    | RealType '''

def p_PointerType(p):
    ''' PointerType : POWER ID '''

def p_StringType(p):
    ''' StringType : STRING '''

def p_ProcedureType(p):
    ''' ProcedureType : ProcedureHeading
    | FuncHeading
    '''

def p_TypeArgs(p):
    ''' TypeArgs : LANGLE TypeID RANGLE
    | LANGLE STRING RANGLE '''

def p_TypeID(p):
    ''' TypeID : INTEGER
    | REAL
    | CHAR '''

def p_OrdinalType(p):
    ''' OrdinalType : INTEGER'''

def p_RealType(p):
    ''' RealType : DOUBLE'''

# Added without the keyword TYPE for classes and objects
def p_TypeSection(p):
    ''' TypeSection : TYPE ColonTypeDecl 
    | ColonTypeDecl'''

def p_ColonTypeDecl(p):
    ''' ColonTypeDecl : ColonTypeDecl TypeDecl SEMICOLON 
    | '''

def p_TypeDecl(p):
    ''' TypeDecl : ID EQUALS Type
    | ID EQUALS RestrictedType
    | ID EQUALS TYPE Type
    | ID EQUALS TYPE RestrictedType '''

def p_RestrictedType(p):
    ''' RestrictedType : ObjectType
    | ClassType '''

def p_RelOp(p):
    ''' RelOp : LANGLE
    | RANGLE
    | GEQ
    | LEQ
    | NOTEQUALS
    | EQUALS'''

def p_AddOp(p):
    ''' AddOp : PLUS
    | MINUS
    | OR
    | XOR '''

def p_MulOp(p):
    ''' MulOp : MULTIPLY
    | DIVIDE
    | DIV
    | MOD
    | AND
    | SHL
    | SHR '''

def p_CommaExpression(p):
    ''' CommaExpression : CommaExpression COMMA Expression
    | '''

def p_ExprList(p):
    ''' ExprList : Expression CommaExpression'''

def p_Designator(p):
    ''' Designator : ID DesSubEleStar'''

def p_DesSubEleStar(p):
    ''' DesSubEleStar : DesSubEleStar DesignatorSubElem 
    | '''

def p_DesignatorSubElem(p):
    ''' DesignatorSubElem : DOT ID
    | LSQUARE ExprList RSQUARE
    | POWER SEMICOLON '''

# Added without keyword CONSTANT for classes and objects
def p_ConstSection(p):
    ''' ConstSection : CONSTANT ColonConstDecl
    | '''

def p_ColonConstDecl(p):
    ''' ColonConstDecl : ColonConstDecl ConstDecl SEMICOLON
    | '''

def p_ConstDecl(p):
    ''' ConstDecl : ID EQUALS ConstExpr
    | ID COLON TypeID EQUALS TypedConst '''

def p_TypedConst(p):
    ''' TypedConst : ConstExpr
    | ArrayConst '''

def p_Array(p):
    ''' Array : ARRAY LSQUARE ONE DOTDOT OrdinalType RSQUARE OF TypeArray '''

def p_TypeArray(p):
    ''' TypeArray : TypeID
    | PointerType '''

def p_ArrayConst(p):
    ''' ArrayConst : LPAREN TypedConst CommaTypedConst RPAREN '''

def p_CommaTypedConst(p):
    ''' CommaTypedConst : CommaTypedConst COMMA TypedConst 
    | '''

def p_ConstExpr(p):
    ''' ConstExpr : '''


def p_IdentList(p):
    ''' IdentList : ID TypeArgs CommaIDTypeArgs
    | ID CommaIDTypeArgs'''

def p_CommaIDTypeArgs(p):
    ''' CommaIDTypeArgs : CommaIDTypeArgs COMMA ID TypeArgs
    | CommaIDTypeArgs COMMA ID                 
    | '''

# Added VarSection without starting with the keyword VAR for classes and objects
def p_VarSection(p):
    ''' VarSection : VAR ColonVarDecl 
    | ColonVarDecl'''

def p_ColonVarDecl(p):
    ''' ColonVarDecl : VarDecl SEMICOLON ColonVarDecl
    | '''

def p_VarDecl(p):
    ''' VarDecl : IdentList COLON Type'''

def p_ProcedureDeclSection(p):
    ''' ProcedureDeclSection : ProcedureDecl
    | FuncDecl
    | ConstrucDecl
    | LambFuncDecl '''

# Don't need to add SEMICOLON after Block
def p_ConstrucDecl(p):
    ''' ConstrucDecl : ConstrucHeading SEMICOLON Block '''

def p_ConstrucHeading(p):
    ''' ConstrucHeading : CONSTRUCTOR ID FormalParams '''

def p_FuncDecl(p):
    ''' FuncDecl : FuncHeading SEMICOLON Block '''

def p_FuncHeading(p):
    ''' FuncHeading : FUNCTION ID LPAREN FormalParams RPAREN'''

def p_FuncHeadingSemicolon(p):
    ''' FuncHeadingSemicolon : FUNCTION ID LPAREN FormalParams RPAREN SEMICOLON'''

def p_FormalParams(p):
    ''' FormalParams : IdentList 
    | '''

def p_ProcedureDecl(p):
    ''' ProcedureDecl : ProcedureHeading SEMICOLON Block '''

#replaced ID by designator for dealing with Object.Function
def p_ProcedureHeading(p):
    ''' ProcedureHeading : PROCEDURE Designator FormalParams '''

def p_ProcedureHeadingSemicolon(p):
    ''' ProcedureHeadingSemicolon : PROCEDURE Designator FormalParams SEMICOLON '''

### ---------------- LAMBDA DEFS -------------- ###

def p_LambFuncDecl(p):
    ''' LambFuncDecl : ID COLON SimpleExpression '''

def p_LambFunc(p):
    ''' LambFunc : ID LPAREN ConstExpr RPAREN '''

### ------------------------------------------- ###


### ---------------- OBJECT DEFS -------------- ###

def p_ObjectType(p):
    ''' ObjectType : OBJECT ObjectHeritage ObjectBody END'''

def p_ObjectHeritage(p):
    ''' ObjectHeritage : LPAREN IdentList RPAREN
    | '''

# The problem here is that the first Identifier list is being identified as that in VarSection rather than type section
def p_ObjectBody(p): 
    ''' ObjectBody : ObjectBody ObjectVis ObjectVarSection ObjectTypeSection ObjectConstSection ObjectMethodList
    | '''
    
def p_ObjectVis(p):
    ''' ObjectVis : PUBLIC
    | '''

def p_ObjectVarSection(p):
    ''' ObjectVarSection : VarSection 
    | '''

def p_ObjectTypeSection(p):
    ''' ObjectTypeSection : TypeSection 
    | '''

def p_ObjectConstSection(p):
    ''' ObjectConstSection : ConstSection 
    | '''

def p_ObjectMethodList(p):
    ''' ObjectMethodList : ObjectMethodHeading 
    | '''

def p_ObjectMethodHeading(p):
    ''' ObjectMethodHeading : ProcedureHeadingSemicolon
    | FuncHeadingSemicolon '''

### ------------------------------------------- ###

### --------------------- CLASS DEFS ------------ ###

def p_ClassType(p):
    ''' ClassType : CLASS ClassHeritage ClassBody END'''

def p_ClassHeritage(p):
    ''' ClassHeritage : LPAREN IdentList RPAREN
    | '''

def p_ClassBody(p):
    ''' ClassBody : ClassBody ClassVis ClassTypeSection ClassConstSection ClassVarSection ClassMethodList
    | '''
    
def p_ClassVis(p):
    ''' ClassVis : PUBLIC
    | '''

def p_ClassTypeSection(p):
    ''' ClassTypeSection : TypeSection 
    | '''

def p_ClassConstSection(p):
    ''' ClassConstSection : ConstSection 
    | '''

def p_ClassVarSection(p):
    ''' ClassVarSection : VarSection 
    | '''

def p_ClassMethodList(p):
    ''' ClassMethodList : ClassMethodHeading 
    | '''

def p_ClassMethodHeading(p):
    ''' ClassMethodHeading : ProcedureHeadingSemicolon
    | FuncHeadingSemicolon '''

### ---------------------------------------- ###


# def p_Input(p):
    # ''' Input : READ
    # | READLN LPAREN IdentList RPAREN '''

# def p_Output(p):
    # ''' Output : WRITE
    # | WRITELN LPAREN IdentList RPAREN '''

### -------------------------------- ###

def p_error(p):
    print "Syntax Error at Line: %d, Pos: %d"%(p.lineno,p.lexpos)
    # Add formatters later here, to fetch line number and position


def main():
    parser = yacc.yacc()

    # Do the things that we want to here
    inputfile = open(sys.argv[1],'r').read()
    yacc.parse(inputfile, debug = 1)

if __name__ == '__main__':
    main()
