# The core lexer program. Uses PLY

import ply.lex as lex
from tokens import *
from reserved_tokens import *


# def build(debug=True):
'''
builds and returns the lexer object according to specifications.
NOTE: We don't require regex for reserved tokens as we first use the regex for identifier and match in the reserved dict
'''
    
# Should we use tokens for +- or literals?
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LANGLE = r'<' 
t_RANGLE = r'>'
t_LSQUARE = r'\[' # verify regex
t_RSQUARE = r'\]'
t_DOT = r'\.'
t_COMMA = r','
t_INVERTCOMMA = r'\''
t_INVERTDOUBLECOMMA = r'"'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGNTO = r':='                         #Instead of recognizing this, the lexer is reading ':=' as ':'+'='
t_COLON = r'\:'
t_SEMICOLON = r';'
t_POWER = r'\^'
t_ATRATE = r'@'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_AMPERSAND = r'&'
t_PERCENT = r'%'
t_DOUBLESTAR = r'\*\*'
t_LEQ = r'<='
t_GEQ = r'>='
t_PLUSEQ = r'\+='
t_MINUSEQ = r'-='
t_MULEQ = r'\*='
t_DIVEQ = r'/='
t_COMSTART = r'\(\*'
t_COMEND = r'\*\)'
t_DOUBLESLASH = r'//'
t_UNDERSCORE = r'_'


def t_ID(t):
    r'[A-Za-z](_?[A-Za-z0-9])*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)                                    #We can change the int to hex if required
    return t

def t_CHAR(t):
    r'["\'][A-Za-z0-9]["\']'
    if t.value[0] == '"':
        t.value = t.value.split('"')[1]
    else:
        t.value = t.value.split('\'')[1]
    return t

def t_STRING(t):
    r'["\'].+["\']'
    if t.value[0] == '"':
        t.value = t.value.split('"')[1]
    else:
        t.value = t.value.split('\'')[1]
    return t

### Following is borrowed from PLY tutorial

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
    # A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
    
# Error handling rule
def t_error(t):
    print("Line: [%d] Illegal character '%s'" % t.lineno,t.value)
    t.lexer.skip(1)
    
    # Build and return the lexer
    # if debug:
    #     return lex.lex(debug=1)
    # else
    #     return lex.lex()
    
lexer = lex.lex()

data = "PROGRAM Greeting;\nVAR MyMessage: STRING;\nBEGINMyMessage := 'Hello world!';\nWRITELN(MyMessage);\nEND."           

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print tok

