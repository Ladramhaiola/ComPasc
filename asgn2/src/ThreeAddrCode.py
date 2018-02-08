import os
import sys
# import SymTable as SymTab # Is it required ?

class ThreeAddrCode:
    '''
        Class holding the three address code, links with symbol table
    '''

    def __init__(self, symTable):
        '''
            args:
                symTable: symbol table constructed after parsing
        '''
        self.code = []
        self.symTable = symTable
        self.operator_list = ["unary","=","+","-","*","/","MOD","OR","AND","LEQ","SHL","SHR","<",">","<=",">=","CMP","JUMP","JGE","JTRUE","JFALSE","LOADREF","STOREREF","CALL","LABEL","param","RETURN","RETRUNVAL","PRINT"]

    def RepresentsInt(self,s):
        try: 
            int(s)
            return True
        except ValueError:
            return False

    def symTabOp (self, x):
        xEntry = None
        if (self.RepresentsInt(x) == True):
            return None
        if (x != ''):
            xEntry = self.symTable.Lookup(x)
        if (xEntry == None):
            xEntry = self.symTable.Define(x, 'int', 'var')
        return xEntry

    def addTo3AC (self, listCode):
        '''
            We need to refer to the symbol table objects, which holds variable objects for scope resolutions
            Args:
                listcode element: Format: LineNumber, Operation, Left Hand Side, Operand 1, Operand 2
                LineNumber, Operation are never NULL/None
        '''
        # Assignment translates to addition with 0

        for codeLine in listCode:

            temp = [None] * 5 # 3 AC rep
            lineno, operator, lhs, op1, op2 = codeLine

            temp.append(lineno) # Storing line number
            temp.append(operator) # Store the kind of instruction, or operator. Look at README

            if operator not in self.operator_list:
                print (codeLine)
                raise Exception('Operator Not Defined')

            
            temp[2] = self.symTabOp (lhs) 
            temp[3] = self.symTabOp (op1)
            temp[4] = self.symTabOp (op2)
            
            self.code.append([lineno, operator, lhs, op1, op2]) # Storing it to the global code store


    def display_code(self):
        '''
            For pretty printing the 3AC code stored here
            WARNING: Still not complete yet. self.code won't work. has objects refering to symbol table
        '''

        print ("=========================================")
        print ('      Displaying three-address-code      ')
        print ("=========================================")

        for code in self.code:
            # print (code)
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

