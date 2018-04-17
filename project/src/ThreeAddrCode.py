import os
import sys
# import SymTable as SymTab # Is it required ?

class ThreeAddrCode:
    '''
        Class holding the three address code, links with symbol table
    '''

    def __init__(self,symTab):
        '''
            args:
                symTable: symbol table constructed after parsing
        '''
        self.code = []
        self.jump_list = ["JMP","JL","JG","JGE","JLE","JNE","JE","JZ"]
        self.binary_list = ["+","-","*","/","MOD","OR","AND","SHL","SHR","CMP"]
        self.operator_list = ["UNARY","=","LOADREF","STOREREF","CALL","LABEL","PARAM","RETURN","RETRUNVAL","PRINT","SCAN"]
        # This is for stack handling of all local variables of a function
        self.tempToOffset = {}
        self.symTab = symTab

    def mapOffset(self):
        for scope in self.symTab.table.keys():
            offset = -4 # Begin at -4, as -4 is the base

            scope_entry = self.symTab.table[scope]
            func_name = scope_entry['Name']
            self.tempToOffset[func_name] = {}
            mapDick = self.tempToOffset[func_name]

            width = 0
            #print "Scope:",scope

            # First adding the local variables
            if func_name != 'main':
                for var in scope_entry['Ident'].keys():
                    if scope_entry['Ident'][var].parameter == False:
                        #print "Var in mapping, offset: ",var, offset
                        # First fetch the variables from the scope
                        mapDick[var] = offset
                        varEntry = self.symTab.Lookup(var, 'Ident')
                        varEntry.offset = offset

                        # Now upadate the offset
                        offset = offset - self.symTab.getWidth(var)
                        width = width + self.symTab.getWidth(var)

            # Now handling the temporaries.
            for temp in self.symTab.localVals[func_name]:
                #print "Temp in mapping, offset: ",temp, offset
                mapDick[temp] = offset
                offset = offset - 4 # temporaries are size 4
                width = width + 4

            # This is for keeping the stack size for a local function
            scope_entry['width'] = width


    def emit(self,op,lhs,op1,op2):
        '''
            Writes the proper 3AC code: removes strings from symbol table entries
        '''
        self.code.append([op,lhs,op1,op2])

    def addlineNumbers(self):

        for i,code in enumerate(self.code):

            #print (code)
            op, lhs, op1, op2 = code
            self.code[i] = [str(i+1)] + code
        
    def display_code(self):
        '''
            For pretty printing the 3AC code stored here
            WARNING: Still not complete yet. self.code won't work. Has objects refering to symbol table

            The point of this to finally emit all the code generated, in the way desired.
        '''
        
        for i, code in enumerate(self.code):

            #print (code)
            LineNumber, op, lhs, op1, op2 = code

            if type(lhs) != type(""):
                lhs = lhs.name

            if type(op1) != type(""):
                op1 = op1.name

            if type(op2) != type(""):
                op2 = op2.name
            
            print ("#" + LineNumber + ", " + op + ", " + lhs + ", " + op1 + ", " + op2)

