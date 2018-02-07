import os
import sys

class varAllocateRegister:
    '''
    Class holding the register allocated and the next use information for a symbol in the given scope
    '''

    def __init__(self,SymTable,ThreeAddrCode):

        # nextUse maps every basic block to a list of  dictionaries containing next use info for every symbol in the block
        self.nextUse = []
        self.registerToSymbol = {}                                       # stores register to symbol mapping
        self.symbolToRegister = {}                                       # symbol to register mapping
        self.unusedRegisters = ["eax","ebx","ecx","edx"]
        self.usedRegisters = []
        self.SymTable = SymTable
        self.basicBlocks = []
        self.leaders = []                                                # This will determine the basic blocks 
        self.code = ThreeAddrCode.code

    def getBasicBlocks(self):
        '''
        Stores the basic blocks as [startline,endline] pairs in the list self.basicBlocks
        '''
        code = self.code
        self.leaders.append(1)                         # first statement is a leader
        for i in range(len(code)):
            codeLine = code[i]
            if codeLine[1] in ["jmp","je","jne","jz","jg","jl","jge","jle"]:
                self.leaders.append(codeLine[3])       # target of a jump is a leader
            self.leaders.append(code[i+1][3])          # statement next to a jump statement is a leader

        self.leaders = list(set(self.leaders))         # removes duplicates
        self.leaders.sort()

        for i in range(len(self.leaders)):
            self.basicBlocks.append([self.leaders[i],self.leaders[i+1]])

    def blockAssignNextUse(self,blockIndex):
        '''
        Reading the code from last line to first line in the given block and updating the next use information.
        '''
        self.nextUse[blockIndex] = [];              # This is a list of dictionaries. Each dictionary corresponds to a line
        block = self.basicBlocks[blockindex]
        start = block[0]
        end = block[1]
        code = self.code[start-1,end]               # Line numbers start from 1 but code list index starts from 0

        for i in range(len(code),-1,-1):

            lineDict = {}
            codeLine = code[i]

            lhs = codeLine[2]
            op1 = codeLine[3]
            op2 = codeLine[4]
        
            lhs_symbol = SymTable.lookup(lhs)
            op1_symbol = SymTable.lookup(op1)
            op2_symbol = SymTable.lookup(op2)
        
            if lhs_symbol.varfunc == "var":
                lineDict[lhs] = float("inf")
            if op1_symbol.varfunc == "var":
                lineDict[op1] = codeLine[0]
            if op2_symbol.varfunc == "var":
                lineDict[op2] = codeLine[0]

            self.nextUse[blockIndex].append(lineDict)                        # These dictionaries will be appended in reverse order of the line number

        self.nextUse[blockIndex] = list(reversed(self.nextUse[blockIndex]))

    def iterateOverBlocks(self):
        '''
        This is being used to calculate next use line numbers for variables in a basic block
        '''
        code = self.code

        for i,block in enumerate(self.basicBlocks):
            self.blockAssignNextUse(i)
    
    def getBlockMaxUse(self,blockIndex): # Mend this function; it should accept line number too
        '''
            This returns the symbol with the maximum value of next use in the given basic block
        '''
        blockMaxNext = 0
        blockMaxSymbol = ""
        blockNextUse = self.nextUse[blockIndex]                              # This is a list of dictionaries
        for i,lineNextUse in enumerate(blockNextUse):
            lineMaxSymbol = max(lineNextUse.iterkeys(), key=(lambda key: lineNextUse[key]))
            lineMaxNext = lineNextUse[lineMaxSymbol]
            if lineMaxNext > blockMaxNext:
                blockMaxNext = lineMaxNext
                blockMaxSymbol = lineMaxSymbol

        return blockMaxSymbol

    def movToMem (self, reg, v):
    	dataSection

    def getReg(self,blockIndex,line):
        '''
            Refer to slide 29, CodeGen.pdf for the cases
            WARNING: Still not returning anything ?
        '''
        reg = ""
        msg = ""
        codeLine = self.code[line]
        
        lhs = self.SymTable.lookup(codeLine[2]) # x
        op1 = self.SymTable.lookup(codeLine[3]) # y
        op2 = self.SymTable.lookup(codeLine[4]) # z

        # x = y OP z

        nextUseInBlock = self.nextUse[blockIndex][line - self.basicBlocks[blockIndex][0]]

        # float("inf") means that variable has no next use after that particular line in the block
        if ( op1.varfunc == "var" and self.symbolToRegister[op1.name] != "" and nextUseInBlock[op1.name] == float("inf") ):
            reg = self.symbolToRegister[op1.name]
            self.symbolToRegister[op1.name] = ""
            msg = "Replaced op1"
        elif ( op2.varfunc == "var" and self.symbolToRegister[op2.name] != "" and nextUseInBlock[op2.name] == float("inf") ):
            reg = self.symbolToRegister[op2.name]
            self.symbolToRegister[op2.name] = ""
            msg = "Replaced op2"
        elif ( len(self.unusedRegisters) > 0 ):
            reg = self.unusedRegisters[0]
            self.unusedRegisters.remove(reg)
            self.usedRegister.append(reg)
            msg = "Did not replace"
        elif (( lhs.varfunc == "var" and nextUseInBlock[lhs.name] != float("inf"))):
        	MU_var = getBlockMaxUse(blockIndex, line)
        	reg = self.symbolToRegister[MU_var.name]
        	self.movToMem (reg,MU_var)
        	msg = "Replaced NextUse"
        else:
        	msg = "Replaced Nothing"

        self.registerToSymbol[reg] = lhs.name
        self.symbolToRegister[lhs.name] = reg



        return (reg, msg)