from SymTable import SymTableEntry
class CodeGenerator():
    '''
        Args:
            symTab: Symbol Table formed in main.py
            threeAC: Three AC code formed in main.py
            varAllocate: the varAllocate object from main.py
    '''

    def __init__(self,symTab,threeAC,varAllocate):

        self.symTab = symTab
        self.threeAC = threeAC
        self.asm_code = {'text':[],
                         'data':[]}
        self.curr_func = 'main'
        self.varAllocate = varAllocate
        self.varAllocate.getBasicBlocks()
        self.varAllocate.iterateOverBlocks()
        # self.functionBlocks = fBlocks
        self.code = threeAC.code
        self.symbols = self.varAllocate.symbols
        self.registers = ['eax','ebx','ecx','edx']
        
        # Register descriptor
        self.registerToSymbol = self.varAllocate.registerToSymbol
        # print ('ss' ,self.registerToSymbol['eax'])

        # Memory descriptor
        self.symbolToRegister = self.varAllocate.symbolToRegister # dict with key value pairs.
        # For a given register, we get a list, whos first element is the register, and second is the memory location


        # self.operator_list = ["unary","jmp","jtrue","jfalse","loadref","storeref","label","param","call","return","returnval"]
        self.Registers = ["eax","ebx","ecx","edx"]

        # Operation list for 32 bit registers
        self.op32_dict = {"+":"addl",
                        "-":"subl",
                        "*":"imull",
                        "/":"idivl",
                        "MOD":"mod",
                        "OR":"or",
                        "AND":"and",
                        "SHL":"shll",
                        "SHR":"shrl"
                         }

        self.jump_list = threeAC.jump_list

    def getName(self, symbol):

        if isinstance(symbol, SymTableEntry):
            return symbol.name
        else:
            return symbol
        
    def getRegister(self, symbol):

        if isinstance(symbol, SymTableEntry):
            return self.symbolToRegister[symbol.name]
        else:
            if symbol in self.symbolToRegister.keys():
                return self.symbolToRegister[symbol]
            else:
                return ""

    def checkVariable(self, symbol):
        
        symbolName = self.getName(symbol)
        if symbolName in self.symbols:
            return True
        else:
            return False
        
    def getLoc(self, symbol):

        symbolName = self.getName(symbol)
        symbolReg = self.getRegister(symbol)
        symbolOffsets = self.threeAC.tempToOffset[self.curr_func]
        print "symbolName: ",symbolName


        loc_op = "" # condition checks in varAllocate and codegen
        Loc_op = "" # this is the actual codegen loc

        if symbolReg != "":
            loc_op = symbolReg
            Loc_op =  "%" + symbolReg
        else:
            symbolEntry = self.symTab.Lookup(symbolName,'Ident')
            # print "SE retrieved: ",symbolEntry
            loc_op = symbolName
            if symbolEntry != None and symbolEntry.offset != '' :
                # print "Now we are going to get the offset"
                Loc_op = str(symbolEntry.offset) + '(%ebp)'
            elif symbolName in symbolOffsets.keys():
                Loc_op = str(symbolOffsets[symbolName]) + '(%ebp)'
                print "Loc_op inside temps: ",Loc_op
            else:
                # print "Or maybe not"
                Loc_op = symbolName

        return [loc_op,Loc_op]
        
    def deallocRegs (self):
        for reg in self.Registers:
            if self.registerToSymbol[reg] != '':
                v = self.registerToSymbol[reg]
                self.movToMem(reg,v)
                self.varAllocate.usedRegisters.remove(reg)
                self.varAllocate.unusedRegisters.append(reg)
       # print(self.registerToSymbol)
        

    def RepresentsInt(self,s):
        s = self.getName(s)
        try: 
            int(s)
            return True
        except ValueError:
            return False


    def StatementType (self, operation, op1, op2, const1, const2):
        '''
            no statements of type:
                a = 3 + b
                instead, we insist on b + 3
        '''
        # binary arithmetic
        if (operation in self.op32_dict):
            if self.RepresentsInt(op1) and self.RepresentsInt(op2):
                return ('BA_2C')
            elif not self.RepresentsInt(op1) and self.RepresentsInt(op2):
                return ('BA_1C_R')
            else:
                return ('BA_V')

    def newLocHandling(self, loc, Loc, symbol):

        if (loc in self.registers and self.registerToSymbol[loc] != "" and self.getName(symbol) != self.registerToSymbol[loc]):
            s_code = "" # store code
            self.asm_code[self.curr_func].append("# loc: " + loc)
            s_code = '\t\tmovl ' + Loc + "," + self.registerToSymbol[loc]
            self.symbolToRegister[self.registerToSymbol[loc]] = ""
            self.registerToSymbol[loc] = ''
            self.asm_code[self.curr_func].append(s_code)

    def updateRegEntry(self, symbol, loc):

        symbolName = self.getName(symbol)

        if self.checkVariable(symbol):
            symbol_reg = self.symbolToRegister[symbolName]
            if (symbol_reg != "" and loc != symbol_reg):
                self.varAllocate.unusedRegisters.append(symbol_reg)
                self.varAllocate.usedRegisters.remove(symbol_reg)
                self.registerToSymbol[symbol_reg] = ""
            self.registerToSymbol[loc] = symbolName
            self.symbolToRegister[symbolName] = loc
    
    def movToMem (self, reg, v):
        '''
            move to memory, and update the descriptors
        '''
        # print (v)
        self.asm_code[self.curr_func].append('#movToMem starts here')
        ascode = "\t\tmovl " + "%" + reg + "," + v
        self.symbolToRegister[v] = ''
        self.registerToSymbol[reg] = ''
        self.asm_code[self.curr_func].append(ascode)
        self.asm_code[self.curr_func].append('#movToMem ends here')

    def optOP (self, x, a, b):
        if (x == '+'): 
            z = a + b;
        elif (x == '-'):
            z = a - b;
        elif (x == '*'):
            z = a * b;
        else :
            if (b == 0):
                z = 0
            else:
                z = float(a) / b
        return int(z)

    ### --------------------------- INDIVIDUAL ASSEMBLY INSTRUCTIONS -------------------- ###

    def handle_binary (self, lineno, operation, lhs, op1, op2, const1, const2):
        '''
            
        '''
        
        op = self.op32_dict[operation] # add/sub/idiv
        # lineno, operator, lhs, op1, op2 = line

        statTyp = self.StatementType(operation,op1,op2,const1,const2)
        # print (statTyp)

        blockIndex = self.varAllocate.line2Block(lineno)
        
        # #For debugging
        # self.asm_code[self.curr_func].append("#This is for line number %d"%(lineno))

        # Have assigned loc_op1 and loc_op2 above to aid in handling the case for lhs == op1
        # We use Loc_op1 for printing inside ascode and loc_op1 for accessing the data structures. This helps in removing the specificity in print statements

        loc_op1, Loc_op1 = self.getLoc(op1)
        loc_op2, Loc_op2 = self.getLoc(op2)
        # print "# Loc_op1: ",str(lineno),Loc_op1
        # print "# Loc_op2: ",str(lineno),Loc_op2

        # handle cases a = a + b  (cases like a = a + 1 will be handled in BA_1CR)
        if (op1 == lhs and self.checkVariable(op2)):

            if (Loc_op1[0] == "%"): # a in register

                ascode = "\t\t" + op + " " + Loc_op2 + ", " +  Loc_op1 
                self.asm_code[self.curr_func].append(ascode)
                return

            elif (Loc_op1[0] != "%" and Loc_op2[0] == "%"):
                '''
                This is for 'a' in memory and 'b' in register (the case for both being in memory is handled below (with a redundant movl))
                '''
                ascode = "\t\t" + op + " " + Loc_op2 + "," + Loc_op1
                self.asm_code[self.curr_func].append(ascode)
                return
            
        ## NORMAL HANDLING ##
        s_code = "" # store code
        l_code = "" # load code

        # GetReg gives a location L to perform Operation, L(loc) is a register (for this assignment)
        loc, msg = self.varAllocate.getReg(blockIndex, lineno)

        # We'll use Loc for printing ascode and loc for accessing the data structures
        if loc in self.Registers:
            Loc = "%" + loc
        else:
            Loc = loc

        self.newLocHandling(loc, Loc, lhs)

        ascode = ''

        # This needs to be done for every such case nonetheless
        if (msg == "Did not replace"):
            self.asm_code[self.curr_func].append("# message: " + msg)
            l_code = "\t\tmovl $0," + Loc
            # Setting setNewLine is required whenever we enter a line into code
            self.asm_code[self.curr_func].append(l_code)
            
        if (statTyp == 'BA_2C'):

            # This is an optimization
            n = self.optOP(operation,int(const1),int(const2))
            ascode += "\t\tmovl $" + str(n) + "," + Loc

        elif (statTyp == 'BA_1C_R'):

            if (loc == loc_op1):
                ascode += "\n\t\t" + op + " $" + const2 + "," + Loc
            else:
                # The first instruction won't be allowed if both are memories, we should check for that
                ascode += "\t\tmovl " + Loc_op1 + "," + Loc + "\n\t\t" + op + " $" + const2 + "," + Loc
                
        else:

            # This should remove a lot of redundancies
            if (loc in self.Registers and loc == loc_op1):
                ascode += "\t\t" + op + " " + Loc_op2 + "," + Loc

            # Symmetric case    
            elif (loc in self.Registers and loc == loc_op2):
                ascode += "\t\t" + op + " " + Loc_op1 + "," + Loc
                '''    
                When both op1 and op2 are in memory. This will further be divided into 2 cases depending on the return value of getReg().
                We can check the condition for op1 being in memory by comparing the first character of Loc_op1 with '%' 
                (We are not looking at the symbolToRegister mapping for this purpose because that might be empty string even when op1 might be in the register) 
                '''
            elif (Loc_op1[0] != "%" and Loc_op2[0] != "%"):

                # When loc is a register, loc and loc_op1 cannot be equal since op1 is definitely in memory. Hence we keep the initial movl
                if loc in self.Registers:
                    ascode += "\n\t\tmovl " + Loc_op1 + "," + Loc + "\n\t\t" + op + " " + Loc_op2 + "," + Loc
                else:
                    # We will be moving op1 to the register in this part
                    # Haven't changed printing of ascode in this block according to Loc (would have leaded to added trouble)

                    # This will always give a register
                    loc, msg = self.varAllocate.getReg(blockIndex, lineno, True)

                    if (self.registerToSymbol[loc] != "" and self.getName(op1) != self.registerToSymbol[loc]):
                        s_code = '\n\t\tmovl ' + "%" + loc + "," + self.registerToSymbol[loc]
                        self.symbolToRegister[self.registerToSymbol[loc]] = ""
                        self.asm_code[self.curr_func].append(s_code)

                    ascode += "\n\t\tmovl " + Loc_op1 + ",%" + loc + "\n\t\t" + op + " " + Loc_op2 + ",%" + loc
            
            elif (msg == "Replaced nothing"):
                # If either one of the op1 or op2 are in memory then one of our operations will fail (So I'mskipping this instruction)
                ascode += "\n\t\t" + op + " " + Loc_op1 + "," + Loc + "\n\t\t" + op + " " + Loc_op2 + "," + Loc

            elif (msg == "Did not replace"):
                # There is unused register
                ascode += "\n\t\t" + op + " " + Loc_op1 + "," + Loc + "\n\t\t" + op + " " + Loc_op2 + "," + Loc

            else:
                ascode += "\n\t\tmovl " + Loc_op2 + "," + Loc + "\n\t\t" + op + " " + Loc_op1 + "," + Loc

        self.asm_code[self.curr_func].append("# message: " + msg)
        self.asm_code[self.curr_func].append(ascode)


        ### ------------ Update descriptors for L and LHS ------------ ###

        if loc in self.Registers:
            self.updateRegEntry(lhs, loc)

        # If op1 and/or op2 have no next use, update descriptors to include this info. [?]

    def handle_division(self, lineno, operation, lhs, op1, op2, const1, const2):
        '''
        Look at 'https://stackoverflow.com/questions/39658992/division-in-x86-assembly-gas' for the exact syntax used
        '''
        # These will be changed during the division
        changedRegisters = ['eax','edx']
        statTyp = self.StatementType("/", op1, op2, const1, const2)
        blockIndex = self.varAllocate.line2Block(lineno)
        
        s_code = ''

        for reg in changedRegisters:
            if self.registerToSymbol[reg] != "":
                s_code = "\t\tmovl %" + reg + "," + self.registerToSymbol[reg]
                self.asm_code[self.curr_func].append(s_code)
            
        loc_op1, Loc_op1 = self.getLoc(op1)
        loc_op2, Loc_op2 = self.getLoc(op2)
 
        # This is for storing the value in lhs finally
        loc, msg = self.varAllocate.getReg(blockIndex, lineno)

        # We'll use Loc for printing ascode and loc for accessing the data structures
        if loc in self.Registers:
            Loc = "%" + loc
        else:
            Loc = loc

        # Done this after getting loc_op1 and loc_op2 for preventing redundant movl operations  
        if (loc in self.Registers and self.registerToSymbol[loc] != "" and lhs.name != self.registerToSymbol[loc] and loc not in changedRegisters):

            s_code = '\t\tmovl ' + Loc + "," + self.registerToSymbol[loc]
            self.symbolToRegister[self.registerToSymbol[loc]] = ""
            self.asm_code[self.curr_func].append(s_code)

        ascode = ''
        l_code = ''

        # No need to do this here as we are ultimately going to move the value of ecx to loc
        # # This needs to be done for every such case nonetheless
        # if (msg == "Did not replace"):
        #     l_code = "\t\tmovl $0," + Loc
        #     # Setting setNewLine is required whenever we enter a line into code
        #     self.asm_code[self.curr_func].append(l_code)

        if(statTyp == 'BA_2C' or statTyp == 'BA_1C_R'):

            if self.registerToSymbol['ecx'] != '':
                self.movToMem('ecx',self.registerToSymbol['ecx'])
            
            if (statTyp == 'BA_2C'):

                ascode += "\t\tmovl $" + const1 + ", %eax"
                ascode += "\n\t\tcdq"
                ascode += "\n\t\tmovl $" + const2 + ", %ecx"
                ascode += "\n\t\tidivl %ecx"

                # After this the quotient is stored in eax and the remainder in edx
            
            elif (statTyp == 'BA_1C_R'):

                if loc_op1 != "eax":
                    l_code = "\t\tmovl " + Loc_op1 + ", %eax"
                    self.asm_code[self.curr_func].append(l_code)
                ascode += "\t\tcdq"
                ascode += "\n\t\tmovl $" + const2 + ", %ecx"
                ascode += "\n\t\tidivl %ecx"
            
        else:

            if loc_op1 != "eax":
                l_code = "\t\tmovl " + Loc_op1 + ", %eax"
                self.asm_code[self.curr_func].append(l_code)
            ascode += "\t\tcdq"
            ascode += "\n\t\tidivl " + Loc_op2

        # At this point, we have the quotient in eax and the remainder in edx

        if loc != "eax" and operation == "/":
            ascode += "\n\t\tmovl %eax," + Loc
        if loc != "edx" and operation == "MOD":
            ascode += "\n\t\tmovl %edx," + Loc

        self.asm_code[self.curr_func].append(ascode)

        # Reload the values in eax and edx according to the mapping (only if loc is not one of them)
        for reg in changedRegisters:
            if self.registerToSymbol[reg] != "" and reg!= loc:
                s_code = "\t\tmovl " + self.registerToSymbol[reg] + ",%" + reg
                self.asm_code[self.curr_func].append(s_code)
        
        # We can change the mapping for Loc and lhs
        if loc in self.Registers:
            self.updateRegEntry(lhs, loc)
        
    def printF (self, x, typ):
        
        changedRegisters = ['eax','ecx','edx']

        self.asm_code[self.curr_func].append('\t\t#printF starts here')
        ascode = ''

        #print(self.registerToSymbol)
        for i,reg in enumerate(changedRegisters):
        	v = self.registerToSymbol[reg]
	        if (v != ''):
	            ascode += "\n\t\tmovl " + "%" + reg + "," + v

        if self.symbolToRegister[x] != '':
            x = "%"+self.symbolToRegister[x]
            
        # central code 
        ascode += "\n\t\tmovl $0, %eax"
        ascode += "\n\t\tmovl " + x + ",%esi"
        ascode += "\n\t\tmovl $.formatINT, %edi"
        ascode += "\n\t\tcall printf" 

        # restore values in registers
        for i,reg in enumerate(changedRegisters):
        	v = self.registerToSymbol[reg]
        	if (v != ''):
        		ascode += "\n\t\tmovl " + v + ",%" + reg
        
        self.asm_code[self.curr_func].append(ascode)
        self.asm_code[self.curr_func].append('\t\t#printF ends here')

    def handle_print (self, lineno, op1, const1):

        ascode = ''
        
        if self.checkVariable(op1):
            self.printF(self.getName(op1), 'int')
        else:
            self.printF('$'+const1, 'int')

    def handle_input (self, lineno, lhs):

        self.asm_code[self.curr_func].append('#scanF starts here')

        v = self.registerToSymbol['eax']
        if (v == ''):
            ascode = ''
        else:
            ascode = "\t\tmovl " + "%eax" + "," + v


        # central code 
        # ascode += "\n\t\tpush %ebp"
        ascode += "\n\t\tmovl $0, %eax"
        ascode += "\n\t\tmovl $" + lhs.name + ",%esi"
        ascode += "\n\t\tmovl $.formatINT_INP, %edi"
        ascode += "\n\t\tcall scanf" 
        # ascode += "\n\t\tpop %ebp"

        if (v != ''):
            ascode += "\n\t\tmovl " + v + ", %eax" 
            self.registerToSymbol['eax'] = v
            self.symbolToRegister[v] = 'eax'

        self.asm_code[self.curr_func].append(ascode)
        self.asm_code[self.curr_func].append('#scanF ends here')

    def handle_cmp (self, lineno, op1, op2, const1, const2):
        '''
            const1 and const2 are strings
            op1 and op2 are SymbolTable objects
            two are definitely useless for a instruction
        '''
        loc_op1, Loc_op1 = self.getLoc(op1)
        loc_op2, Loc_op2 = self.getLoc(op2)
        
        if not self.checkVariable(op1) and not self.checkVariable(op2):
            ascode = "\t\tcmpl $" + const1 + ", $" + const2
        elif not self.checkVariable(op1) and self.checkVariable(op2):
            ascode = "\t\tcmpl $" + const1 + ", %" + loc_op2
        elif self.checkVariable(op1) and not self.checkVariable(op2):
            ascode = "\t\tcmpl $" + const2 + ", " + Loc_op1
        else:
            if loc_op1 not in self.Registers and loc_op2 not in self.Registers:
                loc, msg = self.varAllocate.getReg(self.varAllocate.line2Block(lineno), lineno, True)
                ascode = "\t\tmovl " + Loc_op1 + ", %" + loc + "\n\t\tcmpl %" + loc + ", " + Loc_op2
            else:
                ascode = "\t\tcmpl " + Loc_op1 + ", " + Loc_op2

        self.asm_code[self.curr_func].append(ascode)

    def handle_jump (self, op, const1):
        '''
            Handle all jumps.
            op has direct mapping with jumps in assembly
            const1 has the label to jumpto as a string
        '''
        self.asm_code[self.curr_func].append("\t\t" + op.lower() + " " + const1)

    def handle_label (self, lhs, op1, const1):
        '''
        args:
            lhs: FUNC/NONFUNC Label
            op1: if func label, then get from symboltable
            const1: if non func, then simply take this
        '''
        if lhs == 'FUNC':
            self.function_change(self.getName(op1))
        else:
            ascode = "\t" + const1 + ":"
            self.asm_code[self.curr_func].append(ascode)

    def handle_funccall (self,op1):
        '''
        args:
            op1 is a symbol table entry.
        '''
        self.asm_code[self.curr_func].append('\t\tcall ' + self.getName(op1))

    def handle_param(self,op1):
        '''
        args:
            op1 is the symbol table entry for the object to push
        '''
        if op1 == None:
            return 
        self.asm_code[self.curr_func].append('\t\tpush ' + self.getName(op1))


    def handle_return(self,op1):
        '''
            Currently moving the variable to be returned to the eax register, and updating the descriptors
        '''
        if self.checkVariable(op1) and op1 != '':
            # Clear EAX before putting the return value
            self.movToMem('eax',self.registerToSymbol['eax'])

            # Move the actual value to eax
            self.asm_code[self.curr_func].append('\t\tmovl ' + self.getName(op1) + ',%eax')

            # Register descriptor update
            self.registerToSymbol['eax'] = self.getName(op1)

            # memvariable update
            self.symbolToRegister[self.getName(op1)] = 'eax'

            self.asm_code[self.curr_func].append('\t\tret')
        else:
            # print ('tati')
            self.asm_code[self.curr_func].append('\t\tret')

        for scope in self.symTab.table.keys():
            if self.symTab.table[scope]['Name'] == self.curr_func:
                parent_scope = self.symTab.table[scope]['ParentScope']
                self.curr_func = self.symTab.table[parent_scope]['Name']
                break

    def handle_loadref (self,lineno, lhs, op1, op2, const2):
    	# op1.name is always avaiable

    	blockIndex = self.varAllocate.line2Block(lineno)
    	loc, msg = self.varAllocate.getReg(blockIndex, lineno, True)
        
        #self.registerToSymbol[self.symbolToRegister[self.getName(lhs)]] = ''
    	# We'll use Loc for printing ascode and loc for accessing the data structures
        Loc = "%" + loc

    	ascode = ''

        self.newLocHandling(loc, Loc, lhs)

        # We are checking if op2 is a symTableEntry instead we need to check if it's a variable
        if self.checkVariable(op2) and self.checkVariable(lhs) and lhs != op2:

            loc_op2, msg = self.varAllocate.getReg(blockIndex, lineno, True)
            Loc_op2 = "%" + loc_op2

            self.newLocHandling(loc_op2, Loc_op2, op2)

        else:
            
            loc_op2 = loc
            Loc_op2 = Loc

        if (self.checkVariable(op2)): # if array index is a variable

            ascode += '\t\tmovl ' + self.getName(op2) + ",%" + loc_op2
            self.registerToSymbol[loc_op2] = self.getName(op2)
            self.symbolToRegister[self.getName(op2)] = loc_op2
            ascode += '\n\t\tmovl ' + self.getName(op1) + '(,%' + loc_op2 + ",4), " + Loc

        else: # if array index is a constant, we still need to allocate a register for the index as per x86 syntax
    		ascode += '\t\tmovl %' + loc_op2 + ',' + self.registerToSymbol[loc_op2]
    		ascode += '\n\t\tmovl $' + const2 + ', %' + loc_op2
    		ascode += '\n\t\tmovl ' + self.getName(op1) + '(,%' + loc_op2 + ",4), " + Loc
    		ascode += '\n\t\tmovl ' + self.registerToSymbol[loc_op2] + ', %' + loc_op2

        self.updateRegEntry(op2, loc_op2)
        self.updateRegEntry(lhs, loc)

        self.asm_code[self.curr_func].append(ascode)

    def handle_storeref (self, lineno, lhs, op1, op2, const1, const2):

        blockIndex = self.varAllocate.line2Block(lineno)
        
        loc_op1 = ''
        loc_op2 = ''
        
        # We always require register to hold the value of i in a[i]
        loc_op1, msg = self.varAllocate.getReg(blockIndex, lineno, True)
        Loc_op1 = "%" + loc_op1

        self.newLocHandling(loc_op1, Loc_op1, op1)

        # loc_op2 is to store x in a[i] = x
        if self.checkVariable(op2) and self.checkVariable(op1) and op1 != op2:

            loc_op2, msg = self.varAllocate.getReg(blockIndex, lineno, True)
            Loc_op2 = "%" + loc_op2

            self.newLocHandling(loc_op2, Loc_op2, op2)

        else:
            
            loc_op2 = loc_op1
            Loc_op2 = Loc_op1

        ascode = ''
        s_code = "" # store code
        
        if(op1 != op2):
            if (not self.checkVariable(op1)):
                ascode += '\t\tmovl $' + const1 + ',' + Loc_op1
            elif (self.symbolToRegister[self.getName(op1)] != loc_op1):
                ascode += '\t\tmovl ' + self.getName(op1) + ',' + Loc_op1

        if (not self.checkVariable(op2)):
            ascode += '\n\t\tmovl $' + const2 + ',' + self.getName(lhs) + '(,' + Loc_op1 + ',4)'
        else:
            ascode += '\n\t\tmovl ' + self.getName(op2) + ',' + Loc_op2
            ascode += '\n\t\tmovl ' + Loc_op2 + ',' + self.getName(lhs) + '(,' + Loc_op1 + ',4)'
        
        self.updateRegEntry(op1, loc_op1)
        self.updateRegEntry(op2, loc_op2)

        self.asm_code[self.curr_func].append(ascode)


    ### ---------------------------- AGGREGATORS ---------------------------------------- ###

    def function_change (self, func_name):
        '''
            If we get a basic block part which has different name than the current, add a key with that name
        '''
        self.asm_code[func_name] = ["\t" + func_name + ":"]
        self.curr_func = func_name


    def setup_text(self):
        '''
            Text section
            Refer to 3AC_complete.md for exact 3 Abstract Code definitions
        '''

        # op1, op2 are symbol table objects

        self.asm_code['text'].append('\n.text\n\t.global main\n')
        
        self.function_change('main')
            
        start, end = 1,len(self.code)

        for i in range(start-1,end):
            # i is the index into self.code

            #print(self.registerToSymbol)
            #print(self.code[i])
            lineno, op, lhs, op1, op2, const1, const2 = self.code[i]
            # print "code[i]: ",self.code[i]
            # print lhs.name
            ln = int(lineno)

            # Find the blockIndex
            blockIndex = self.varAllocate.line2Block(ln)

            self.asm_code[self.curr_func].append("# Linenumber IR: " + str(ln))

            # DONE HOPEFULLY
            if op in ["+","-","*","AND","OR","SHL","SHR"]:
                self.handle_binary (ln, op, lhs, op1, op2, const1, const2)
                self.check_dealloc(ln,blockIndex)
                # pass

            elif op in ["/","MOD"]:
                self.handle_division(ln, op, lhs, op1, op2, const1, const2)
                
            # Would need to refer to handle_binary for most part
            elif op == 'CMP':
                self.handle_cmp (ln, op1, op2, const1, const2)
                self.check_dealloc(ln,blockIndex)
            
            # DONE HOPEFULLY
            elif op in self.jump_list:
                self.check_dealloc(ln,blockIndex)
                self.handle_jump (op, const1)

            # DONE HOPEFULLY
            elif op == 'LABEL':
                #print("#",self.code[i])
                self.check_dealloc(ln,blockIndex)
                self.handle_label (lhs, op1, const1)

            # DONE HOPEFULLY
            elif op == 'CALL':
                self.check_dealloc(ln,blockIndex)
                self.handle_funccall (op1)

            # DONE HOPEFULLY
            elif op == 'PARAM':
                self.handle_param (op1)
                self.check_dealloc(ln,blockIndex)

            elif op == 'RETURN':
                self.check_dealloc(ln,blockIndex)
                self.handle_return (op1)

            elif op == 'LOADREF':
                self.handle_loadref (ln,lhs, op1, op2, const2)

            elif op == 'STOREREF':
                self.handle_storeref (ln, lhs, op1, op2, const1, const2)

            elif op == 'PRINT':
                self.check_dealloc(ln,blockIndex)
                self.handle_print (ln,op1,const1)
                self.check_dealloc(ln,blockIndex)

            elif op == 'SCAN':
                self.handle_input(ln,lhs)


    def check_dealloc(self,ln,blockIndex):
        '''
            Checks and performs deallocation.
        '''
        if (ln == self.varAllocate.basicBlocks[blockIndex][1]):
            self.deallocRegs()


    def setup_data(self):
        '''
            data section
        '''
        type_to_asm = {'INTEGER':".long",'CHAR':'.string','float':'','int_arr':".fill"}
        self.asm_code['data'] = []
        self.asm_code['data'].append('.extern printf \n')
        self.asm_code['data'].append('.data \n')
        self.asm_code['data'].append('.formatINT : \n .string \"%d\\n\" \n')
        self.asm_code['data'].append('.formatINT_INP : \n .string \"%d\" \n')
        for scope in ['main']:
            for var in self.symTab.table[scope]['Ident']:
                varEntry = self.symTab.Lookup(var,'Ident')
                if varEntry.typ in type_to_asm.keys():
                    conv = varEntry.typ
                elif varEntry.cat == 'array':
                    arrayType = varEntry.typ
                    arrayEntry = self.symTab.Lookup(arrayType,'Ident')
                    conv = arrayEntry.typ
                elif varEntry.cat == 'object':
                    continue
                memsize = self.symTab.getWidth(var) # for arrays
                self.asm_code['data'].append(".globl " + var + "\n" + var + ": " + type_to_asm[conv] + " " + str(memsize))


    def setup_all(self):
        '''
            integrate across all the major parts
        '''
        # self.asm_code += 'section .text\nglobal _start\n\n'
        self.setup_text()
        self.setup_data()

    def display_code(self):
        print ('#===========================================')
        print ('#----------------- x86 code ----------------')
        print ('#===========================================')

        for codeline in self.asm_code['data']:
            print codeline

        # print self.asm_code.keys()
        for key in self.asm_code.keys():
            if key not in ['data']:
                # print "\t%s:" % key
                for codeLine in self.asm_code[key]:
                    print codeLine
        # print (self.asm_code['text'])
        print ('#===========================================')
