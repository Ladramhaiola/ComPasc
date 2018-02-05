import os
import sys
import SymTable as SymTab

class ThreeAddrCode:
    '''
        Class holding the three address code, links with symbol table
    '''

    def __init__(self,symbol_table):
        '''
            Currrently houses a 3 AC list as list of lists
            Each list has the quadruple we require
        '''
        self.code = []

    def addTo3AC (self, listCode):
        self.code = listCode

    def display_code(self):
        '''
            For pretty printing the 3AC code stored here
            WARNING: Still not complete yet
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

