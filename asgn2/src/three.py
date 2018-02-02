import os
import sys

class ThreeAddrCode:
    '''
        Class holding the three address code, links with symbol table
    '''

    def __init__(self,symbol_table):
        '''

        '''
        self.code_list = []


    def display_code(self):
        '''

        '''

        print "========================================="
        print '      Displaying three-address-code      '
        print "========================================="

        for code in self.code_list:
            lineno, op, lhs, op1, op2 = code

            if op == '=':
                print lineno, '\t', lhs, '<-', op1
            if op == '+':
                print lineno, '\t', lhs, '<-', op1, op, op2
            if op == '-':
                print lineno, '\t', lhs, '<-', op1, op, op2
            if op == '*':
                print lineno, '\t', lhs, '<-', op1, op, op2
            if op == '/':
                print lineno, '\t', lhs, '<-', op1, op, op2
            if op == '**':
                print lineno, '\t', lhs, '<-', op1, op, op2
            if op == 'ret':
                print lineno, '\t', op
            if op == 'goto':
                # LHS holds the line number to go to
                print lineno, '\t', op, lhs
            if op == 'if':
                # LHS is the comparison condition
                print lineno, '\t', op, op1, lhs, op2
            if op == 'label':
                # LHS is function name
                print lineno, '\t', op, lhs

        print "========================================="
