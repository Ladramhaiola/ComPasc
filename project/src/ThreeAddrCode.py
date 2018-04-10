import os
import sys
# import SymTable as SymTab # Is it required ?

class ThreeAddrCode:
    '''
        Class holding the three address code, links with symbol table
    '''

    def __init__(self):
        '''
            args:
                symTable: symbol table constructed after parsing
        '''
        self.code = []
        self.jump_list = ["JMP","JL","JG","JGE","JLE","JNE","JE","JZ"]
        self.binary_list = ["+","-","*","/","MOD","OR","AND","SHL","SHR","CMP"]
        self.operator_list = ["UNARY","=","LOADREF","STOREREF","CALL","LABEL","PARAM","RETURN","RETRUNVAL","PRINT","SCAN"]

    
    def emit(self,op,lhs,op1,op2):
        '''
            Writes the proper 3AC code: removes strings from symbol table entries
        '''
        self.code.append([op,lhs,op1,op2])

    def addlineNumbers(self):

        for i,code in enumerate(self.code):

            # print (code)
            op, lhs, op1, op2 = code
            self.code[i] = [str(i+1)] + code
        
    def display_code(self):
        '''
            For pretty printing the 3AC code stored here
            WARNING: Still not complete yet. self.code won't work. Has objects refering to symbol table

            The point of this to finally emit all the code generated, in the way desired.
        '''
        
        for code in enumerate(self.code):

            # print (code)
            LineNumber, op, lhs, op1, op2 = code

            if type(lhs) != type(""):
                lhs = lhs.name

            if type(op1) != type(""):
                op1 = op1.name

            if type(op2) != type(""):
                op2 = op2.name
            
            print (LineNumber + ", " + op + ", " + lhs + ", " + op1 + ", " + op2)

