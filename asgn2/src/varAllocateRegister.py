import os
import sys
import math

class varAllocateRegister:
    '''
    Class holding the register allocated and the next use information for a symbol in the given scope
    '''

    def __init__(self,symbol,SymTable):

        self.symbol = symbol;
        self.lineno = -1;
        self.nextUse = float("inf");                                      # Represents a dead variable
        self.register = "";
        self.SymTable = SymTable;

    def assignNextUse(self,lineno,leftOrRight):
        '''
        This will be called when we will be processing the code from bottom to top for a given SymTable (scope)
        '''
        self.lineno = lineno

        if leftOrRight == "left":
            self.nextUse = float("inf")
        elif leftOrRight == "right":
            self.nextUse = lineno
        else:
            raise Exception("Not clear if symbol on left or right of expression");

    def getNextUse(self):
        '''
        This will be called when allocating registers, processing the code from top to down

        '''
        if self.register != "":
            return self.nextUse
        else:
            return float("inf")

    def allocateRegister(self,index):
        '''
        This will be called after we have decided to allocate the next free register index to the symbol
        '''
        if index not in (1,9):
            raise Exception("Register index not a valid one");
            
        self.register = "t%d"%(index)
