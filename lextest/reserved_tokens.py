
# List of reserved tokens to be used by Lexer, for Tokenization
# Taken from http://wiki.freepascal.org/Reserved_words#Reserved_words_in_Object_Pascal

# Mappings are from soure language to the rep that we want in the compiler

reserved = {
    'and':'AND',
    'array':'ARRAY',
    'begin':'BEGIN',
    'break':'BREAK',
    'case':'CASE',
    'const':'CONSTANT',
    'constructor':'CONSTRUCT',
    'continue':'CONTINUE',
    'div':'DIV',
    'do':'DO',
    'else':'ELSE',
    'end':'END',
    'function':'FUNCTION',
    'if':'IF',
    'mod':'MOD',
    'nil':'NIL',
    'not':'NOT',
    'object':'OBJECT',
    'of':'OF',
    'or':'OR',
    'procedure':'PROCEDURE',
    'program':'PROGRAM',
    'repeat':'REPEAT',
    'shl':'SHL',
    'shr':'SHR',
    'string':'STRING',
    'then':'THEN',
    'to':'TO',
    'type':'TYPE',
    'until':'UNTIL',
    'var':'VAR',
    'while':'WHILE',
    'xor':'XOR',
    'as':'AS',
    'class':'CLASS',
    'inherited':'INHERITED',
    'self':'SELF',
    #adding absent tokens
    'int':'INT',
    'real':'REAL',
    'char':'CHAR',
    'double':'DOUBLE',
    'lambda':'LAMBDA',
    'public':'PUBLIC',
    'readln':'READLN',
    'writeln':'WRITELN',
    'read':'READ',
    'write':'WRITE'
    #POSSIBILITIES FOR ADDITION:
    #'absolute':''
}
