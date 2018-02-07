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
        self.blocksToLabels = {}                                         # key value is the [startline,endline] for a block and value is the label name
        self.leaders = []                                                # This will determine the basic blocks 
        self.code = ThreeAddrCode.code

        for reg in self.unusedRegisters:
            self.registerToSymbol = ""
        for sym in self.SymTable.table['Ident'].keys():
            self.symbolToRegister[sym] = ""
        
    def labelToLine(self,labelName):
        '''
        This function hasn't been used yet
        '''
        for i in range(len(self.code)):
            if self.code[i][1] == "label" and self.code[i][3] == labelName:
                return self.code[i][0]

    def blockToLabel(self):
        '''
        Mapping every block to a label name in which that block is present
        '''

        for block in self.basicBlocks:
            self.blocksToLabels[block] = ""

        for index,block in enumerate(self.basicBlocks):

            if self.code[block[0]][1] == "label":
                labelName = self.code[block[0]][3]
                self.blocksToLabels[block] = labelName

            for j in range(index+1,len(self.basicBlocks)):                  # all blocks under the same label should get the same mapping
                block = self.basicBlocks[j]
                if self.code[block[0]][1] != "label":                                   
                    self.blocksToLabels[block] = labelName
                else:                                                        #break as soon as we get a new label name. This will be dealt with in the outer loop     
                    break
 
        for block in self.basicBlocks:
            if self.blocksToLabels[block] == "":
                self.blocksToLabels[block] = "Main"
        
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
        self.nextUse[blockIndex] = [];                                       # This is a list of dictionaries. Each dictionary corresponds to a line

        block = self.basicBlocks[blockindex]
        start = block[0]
        end = block[1]
        code = self.code[start-1,end]                                        # Line numbers start from 1 but code list index starts from 0

        prevLine = {}                                                        # Stores the next use info for the next line (next to the current line in the loop)
        symbols = self.SymTable.table['Ident'].keys()                        # This is the list of all symbols

        for sym in symbols:
            prevLine[sym] = float("inf")
        
        for i in range(len(code)-1,-1,-1):

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

            for sym in symbols:
                if sym not in [lhs,op1,op2]:
                    lineDict[sym] = prevLine[sym]                            # Rest of the symbols will get the next use info of the next line

            self.nextUse[blockIndex].append(lineDict)                        # These dictionaries will be appended in reverse order of the line number
            prevLine = lineDict                                              # We need this for updating the next use for every symbol
            
        self.nextUse[blockIndex] = list(reversed(self.nextUse[blockIndex]))

    def iterateOverBlocks(self):
        '''
        This is being used to calculate next use line numbers for variables in a basic block
        '''
        code = self.code

        for i,block in enumerate(self.basicBlocks):
            self.blockAssignNextUse(i)
    
    def getBlockMaxUse(self,blockIndex, linenumber):
        '''
       This returns the symbol with the maximum value of next use in the given basic block such that the symbol has been allocated a register
        '''

        blockMaxNext = 0
        blockMaxSymbol = ""

        blockNextUse = self.nextUse[blockIndex][linenumber]                              # This is a dictionary

        symbols = self.SymTable.table['Ident'].keys()

        for sym in symbols:
            if blockNextUse[sym] > blockMaxNext and self.symbolToRegister[sym] != "":     # Return only the symbol which is held in some register
                blockMaxNext = blockNextUse[sym]
                blockMaxSymbol = sym
        
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
        	reg = ""
        	msg = "Replaced Nothing"

        self.registerToSymbol[reg] = lhs.name
        self.symbolToRegister[lhs.name] = reg



        return (reg, msg)
