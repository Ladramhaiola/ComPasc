import os
import sys
import SymTable as SymTab

class ThreeAddrCode:
    '''
        Class holding the three address code, links with symbol table
    '''

    def __init__(self,symbol_table):
        '''

        '''
        self.code = []


    def display_code(self):
        '''

        '''

        print ("=========================================")
        print ('      Displaying three-address-code      ')
        print ("=========================================")

        for code in self.code:
            lineno, op, op3, op1, op2 = code

            if op == '=':
                print (lineno, '\t', op3, '<-', op1)
            if op == '+':
                print (lineno, '\t', op3, '<-', op1, op, op2)
            if op == '-':
                print (lineno, '\t', op3, '<-', op1, op, op2)
            if op == '*':
                print (lineno, '\t', op3, '<-', op1, op, op2)
            if op == '/':
                print (lineno, '\t', op3, '<-', op1, op, op2)
            if op == '**':
                print (lineno, '\t', op3, '<-', op1, op, op2)
            if op == 'ret':
                print (lineno, '\t', op)
            if op == 'goto':
                # op3 holds the line number to go to
                print (lineno, '\t', op, op3)
            if op == 'if':
                # op3 is the comparison condition
                print (lineno, '\t', op, op1, op3, op2)
            if op == 'label':
                # op3 is function name
                print (lineno, '\t', op, op3)
        print ("=========================================")

    def addTo3AC (self, listCode):
        self.code = listCode