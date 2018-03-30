import ply.yacc as yacc
import sys
import ply.lex as lex
from tokens import *
from lexer import *
from SymTable import SymTable
from ThreeAddrCode import ThreeAddrCode

### ------------ ISSUES ----------- ###

# Ambiguity checking?
# Remove the Lexer error that Goutham said
# Use of Pointer Type Statement in Grammar? Since we are not working with pointers[?]
# Do we need to expand rules like Identifier, which is a token? NO

### ------------------------------- ###
reverse_output = []

precedence = (
    ('nonassoc','ELSETOK'),
    ('nonassoc','ELSE'),
    ('nonassoc','IDTOK'),
    ('nonassoc','ID'),
    ('nonassoc','ENDTOK'),
    ('nonassoc','END'),
    ('nonassoc', 'TOK'),
    ('nonassoc','PROCEDURE'),
    ('nonassoc','FUNCTION'),
    ('nonassoc','CONSTRUCTOR')
)

#factor should be a dictionary with attributes 'place' and 'isArray'
def resolveRHSArray(factor):
    if factor['isArray']:
        lhs = symTab.getTemp()
        tac.emit('LOADREF', lhs, factor['place'], factor['ArrayIndex'])
        factor['place'] = lhs

def updateStar(p):

    p[0] = {}
    p[0]['place'] = p[2]['place']
    p[0]['previousOp'] = p[1]
    p[0]['ExprList'] = []
    resolveRHSArray(p[2])
    
    if p[3]!={}:
        p[0]['ExprList'] = p[3]['ExprList']
        p[0]['ExprList'].append([p[3]['previousOp'],p[2]['place'],p[3]['place']])

def handleTerm(p, termIndex=1, starIndex=2, whetherRelational=False):

    p[0]={}
    p[0]['ExprList'] = p[starIndex]['ExprList']
    p[0]['ExprList'].append([p[starIndex]['previousOp'],p[termIndex]['place'],p[starIndex]['place']])
    #reversing the list for left associativity 
    p[0]['ExprList'] = p[0]['ExprList'][::-1]
    #expr is of the form [op,op1,op2]
    for i,expr in enumerate(p[0]['ExprList']):
        lhs = symTab.getTemp()        
        tac.emit(expr[0],lhs,expr[1],expr[2])
        if i != len(p[0]['ExprList'])-1:
            p[0]['ExprList'][i+1][1] = lhs
    p[0]['place'] = lhs
    #I'm making this False because array will be handled in MulFacStar (no need to handle it for term)
    p[0]['isArray'] = False
        
def p_Goal(p):
    ''' Goal : Program '''
    reverse_output.append(p.slice)

def p_Program(p):
    ''' Program : PROGRAM ID SEMICOLON Block 
    | PROGRAM ID LPAREN IdentList RPAREN SEMICOLON Block'''
    reverse_output.append(p.slice)

def p_Block(p):
    ''' Block : DeclSection CompoundStmt'''
    reverse_output.append(p.slice)

def p_DeclSection(p):
    ''' DeclSection : DeclSection WhichSection
    | '''
    reverse_output.append(p.slice)

def p_WhichSection(p):
    ''' WhichSection : ConstSection
    | TypeSection
    | VarSection
    | ProcedureDeclSection '''
    reverse_output.append(p.slice)

def p_CompoundStmt(p):
    ''' CompoundStmt : BEGIN StmtList END SEMICOLON '''
    reverse_output.append(p.slice)

def p_StmtList(p):
    ''' StmtList : Statement StmtList 
    | Statement'''
    reverse_output.append(p.slice)

def p_Statement(p):
    ''' Statement : SimpleStatement SEMICOLON
    | StructStmt '''
    reverse_output.append(p.slice)

def p_SimpleStatement(p):
    ''' SimpleStatement : Designator
    | Designator LPAREN ExprList RPAREN
    | Designator ASSIGNTO Expression
    | INHERITED
    | LPAREN Expression RPAREN
    | BREAK
    | CONTINUE'''

    if p[2] == ':=':

        if p[1]['isArray']:
            tac.emit('STOREREF',p[1]['place'],p[1]['ArrayIndex'],p[3]['place'])
            
        else:
            tac.emit('+',p[1]['place'],p[3]['place'],'0')
        
    reverse_output.append(p.slice)

def p_StructStmt(p):
    ''' StructStmt : CompoundStmt
    | ConditionalStmt 
    | LoopStmt '''
    reverse_output.append(p.slice)

# Removed semicolon from if and case
def p_ConditionalStmt(p):
    ''' ConditionalStmt : IfStmt
    | CaseStmt '''
    reverse_output.append(p.slice)

def p_IfStmt(p):
    ''' IfStmt : IF Expression THEN IfMark1 CompoundStmt ELSE IfMark3 CompoundStmt IfMark4
    | IF Expression THEN IfMark1 CompoundStmt IfMark2 %prec ELSETOK '''
    reverse_output.append(p.slice)

## ------------ IF DEFS ----------- ##
def p_IfMark1(p):
    ''' IfMark1 : '''
    l1 = symTab.getLabel()
    tac.emit('CMP','',p[-2]['place'],'0')
    tac.emit('JE','',l1,'')
    p[0] = l1

def p_IfMark2(p):
    ''' IfMark2 :  '''
    label = p[-2]
    tac.emit('LABEL','',label,'')

def p_IfMark3(p):
    ''' IfMark3 :  '''
    l1 = symTab.getLabel()
    label = p[-3]
    tac.emit('JMP','',l1,'')
    tac.emit('LABEL','',label,'')
    p[0] = l1

def p_IfMark4(p):
    ''' IfMark4 : '''
    tac.emit('LABEL','',p[-2],'')
## ------------ IF DEFS END ------ ###

#testMark is for the function test as in Sir's slides
def p_CaseStmt(p):
    ''' CaseStmt : CASE Expression OF CaseSelector ColonCaseSelector END
    | CASE Expression OF CaseSelector ColonCaseSelector ELSE CompoundStmt END '''
    reverse_output.append(p.slice)

def p_ColonCaseSelector(p):
    ''' ColonCaseSelector : SEMICOLON CaseSelector ColonCaseSelector 
    | '''
    reverse_output.append(p.slice)

def p_CaseSelector(p):
    ''' CaseSelector : CaseLabel COLON Statement'''
    
    reverse_output.append(p.slice)


def p_CaseLabel(p):
    # THIS IS NOT CORRECT. WILL PUT INTEGER/NUMBER
    ''' CaseLabel : NUMBER '''

    p[0] = p[1]
    reverse_output.append(p.slice)

def p_LoopStmt(p):
    ''' LoopStmt : RepeatStmt
    | WhileStmt '''
    reverse_output.append(p.slice)

def p_RepeatStmt(p):
    ''' RepeatStmt : REPEAT Statement UNTIL Expression SEMICOLON '''
    reverse_output.append(p.slice)

#No need of semicolon after WhileStmt because CompoundStmt will handle it
def p_WhileStmt(p):
    ''' WhileStmt : WHILE WhileMark1 Expression DO WhileMark2 CompoundStmt WhileMark3'''
    reverse_output.append(p.slice)

def p_WhileMark1(p):
    ''' WhileMark1 :  '''
    l1 = symTab.getLabel()
    l2 = symTab.getLabel()
    tac.emit('LABEL','',l1,'')
    p[0] = [l1,l2]

def p_WhileMark2(p):
    ''' WhileMark2 :  '''
    tac.emit('CMP','',p[-2]['place'],'0')
    tac.emit('JE','',p[-3][1],'') # Jump to l2, that is exit

def p_WhileMark3(p):
    ''' WhileMark3 :  '''
    tac.emit('JMP','',p[-5][0],'') # Go back to l1
    tac.emit('LABEL','',p[-5][1],'') # l2, This is exit

def p_Expression(p):
    ''' Expression : SimpleExpression RelSimpleStar 
    | LambFunc'''

    # Expression has dictionary attribute
    if len(p) == 3:

        if p[2] != {}:
            handleTerm(p,1,2,True)

        else:
            p[0] = p[1]
            
    reverse_output.append(p.slice)

def p_RelSimpleStar(p):
    ''' RelSimpleStar : RelOp SimpleExpression RelSimpleStar
    | '''

    if len(p) == 1:
        p[0] = {}

    else:
        updateStar(p)
            
    reverse_output.append(p.slice)

def p_SimpleExpression(p):
    ''' SimpleExpression : Term AddTermStar
    | MINUS Term AddTermStar '''

    if len(p) == 3:
        starIndex = 2
        termIndex = 1
    else:
        starIndex = 3
        termIndex = 2
    
    if p[starIndex] != {}:
        handleTerm(p, termIndex, starIndex)

    else:
        p[0] = p[1]

    if len(p) == 4:
        tac.emit('-',p[0]['place'],'0',p[0]['place'])
        
    reverse_output.append(p.slice)

def p_AddTermStar(p):
    ''' AddTermStar : AddOp Term AddTermStar
    | '''

    # p[0] is dictionary here
    if len(p) == 1:
        p[0] = {}

    else:
        updateStar(p)
        
    reverse_output.append(p.slice)

def p_Term(p):
    ''' Term : Factor MulFacStar '''
    
    if p[2] != {}:
        handleTerm(p)

    else:
        p[0] = p[1]
        resolveRHSArray(p[1])
        
    reverse_output.append(p.slice)

def p_MulFacStar(p):
    ''' MulFacStar : MulOp Factor MulFacStar
    | '''

    # p[0] is dictionary here
    if len(p) == 1:
        p[0] = {}

    else:
        updateStar(p)
            
    reverse_output.append(p.slice)

def p_Factor(p):
    ''' Factor : Designator 
    | Designator LPAREN ExprList RPAREN
    | USERSTRING
    | NUMBER
    | LPAREN Expression RPAREN
    | NOT Factor
    | INHERITED Designator
    | INHERITED
    | TypeID LPAREN Expression RPAREN '''

    p[0] = {}

    if type(p[1]) is dict:
        p[0] = p[1]
    else:
        p[0]['place'] = p[1]
        p[0]['isArray'] = False

    # print(p[0])
    reverse_output.append(p.slice)

# Added ID as a form of type for handling objects and classes
def p_Type(p):
    ''' Type : TypeID
    | PointerType
    | StringType
    | ProcedureType 
    | Array 
    | ID'''

    p[0] = p[1]
    reverse_output.append(p.slice)

def p_PointerType(p):
    ''' PointerType : POWER ID '''

    p[0] = 'POINTER'
    reverse_output.append(p.slice)

def p_StringType(p):
    ''' StringType : STRING '''

    p[0] = p[1]
    reverse_output.append(p.slice)

def p_ProcedureType(p):
    ''' ProcedureType : ProcedureHeading
    | FuncHeading
    '''

    reverse_output.append(p.slice)

def p_TypeArgs(p):
    ''' TypeArgs : LPAREN TypeID RPAREN
    | LPAREN STRING RPAREN '''

    reverse_output.append(p.slice)

def p_TypeID(p):
    ''' TypeID : INTEGER
    | DOUBLE
    | CHAR '''

    p[0] = p[1]
    reverse_output.append(p.slice)

# def p_OrdinalType(p):
#     ''' OrdinalType : INTEGER'''
#     reverse_output.append(p.slice)

# def p_RealType(p):
    # ''' RealType : DOUBLE'''
    # reverse_output.append(p.slice)

# Added without the keyword TYPE for classes and objects

def p_TypeSection(p):
    ''' TypeSection : TYPE ColonTypeDecl '''
    reverse_output.append(p.slice)

def p_ColonTypeDecl(p):
    ''' ColonTypeDecl : ColonTypeDecl TypeDecl SEMICOLON 
    | TypeDecl SEMICOLON'''
    reverse_output.append(p.slice)

def p_TypeDecl(p):
    ''' TypeDecl : ID EQUALS Type
    | ID EQUALS RestrictedType
    | ID EQUALS TYPE Type
    | ID EQUALS TYPE RestrictedType '''
    reverse_output.append(p.slice)

def p_RestrictedType(p):
    ''' RestrictedType : ObjectType
    | ClassType '''
    reverse_output.append(p.slice)

def p_RelOp(p):
    ''' RelOp : LANGLE
    | RANGLE
    | GEQ
    | LEQ
    | NOTEQUALS
    | EQUALS'''

    p[0] = p[1]
    reverse_output.append(p.slice)

def p_AddOp(p):
    ''' AddOp : PLUS
    | MINUS
    | OR
    | XOR '''
    p[0] = p[1]
    reverse_output.append(p.slice)

def p_MulOp(p):
    ''' MulOp : MULTIPLY
    | DIVIDE
    | DIV
    | MOD
    | AND
    | SHL
    | SHR 
    | DOUBLESTAR '''

    p[0] = p[1]
    reverse_output.append(p.slice)

def p_CommaExpression(p):
    ''' CommaExpression : CommaExpression COMMA Expression
    | '''
    reverse_output.append(p.slice)

def p_ExprList(p):
    ''' ExprList : Expression CommaExpression'''
    reverse_output.append(p.slice)

def p_Designator(p):
    ''' Designator : ID DesSubEleStar'''

    p[0] = p[2]
    p[0]['place'] = p[1]

    reverse_output.append(p.slice)

def p_DesSubEleStar(p):
    ''' DesSubEleStar : DesSubEleStar DesignatorSubElem 
    | '''
    
    if len(p) == 1:
        p[0] = {}
        p[0]['isArray'] = False
    else:
        p[0] = p[2]

    reverse_output.append(p.slice)

#replaced ExprList by Expression for simplicity
def p_DesignatorSubElem(p):
    ''' DesignatorSubElem : DOT ID
    | LSQUARE Expression RSQUARE
    | POWER '''

    if len(p) == 4:
        p[0] = {}
        p[0]['isArray'] = True
        p[0]['ArrayIndex'] = p[2]['place']
    else:
        p[0] = {}
        p[0]['isArray'] = False
        
    reverse_output.append(p.slice)

# Added without keyword CONSTANT for classes and objects
def p_ConstSection(p):
    ''' ConstSection : CONSTANT ColonConstDecl '''
    reverse_output.append(p.slice)

#Making this left recursive helps to remove a shift-reduce conflict
def p_ColonConstDecl(p):
    ''' ColonConstDecl : ColonConstDecl ConstDecl SEMICOLON
    | ConstDecl SEMICOLON'''
    reverse_output.append(p.slice)

def p_ConstDecl(p):
    ''' ConstDecl : ID EQUALS ConstExpr
    | ID COLON TypeID EQUALS TypedConst '''

    if len(p) == 4:
        tac.emit('+',p[1],p[3],'0')
        
    reverse_output.append(p.slice)

def p_TypedConst(p):
    ''' TypedConst : ConstExpr
    | ArrayConst '''
    reverse_output.append(p.slice)
    
def p_Array(p):
    ''' Array : ARRAY LSQUARE ArrayBetween RSQUARE OF TypeArray '''
    reverse_output.append(p.slice)

def p_ArrayBetween(p):
    ''' ArrayBetween : NUMBER DOT DOT NUMBER
    | NUMBER DOT DOT ID
    | ID DOT DOT ID
    | ID DOT DOT NUMBER '''
    reverse_output.append(p.slice)

def p_TypeArray(p):
    ''' TypeArray : TypeID
    | PointerType '''
    reverse_output.append(p.slice)

def p_ArrayConst(p):
    ''' ArrayConst : LPAREN TypedConst CommaTypedConst RPAREN '''
    reverse_output.append(p.slice)

def p_CommaTypedConst(p):
    ''' CommaTypedConst : COMMA TypedConst CommaTypedConst
    | '''
    reverse_output.append(p.slice)

def p_ConstExpr(p):
    ''' ConstExpr : NUMBER'''
    p[0] = p[1]
    reverse_output.append(p.slice)

#the identList for procedure definition and var declaration is not the same
def p_IdentList(p):
    ''' IdentList : ID TypeArgs CommaIDTypeArgs
    | ID CommaIDTypeArgs'''

    if len(p) == 3:
        if p[2] == None:
            p[0] = []
        else:
            p[0] = p[2]

        p[0].append(p[1])

    reverse_output.append(p.slice)

def p_CommaIDTypeArgs(p):
    ''' CommaIDTypeArgs : COMMA ID TypeArgs CommaIDTypeArgs
    | COMMA ID CommaIDTypeArgs                 
    | '''
    
    if len(p) == 4:
        if p[3] == None:
            p[0] = []
        else:
            p[0] = p[3]
        p[0].append(p[2])
    reverse_output.append(p.slice)

#ParamIdentList and ParamIdent are added for handling Formal Parameters for function or procedure declaration
def p_ParamIdentList(p):
    ''' ParamIdentList : ParamIdent SEMICOLON ParamIdentList
    | ParamIdent
    | '''
    reverse_output.append(p.slice)

def p_ParamIdent(p):
    ''' ParamIdent : IdentList COLON Type
    | IdentList '''
    reverse_output.append(p.slice)
    
# Added VarSection without starting with the keyword VAR for classes and objects
def p_VarSection(p):
    ''' VarSection : VAR ColonVarDecl '''
    reverse_output.append(p.slice)

def p_ColonVarDecl(p):
    ''' ColonVarDecl : ColonVarDecl VarDecl SEMICOLON
    | VarDecl SEMICOLON'''
    reverse_output.append(p.slice)

def p_VarDecl(p):
    ''' VarDecl : IdentList COLON Type'''
    for elem in p[1]:

        # tac.emit('+',elem,'0','0')

        symTab.symTabOp(elem,p[3].lower(),'VAR')
    
    reverse_output.append(p.slice)

def p_ProcedureDeclSection(p):
    ''' ProcedureDeclSection : ProcedureDecl
    | FuncDecl
    | ConstrucDecl '''
    reverse_output.append(p.slice)

# Don't need to add SEMICOLON after Block
def p_ConstrucDecl(p):
    ''' ConstrucDecl : ConstrucHeading SEMICOLON Block '''
    reverse_output.append(p.slice)

def p_ConstrucHeading(p):
    ''' ConstrucHeading : CONSTRUCTOR Designator FormalParams '''
    reverse_output.append(p.slice)

def p_ConstrucHeadingSemicolon(p):
    ''' ConstrucHeadingSemicolon : CONSTRUCTOR Designator FormalParams SEMICOLON '''
    reverse_output.append(p.slice)

def p_FuncDecl(p):
    ''' FuncDecl : FuncHeading SEMICOLON Block '''
    reverse_output.append(p.slice)

def p_FuncHeading(p):
    ''' FuncHeading : FUNCTION Designator FormalParams COLON Type '''
    reverse_output.append(p.slice)

def p_FuncHeadingSemicolon(p):
    ''' FuncHeadingSemicolon : FUNCTION Designator FormalParams COLON Type SEMICOLON '''
    reverse_output.append(p.slice)

#Included LPAREN and RPAREN in the definition of FORMALPARAMS
def p_FormalParams(p):
    ''' FormalParams : LPAREN ParamIdentList RPAREN
    | '''
    reverse_output.append(p.slice)

def p_ProcedureDecl(p):
    ''' ProcedureDecl : ProcedureHeading SEMICOLON Block '''
    reverse_output.append(p.slice)

#replaced ID by designator for dealing with Object.Function
def p_ProcedureHeading(p):
    ''' ProcedureHeading : PROCEDURE Designator FormalParams '''
    reverse_output.append(p.slice)

def p_ProcedureHeadingSemicolon(p):
    ''' ProcedureHeadingSemicolon : PROCEDURE Designator FormalParams SEMICOLON '''
    reverse_output.append(p.slice)

### ---------------- LAMBDA DEFS -------------- ###

def p_LambFunc(p):
    ''' LambFunc : LAMBDA ID COLON SimpleExpression '''
    reverse_output.append(p.slice)

# def p_LambFunc(p):
#     ''' LambFunc : ID LPAREN ConstExpr RPAREN '''
#     reverse_output.append(p.slice)

### ------------------------------------------- ###


### ---------------- OBJECT DEFS -------------- ###

def p_ObjectType(p):
    ''' ObjectType : OBJECT ObjectHeritage ObjectVis ObjectBody END'''
    reverse_output.append(p.slice)

def p_ObjectHeritage(p):
    ''' ObjectHeritage : LPAREN IdentList RPAREN
    | '''
    reverse_output.append(p.slice)

# The problem here is that the first Identifier list is being identified as that in VarSection rather than type section
def p_ObjectBody(p): 
    ''' ObjectBody : ObjectBody ObjectTypeSection ObjectVarSection ObjectConstSection ObjectMethodList
    | '''
    reverse_output.append(p.slice)
    
def p_ObjectVis(p):
    ''' ObjectVis : PUBLIC
    | '''
    reverse_output.append(p.slice)

def p_ObjectVarSection(p):
    ''' ObjectVarSection : ColonVarDecl %prec IDTOK
    | '''
    reverse_output.append(p.slice)

def p_ObjectTypeSection(p):
    ''' ObjectTypeSection : ColonTypeDecl %prec IDTOK
    | %prec ENDTOK '''
    reverse_output.append(p.slice)

def p_ObjectConstSection(p):
    ''' ObjectConstSection : ColonConstDecl %prec IDTOK
    | '''
    reverse_output.append(p.slice)

def p_ObjectMethodList(p):
    ''' ObjectMethodList : ObjectMethodHeading 
    | %prec TOK '''
    reverse_output.append(p.slice)

def p_ObjectMethodHeading(p):
    ''' ObjectMethodHeading : ProcedureHeadingSemicolon
    | FuncHeadingSemicolon 
    | ConstrucHeadingSemicolon '''
    reverse_output.append(p.slice)

### ------------------------------------------- ###

### --------------------- CLASS DEFS ------------ ###

def p_ClassType(p):
    ''' ClassType : CLASS ClassHeritage ClassVis ClassBody END'''
    reverse_output.append(p.slice)

def p_ClassHeritage(p):
    ''' ClassHeritage : LPAREN IdentList RPAREN
    | '''
    reverse_output.append(p.slice)

def p_ClassBody(p):
    ''' ClassBody : ClassBody ClassTypeSection ClassConstSection ClassVarSection ClassMethodList
    | '''
    reverse_output.append(p.slice)
    
def p_ClassVis(p):
    ''' ClassVis : PUBLIC
    | '''
    reverse_output.append(p.slice)

def p_ClassTypeSection(p):
    ''' ClassTypeSection : ColonTypeDecl %prec IDTOK
    | %prec ENDTOK '''
    reverse_output.append(p.slice)

def p_ClassConstSection(p):
    ''' ClassConstSection : ColonConstDecl %prec IDTOK
    | '''
    reverse_output.append(p.slice)

def p_ClassVarSection(p):
    ''' ClassVarSection : ColonVarDecl %prec IDTOK
    | '''
    reverse_output.append(p.slice)

def p_ClassMethodList(p):
    ''' ClassMethodList : ClassMethodHeading 
    | %prec TOK '''
    reverse_output.append(p.slice)

def p_ClassMethodHeading(p):
    ''' ClassMethodHeading : ProcedureHeadingSemicolon
    | FuncHeadingSemicolon 
    | ConstrucHeadingSemicolon '''
    reverse_output.append(p.slice)

### ---------------------------------------- ###


# def p_Input(p):
    # ''' Input : READ
    # | READLN LPAREN IdentList RPAREN '''

# def p_Output(p):
    # ''' Output : WRITE
    # | WRITELN LPAREN IdentList RPAREN '''

### -------------------------------- ###

def p_error(p):
    print ("Syntax Error at Line: %d, Pos: %d"%(p.lineno,p.lexpos))
    # Add formatters later here, to fetch line number and position

def printpretty(filename):
    output = [i for i in reverse_output[::-1]]
    # print(output)

    f = open(filename+".html","w+") 
    f.write("<!DOCTYPE HTML> \n <html> \n \t<head> \n \t\t<title>Rightmost Derivation</title> \n \t<head> \n \t<body>\n")

    runningRule = ""
    pre = ""
    post = ""
    
    for rule in output:
        if runningRule != "":
            for i in range(len(runningRule),-1,-1):
                if runningRule[i:i+len(str(rule[0]))] == str(rule[0]):
                    break
            pre = runningRule[0:i]
            post = runningRule[i+len(str(rule[0])):]

        #print "############## " + str(type(pre)) + " ############## " + str(type(runningRule)) + " ###############"
        f.write("\t\t" + "<br>" + pre + "<b>" + str(rule[0]) + "</b>" + post + ' >>>>>> ')
        runningRule = pre
        f.write(pre + "<u>")
        for symbol in rule[1:]:
            if str(type(symbol)) == "<class 'ply.lex.LexToken'>":
                runningRule = runningRule + symbol.value + ' '
                f.write(symbol.value + ' ')
            else:
                runningRule = runningRule + str(symbol) + ' '
                f.write(str(symbol) + ' ')
                
        runningRule = runningRule + post
        f.write("</u>" + post + "\n")
    f.write("\t</body> \n </html>") 

parser = yacc.yacc()

symTab = SymTable()
tac = ThreeAddrCode()

# Do the things that we want to here
inputfile = open(sys.argv[1],'r').read()
yacc.parse(inputfile, debug = 1)

tac.display_code()
