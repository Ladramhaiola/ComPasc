import ThreeAddrCode as threeAC
import SymTable as symTab


class nextUse:

    def __init__(self,symTab,threeAC):

        self.nextUse = []
        self.basicBlocks = []
        self.symbolTable = symTab
        self.threeAddressCode = threeAC

    def setBasicBlocks(self):

        leader1 = 0
        for i in range(len(self.threeAddressCode.codeList)):

            if self.threeAddressCode.codeList[i].op == "goto":
                leader1 = self.threeAddressCode.codeList[i].lhs
                leader2 = i
                self.basicBlocks.append([leader1,leader2])
                leader1 = i+1
        
        if leader2 != len(self.threeAddressCode.codeList)-1:
            self.basicBlocks.append([leader1,leader2])


    def setNextUse(self):

        for i in range(len(self.threeAddressCode.codeList),0,-1):

            nextDict = {}                                            

            for sym in self.symbolTable:
                if sym == self.threeAddressCode.codeList[i].lhs:
                    nextDict[sym] = infinite
                elif sym in self.threeAddressCode.codeList[i].op:
                    nextDict[sym] = i
                else:
                    nextDict[sym] = null

            self.nextUse.append(nextDict)
