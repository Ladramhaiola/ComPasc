class CodeGenerator():
    '''
        Args:
            symTab: Symbol Table formed in main.py
            threeAC: Three AC code formed in main.py
            varAllocate: the varAllocate object from main.py
    '''

    def __init__(self,symTab,threeAC,varAllocate,fBlocks):

        self.symTab = symTab
        self.threeAC = threeAC
        self.asm_code = {'text':[],
                         'data':[]}
        self.curr_func = ''
        self.varAllocate = varAllocate
        self.varAllocate.getBasicBlocks()
        self.varAllocate.iterateOverBlocks()
        self.functionBlocks = fBlocks
        self.code = threeAC.code

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


    def deallocRegs (self):
        for reg in self.varAllocate.usedRegisters:
            v = self.registerToSymbol[reg]
            self.movToMem(reg,v)
            self.varAllocate.usedRegisters.remove(reg)
            self.varAllocate.unusedRegisters.append(reg)
            self.registerToSymbol[reg] = ""
            self.symbolToRegister[v] = ""


    def RepresentsInt(self,s):
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
            if (op1 == None) and (op2 == None):
                return ('BA_2C')
            elif (op1 != None) and (op2 == None):
                return ('BA_1C_R')
            else:
                return ('BA_V')


    def movToMem (self, reg, v):
        '''
        '''
        ascode = "\t\tmov " + "\%" + reg + "," + v + "(,1)" + "\n"
        return ascode

    def getFromMem (self, x):
        '''
        '''
        ascode = x + "(,1)"
        return ascode


    ### --------------------------- INDIVIDUAL ASSEMBLY INSTRUCTIONS -------------------- ###

    def handle_binary (self, lineno, operation, lhs, op1, op2, const1, const2):
        '''
            
        '''
        # line = self.code[lineno - 1]
        # print ('line = ' , line, 'lineno = ' , lineno)

        op = self.op32_dict[operation] # add/sub/idiv
        # lineno, operator, lhs, op1, op2 = line

        statTyp = self.StatementType(operation,op1,op2,const1,const2)

        blockIndex = self.varAllocate.line2Block(lineno)
        # handle cases a = a + b
        if (op1 == lhs):
            flag = 0
            if self.symbolToRegister[op2.name] != "":
                loc_op2 = self.symbolToRegister[op2.name]
            else:
                loc_op2 = self.getFromMem(op2.name)
                flag = 1

            loc_op1 = self.symbolToRegister[op1.name]

            if (loc_op1 != ""): # a in register
                ascode = "\t\t" + op + " %" + loc_op2 + ",%" +  loc_op1 
                self.asm_code['text'].append(ascode)
                # b may be in memory or register; doesn't matter. just add it to a
                return

            elif (flag == 0):
                ascode = "\t\t" + op + " %" + loc_op2 + ",(" + getFromMem(op1.name) + ")"
                self.asm_code['text'].append(ascode)
                # a not in register, but b is in register. simply update a's value in memory
                return
                # if a and b are both not in registers, they are handled below

        ## NORMAL HANDLING ##

        # GetReg gives a location L to perform Operation, L(loc) is a register (for this assignment)
        loc, msg = self.varAllocate.getReg(blockIndex, lineno)

        if op1 != None:
            if self.symbolToRegister[op1.name] != "":
                loc_op1 = self.symbolToRegister[op1.name] # Fetching register, which is prefered if it exists
            else:
                loc_op1 = self.getFromMem(op1.name)

        if op2 != None:
            if self.symbolToRegister[op2.name] != "":
                loc_op2 = self.symbolToRegister[op2.name]
            else:
                loc_op2 = self.getFromMem(op2.name)

        if (statTyp == 'BA_2C'):
            ascode = "\t\t" + op + " $" + const1 + ",%" + loc + "\n\t\t" + op + " $" + const2 + ",%" + loc
        elif (statTyp == 'BA_1C_R'):
            if (msg == "Replaced op1"):
                ascode = "\t\t" + op + " $" + const2 + ",%" + loc
            else:
                ascode = "\t\tmov %" + loc_op1 + ",%" + loc + "\n\t\t" + op + " $" + const2 + ",%" + loc
        else:
            # Missing the case where both in memory, and loc is also mem location
            if (self.symbolToRegister[op1.name] == "" and self.symbolToRegister[op2.name] == ""):
                if loc in self.Registers:
                    ascode = "\t\tmov %" + loc_op1 + ",%" + loc + "\n" + op + " %" + loc_op2 + ",%" + loc
                else:
                    loc, msg = self.varAllocate.getReg(blockIndex, lineno, True)
            elif (msg == "Replaced op1"):
                ascode = "\t\t" + op + " %" + loc_op2 + ",%" + loc
            elif (msg == "Replaced op2"):
                ascode = "\t\t" + op + " %" + loc_op1 + ",%" + loc
            elif (msg == "Replaced nothing"):
                ascode = "\t\t" + op + " %" + loc_op1 + ",%" + getFromMem(lhs) + "\n" + op + " %" + loc_op2 + ",%" + getFromMem(lhs)
            else:
                # Spill it
                maxUse_var = msg[msg.find(',')+1:]

                # move to memory the var which was replaced
                self.movToMem(loc,maxUse_var)

                # Optimization (Hopefully)
                if (maxUse_var == op1.name):
                    ascode = "\t\t" + op + " %" + loc_op2 + ", %" + loc_op1   # loc = loc_op1
                elif (maxUse_var == op2.name):
                    ascode = "\t\t" + op + " %" + loc_op1 + ", %" + loc_op2   # loc = loc_op2
                else:
                    ascode = "\t\tmov %" + loc_op2 + ",%" + loc + "\n" + op + " %" + loc_op1 + ",%" + loc

        self.asm_code[self.curr_func].append(ascode)


        ### ------------ Update descriptors for L and LHS ------------ ###

        # For L, if it is a register
        if loc in self.Registers:
            # print (self.registerToSymbol[loc])
            lhs_reg = self.symbolToRegister[lhs.name]
            if (lhs_reg != "" and loc != lhs_reg):
                self.varAllocate.unusedRegisters.append(lhs_reg)
                self.varAllocate.usedRegisters.remove(lhs_reg)
                self.registerToSymbol[lhs_reg] = ""
            self.registerToSymbol[loc] = lhs.name
            self.symbolToRegister[lhs.name] = loc                # if it is a register, update the first entry

        # If op1 and/or op2 have no next use, update descriptors to include this info. [?]


    # LIFE IS GOOD FROM HERE

    def handle_cmp (lineno, op1, op2, const1, const2):
        '''
            Still to handle it
        '''
        if op1 != None:
            if self.symbolToRegister[op1.name] != "":
                loc_op1 = self.symbolToRegister[op1.name] # Fetching register, which is prefered if it exists
            else:
                loc_op1 = self.getFromMem(op1.name)

        if op2 != None:
            if self.symbolToRegister[op2.name] != "":
                loc_op2 = self.symbolToRegister[op2.name]
            else:
                loc_op2 = self.getFromMem(op2.name)

        if op1 == None and op2 == None:
            ascode = "\t\tcmpl $" + const1 + ",$ " + const2
        elif op1 == None and op2 != None:
            ascode = "\t\tcmpl $" + const1 + ",% " + loc_op2
        elif op1 != None and op2 == None:
            ascode = "\t\tcmpl %" + loc_op1 + ",$ " + const2
        else:
            if loc_op1 not in self.Registers and loc_op2 not in self.Registers:
                loc, msg = self.varAllocate.getReg(self.varAllocate.line2Block(lineno), lineno, True)
                ascode = "\t\tmovl %" + loc_op1 + ", %" + loc + "\n\t\tcmpl %" + loc + ", %" + loc_op2
            else:
                ascode = "\t\tcmpl %" + loc_op1 + ", %" + loc_op2

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
            ascode = "\t" + op1.name + ":"
        else:
            ascode = "\t" + const1 + ":"
        self.asm_code[self.curr_func].append(ascode)

    def handle_funccall (self,op1):
        '''
        args:
            op1 is a symbol table entry.
        '''
        self.asm_code[self.curr_func].append('\t\tcall ' + op1.name)

    def handle_param(self,op1):
        '''
        args:
            op1 is the symbol table entry for the object to push
        '''
        self.asm_code[self.curr_func].append('\t\tpush %' + op1.name)

    def handle_return(self):
        '''
            Empty return
        '''
        self.asm_code[self.curr_func].append('\t\tret')

    def handle_returnval(self,op1):
        '''
        Have to look how values are returned
        '''
        self.asm_code[self.curr_func].append('\t\tret')




    ### ---------------------------- AGGREGATORS ---------------------------------------- ###

    def function_change (self, func_name):
        '''
            If we get a basic block part which has different name than the current, add a key with that name
        '''
        self.asm_code[func_name] = []
        self.curr_func = func_name


    def setup_text(self):
        '''
            Text section
            Refer to 3AC_complete.md for exact 3 Abstract Code definitions
        '''

        # op1, op2 are symbol table objects

        self.asm_code['text'].append('.section .text\n\t.globl _start\n\t_start:')

        for key in self.functionBlocks.keys():

            # key, according to the function names
            # print key
            self.function_change(key)

            start, end = self.functionBlocks[key]

            for i in range(start-1,end):
                # i is the index into self.code
                # print self.code[i]

                lineno, op, lhs, op1, op2, const1, const2 = self.code[i]
                # print lhs.name

                ln = int(lineno)

                # DONE HOPEFULLY
                if op in ["+","-","*","/","MOD","AND","OR","SHL","SHR"]:
                    self.handle_binary (ln, op, lhs, op1, op2, const1, const2)
                    # pass

                # Would need to refer to handle_binary for most part
                elif op == 'CMP':
                    # self.handle_cmp (op1, op2, const1, const2)
                    pass
                
                # DONE HOPEFULLY
                elif op in self.jump_list:
                    self.handle_jump (op, const1)

                # DONE HOPEFULLY
                elif op == 'LABEL':
                    self.handle_label (lhs, op1, const1)

                # DONE HOPEFULLY
                elif op == 'CALL':
                    self.handle_funccall (op1)

                # DONE HOPEFULLY
                elif op == 'PARAM':
                    self.handle_param (op1)

                elif op == 'RETURN':
                    self.handle_return ()

                elif op == 'RETURNVAL':
                    self.handle_returnval (op1)

                elif op == 'LOADREF':
                    self.handle_loadref ()

                elif op == 'STOREREF':
                    self.handle_storeref ()


                blockIndex =  self.varAllocate.line2Block(ln)

                # deallocate all registers at the end of each basic block
                if (ln == self.varAllocate.basicBlocks[blockIndex][1]):
                    self.deallocRegs()

                # print (self.registerToSymbol)
                # print (self.symbolToRegister)


    def setup_data(self):
        '''
            data section
            FFT: Just pick stuff from symbol table? For now, that's okay I guess...
        '''
        type_to_asm = {'int':".long",'float':''}
        self.asm_code['data'] = []
        self.asm_code['data'].append('.section .data \n')
        for var in self.symTab.table['Ident']:
            conv = self.symTab.Lookup(var).typ
            self.asm_code['data'].append("\t" + var + ": " + type_to_asm[conv] + " 0")


    def setup_all(self):
        '''
            integrate across all the major parts
        '''
        # self.asm_code += 'section .text\nglobal _start\n\n'
        self.setup_text()
        self.setup_data()

    def display_code(self):
        # print (';===========================================')
        # print (';----------------- x86 code ----------------')
        # print (';===========================================')

        for codeline in self.asm_code['data']:
            print codeline

        for key in self.asm_code.keys():
            if key!= 'data':
                for codeLine in self.asm_code[key]:
                    print codeLine
        # print (self.asm_code['text'])
        # print (';===========================================')
