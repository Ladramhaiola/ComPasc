import os
import sys

class lineNextUse:

    def __init__(self,SymTable,codeLine):
        '''
        This will update the next use according to the code line while reading from the bottom line to the first line in nextUse.py
        '''
        self.nextUse = OrderedDict();
        self.SymTable = SymTable
        self.codeLine = codeLine

    def getMaxNextUse(self):

        maxNext = 0
        maxSymbolRegister = None;
        lhsNext = self.nextUse[self.codeLine[2]].nextUse
        op1Next = self.nextUse[self.codeLine[3]].nextUse
        op2Next = self.nextUse[self.codeLine[4]].nextUse

        if lhsNext != float("inf") and lhsNext > maxNext:
            maxNext = lhsNext
            maxSymbolRegister = self.nextUse[lhs]

        if op1Next != float("inf") and op1Next > maxNext:
            maxNext = lhsNext
            maxSymbolRegister = self.nextUse[op1]

        if op2Next != float("inf") and op2Next > maxNext:
            maxNext = lhsNext
            maxSymbolRegister = self.nextUse[op2]

        return maxSymbolRegister

    def assign(self):

        lhs = self.codeLine[2]
        op1 = self.codeLine[3]
        op2 = self.codeLine[4]

        lhs_symbol = self.SymTable.get(lhs)
        op1_symbol = self.SymTable.get(op1)
        op2_symbol = self.SymTable.get(op2)

        self.nextUse[lhs] = varAllocateRegister(lhs_symbol,self.SymTable)
        self.nextUse[op1] = varAllocateRegister(op1_symbol,self.SymTable)
        self.nextUse[op2] = varAllocateRegister(op2_symbol,self.SymTable)

        if lhs_symbol.varOrFunc == "var":
            self.nextUse[lhs].assignNextUse(self.code[0],"left")
        if op1_symbol.varOrFunc == "var":
            self.nextUse[op1].assignNextUse(self.code[0],"right")
        if op2_symbol.varOrFunc == "var":
            self.nextUse[op2].assignNextUse(self.code[0],"right")
