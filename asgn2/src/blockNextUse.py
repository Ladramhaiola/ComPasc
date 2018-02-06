import os
import sys

class blockNextUse:

    def __init__(self,SymTable,code):
        '''
        Sets the next use information for a given block of code
        '''
        self.nextUse = []                                            # Ordered list storing a lineNextUse object for every line
        self.SymTable = SymTable
        self.code = code

    def getMaxUse(self):

        maxNext = 0
        maxSymbolRegister = None;
        
        for i in range(len(self.code)):

            tempSymbolRegister = self.nextUse[i].getMaxNextUse()
            temp = tempMaxSymbolRegister.nextUse

            if temp != float("inf") and temp > maxNext:
                maxNext = temp
                maxSymbolRegister = tempSymbolRegister

        return maxSymbolRegister
        
        
    def main():
        '''
        Reading the code from last line to first line and updating the next use information
        '''
        for i in range(len(code),0,-1):

            codeLine = code[i]
            self.nextUse[i] = lineNextUse(self.SymTable,codeLine);
            self.nextUse[i].assign()
