import os
import sys
# import SymTable as SymTab # Is it required ?

class ThreeAddrCode:
    '''
        Class holding the three address code, links with symbol table
    '''

    def __init__(self,symTable):
        '''
            args:
                symTable: symbol table constructed after parsing
        '''
        self.code = []
        self.symTable = symTable
        self.operator_list = ["unary","+","-","*","/","MOD","OR","AND","SHL","SHR","<",">","<=",">=","jmp","jtrue","jfalse","loadref","storeref","label","param","call","return","returnval"]


    def addTo3AC (self, listCode):
        '''
            We need to refer to the symbol table objects, which holds variable objects for scope resolutions
            Args:
                listcode element: Format: LineNumber, Operation, Left Hand Side, Operand 1, Operand 2
                LineNumber, Operation are never NULL/None
        '''

        for codeLine in listCode:

            temp = [None] * 5 # 3 AC rep
            lineno, operator, lhs, op1, op2 = codeLine

            temp.append(lineno) # Storing line number
            temp.append(operator) # Store the kind of instruction, or operator. Look at README

            if operator not in self.operator_list:
                raise Exception('Operator Not Defined')

            if lhs != '':
                temp[2] = self.symTable.lookup(lhs)

            if op1 != '':
                temp[3] = self.symTable.lookup(op1)

            if op2 != '':
                temp[4] = self.symTable.lookup(op2)
            
            self.code.append(temp) # Storing it to the global code store


    def display_code(self):
        '''
            For pretty printing the 3AC code stored here
            WARNING: Still not complete yet. self.code won't work. has objects refering to symbol table
        '''

        print ("=========================================")
        print ('      Displaying three-address-code      ')
        print ("=========================================")

        for code in self.code:
            lineno, op, lhs, op1, op2 = code

            if op == '=':
                print (lineno, '\t', lhs, '<-', op1)
            if op == '+':
                print (lineno, '\t', lhs, '<-', op1, op, op2)
            if op == '-':
                print (lineno, '\t', lhs, '<-', op1, op, op2)
            if op == '*':
                print (lineno, '\t', lhs, '<-', op1, op, op2)
            if op == '/':
                print (lineno, '\t', lhs, '<-', op1, op, op2)
            if op == '**':
                print (lineno, '\t', lhs, '<-', op1, op, op2)
            if op == 'ret':
                print (lineno, '\t', op)
            if op == 'goto':
                # LHS holds the line number to go to
                print (lineno, '\t', op, lhs)
            if op == 'if':
                # LHS is the comparison condition
                print (lineno, '\t', op, op1, lhs, op2)
            if op == 'label':
                # LHS is function name
                print (lineno, '\t', op, lhs)
        print ("=========================================")

