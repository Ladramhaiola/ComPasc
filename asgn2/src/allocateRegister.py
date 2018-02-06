import os
import sys

class allocateRegister:

    '''
    Called as soon as we enter a new basic block for allocation of registers 
    '''
    def __init__(self,SymTable,code): # code of basic block

        self.BNU = blockNextUse(SymTable,code);
        self.registers = [1,2,3,4,5,6,7,8]
        

    def rotate(l, n):
        return l[-n:] + l[:-n]

    def readCode (self):
    	self.nextUse.assign()
    	for i in range (0,len(self.code)):
    		NU = self.BNU.nextUse[i] # dictionary
    		# varAllocate Objects
    		lhs_curr = NU[lhs];
    		op1_curr = NU[op1];
    		op2_curr = NU[op2];
    		lineno, operator, lhs, op1, op2 = self.code[i]
    		lhs_sym_ob = self.SymTable.lookup(lhs)
    		op1_sym_ob = self.SymTable.lookup(op1)
    		op2_sym_ob = self.SymTable.lookup(op2)

