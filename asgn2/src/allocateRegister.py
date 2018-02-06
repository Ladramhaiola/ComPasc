import os
import sys

class allocateRegister:

    '''
    Called as soon as we enter a new basic block for allocation of registers 
    '''
    def __init__(self,SymTable,code):

        self.nextUse = blockNextUse(SymTable,code);
        self.registers = [1,2,3,4,5,6,7,8]
        

    def rotate(l, n):
        return l[-n:] + l[:-n]

