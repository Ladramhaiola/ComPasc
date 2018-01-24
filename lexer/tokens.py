#List of tokens used by Lexer, for tokenization
#taken from https://www.freepascal.org/docs-html/ref/refch1.html

tokens = {
    #Symbols and operators
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'EQUALS',
    'LANGLE',                                           #LEFT ANGLE BRACKET '<'
    'RANGLE',
    'LSQUARE',                                          #LEFT SQUARE BRACKET '['
    'RSQUARE',
    'DOT',
    'COMMA',
    'INVERTCOMMA',                                      # '\''     
    'INVERTDOUBLECOMMA',                                # '\"'
    'LPAREN',                                           #LEFT PARENTHESES '('
    'RPAREN',
    'COLON',
    'POWER',                                            # '^'
    'ATRATE',                                           # '@'
    'LCURLY',                                           # '{'
    'RCURLY',
    #'DOLLAR',                                          # will have to check whether to remove or keep these (DOLLAR and HASH)
    #'HASH',
    'AMPERSAND',
    'PERCENT',
    'DOUBLESTAR',                                       # used for calculating powers '**'
    #'CINPUT',                                          # '<<' used for input in C
    #'COUTPUT',                                         # '>>' probably this and the upper symbol are not to tbe used in pascal
    #'LRANGLE',                                         # '<>' again probably not used in our grammar
    'ASSIGNTO',                                         # ':=' (used in assignment statements)
    'LESSTHANEQUAL',                                    # '<='
    'GREATERTHANEQUAL',                                 # '>='
    'PLUSEQUAL',                                        # '+='
    'MINUSEQUAL',                                       # '-='
    'MULTIPLYEQUAL',                                    # '*='
    'DIVIDEEQUAL',                                      # '/='
    'COMMENTSTART',                                     # '(*'
    'COMMENTEND',                                       # '*)'
    'DOUBLESLASH',                                      # '//'  
    #Identifiers and constants
    'NUMBER',
    'CHAR',
    #'STRING'                                           # MAYBE NEEDED
    'UNDERSCORE',
    'ID',
    #Bases of numbers
    #'HEX',
    #'BINARY',
    #'DECIMAL'
}
