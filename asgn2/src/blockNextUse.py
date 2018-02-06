import os
import sys

class blockNextUse:

    def __init__(self,code):
        '''
        Sets the next use information for a given block of code
        '''
        self.nextUse = []                      
        self.code = code

    def getLineMaxUse(lineDict, codeLine):
        
        maxNext = 0
        maxSymbolRegister = None;

        lhsNext = lineDict[codeLine[2]].getNextUse()
        '''
        getNextUse() will check whether the symbol already has a register allocated to it, only then will it                                                                        return the next use else infinity
        '''
        op1Next = lineDict[codeLine[3]].getNextUse()
        op2Next = lineDict[codeLine[4]].getNextUse()

        if lhsNext != float("inf") and lhsNext > maxNext:
            maxNext = lhsNext
            maxSymbolRegister = lineDict[lhs]

        if op1Next != float("inf") and op1Next > maxNext:
            maxNext = lhsNext
            maxSymbolRegister = lineDict[op1]

        if op2Next != float("inf") and op2Next > maxNext:
            maxNext = lhsNext
            maxSymbolRegister = lineDict[op2]

        return maxSymbolRegister
        
    def getBlockMaxUse(self):
        '''
        Returns the varAllocateRegister object corresponding to the symbol having the maximum next use and having an already allocated register 
        '''
        maxNext = 0                                                     
        maxSymbolRegister = None;
        
        for i in range(len(self.code)):

            tempSymbolRegister = getLineMaxUse(self.nextUse[i], self.code[i])
            temp = tempSymbolRegister.nextUse

            if temp != float("inf") and temp > maxNext:
                maxNext = temp
                maxSymbolRegister = tempSymbolRegister

        return maxSymbolRegister

    def assignNextUse(codeLine):

    	lineDict = OrderedDict();

        lhs = codeLine[2]
        op1 = codeLine[3]
        op2 = codeLine[4]

        lhs_symbol = SymTable.lookup(lhs)
        op1_symbol = SymTable.lookup(op1)
        op2_symbol = SymTable.lookup(op2)

        lineDict[lhs] = varAllocateRegister(lhs_symbol)
        lineDict[op1] = varAllocateRegister(op1_symbol)
        lineDict[op2] = varAllocateRegister(op2_symbol)

        # set the next use line number for corresponding variable/symbol

        if lhs_symbol.varfunc == "var":
            lineDict[lhs].assignNextUse(codeLine[0],"left")
        if op1_symbol.varfunc == "var":
            lineDict[op1].assignNextUse(codeLine[0],"right")
        if op2_symbol.varfunc == "var":
            lineDict[op2].assignNextUse(codeLine[0],"right")

        return lineDict

    def assign():
        '''
        Reading the code from last line to first line and updating the next use information
        '''
        for i in range(len(self.code)-1,-1,-1):

            codeLine = self.code[i]
            lineDict = assignNextUse(codeLine)
            self.nextUse[i] = lineDict
