class CodeGenerator():
    '''
        Issues:
            Where to add each instruction to? Like how is the basic block interfacing happening?
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
        self.curr_func = ''
        self.varAllocate = varAllocate
        self.varAllocate.getBasicBlocks()
        self.varAllocate.iterateOverBlocks()
        self.code = threeAC.code

        # Register descriptor
        self.registerToSymbol = self.varAllocate.registerToSymbol
        # print ('ss' ,self.registerToSymbol['eax'])

        # Memory descriptor
        self.symbolToRegister = self.varAllocate.symbolToRegister # dict with key value pairs.
        # For a given register, we get a list, whos first element is the register, and second is the memory location


        # self.operator_list = ["unary","jmp","jtrue","jfalse","loadref","storeref","label","param","call","return","returnval"]

        # Operation list for 32 bit registers
        self.op32_dict = {"+":"add",
                        "-":"sub",
                        "*":"imul",
                        "/":"idiv",
                        "MOD":"mod",
                        "OR":"or",
                        "AND":"and",
                        "SHL":"shl",
                        "SHR":"shr",
                        "CMP":"cmp"}

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


    def StatementType (self, line):
        # binary arithmetic
        if (line[1] in self.op32_dict):
            if (self.RepresentsInt(line[3]) and self.RepresentsInt(line[4])):
                return ('BA_2C')
            elif (not self.RepresentsInt(line[3]) and self.RepresentsInt(line[4])):
                return ('BA_1C_R')
            elif (self.RepresentsInt(line[3]) and not self.RepresentsInt(line[4])):
                return ('BA_1C_L')
            else:
                return ('BA_V')


    def movToMem (self, reg, v):
        '''
        '''
        ascode = "mov " + "\%" + reg + "," + v + "(,1)" + "\n"
        return ascode

    def getFromMem (self, x):
        '''
        '''
        ascode = x + "(,1)"
        return ascode


    ### --------------------------- INDIVIDUAL ASSEMBLY INSTRUCTIONS -------------------- ###

    def handle_binary (self, lineno, op, lhs, op1, op2):
        '''
            
        '''
        line = self.code[lineno - 1]
        # print ('line = ' , line, 'lineno = ' , lineno)
        op = self.op32_dict[line[1]]
        # lineno, operator, lhs, op1, op2 = line
        statTyp = self.StatementType(line)

        blockIndex = self.varAllocate.line2Block(lineno)
        # handle cases a = a + b
        if (op1 == lhs):
            if (op1 != op2):
                flag = 0
                if self.symbolToRegister[op2] != "":
                    loc_op2 = self.symbolToRegister[op2]
                else:
                    loc_op2 = self.getFromMem(op2)
                    flag = 1
                loc_op1 = self.symbolToRegister[op1]
                if (loc_op1 != ""): # a in register
                    ascode = op + " " + loc_op2 + "," +  loc_op1 
                    self.asm_code['text'].append(ascode)
                    # b may be in memory or register; doesn't matter. just add it to a
                    return
                elif (flag == 0):
                    ascode = op + " " + loc_op2 + "," + getFromMem(op1)
                    self.asm_code['text'].append(ascode)
                    # a not in register, but b is in register. simply update a's value in memory
                    return
                # if a and b are both not in registers, they are handled below

        # GetReg gives a location L to perform Operation, L(loc) is a register (for this assignment)
        loc, msg = self.varAllocate.getReg(blockIndex, lineno)

        if op1 in self.symTab.table['Ident'].keys() and self.symbolToRegister[op1] != "":
            loc_op1 = self.symbolToRegister[op1] # Fetching register, which is prefered if it exists
        else:
            loc_op1 = self.getFromMem(op1)
        if op2 in self.symTab.table['Ident'].keys() and self.symbolToRegister[op2] != "":
            loc_op2 = self.symbolToRegister[op2]
        else:
            loc_op2 = self.getFromMem(op2)

        if (statTyp == 'BA_2C'):
            ascode =  op + " $" + op1 + "," + loc + "\n" + "add $" + op2 + "," + loc + "\n"
        elif (statTyp == 'BA_1C_R'):
            if (msg == "Replaced op1"):
                ascode = op + " $" + op2 + "," + loc + "\n"
            else:
                ascode = "mov " + loc_op1 + "," + loc + "\n" + op + " $" + op2 + "," + loc + "\n"
        elif (statTyp == 'BA_1C_L'):
            if (msg == "Replaced op2"):
                ascode = op + " $" + op1 + "," + loc + "\n"
            else:
                ascode = "mov " + loc_op2 + "," + loc + "\n" + op + " $" + op1 + "," + loc + "\n"
        else:
            if (op1 in self.symTab.table['Ident'].keys() and op2 in self.symTab.table['Ident'].keys() and self.symbolToRegister[op1] == "" and self.symbolToRegister[op2] == ""):
                ascode = "mov " + loc_op1 + "," + loc + "\n" + op + " " + loc_op2 + "," + loc + "\n"
            elif (msg == "Replaced op1"):
                ascode = op + " " + loc_op2 + "," + loc + "\n"
            elif (msg == "Replaced op2"):
                ascode = op + " " + loc_op1 + "," + loc + "\n"
            elif (msg == "Replaced nothing"):
                ascode = op + " " + loc_op1 + "," + getFromMem(lhs) + "\n" + op + " " + loc_op2 + "," + getFromMem(lhs) + "\n"
            else:
                MU_var = msg[msg.find(',')+1:]
                self.movToMem(loc,MU_var)
                if (MU_var == op1):
                    ascode = op + " " + loc_op2 + "," + loc_op1 + "\n"
                else:
                    ascode = "mov " + loc_op2 + "," + loc + "\n" + op + " " + loc_op1 + "," + loc + "\n"

        self.asm_code['text'].append(ascode)


        ### ------------ Update descriptors for L and LHS ------------ ###

        # For L, if it is a register
        Registers = ["eax","ebx","ecx","edx"]
        if loc in Registers:
            # print (self.registerToSymbol[loc])
            lhs_reg = self.symbolToRegister[lhs]
            if (lhs_reg != "" and loc != lhs_reg):
                self.varAllocate.unusedRegisters.append(lhs_reg)
                self.varAllocate.usedRegisters.remove(lhs_reg)
                self.registerToSymbol[lhs_reg] = ""
            self.registerToSymbol[loc] = lhs
            self.symbolToRegister[lhs] = loc                # if it is a register, update the first entry

        # If op1 and/or op2 have no next use, update descriptors to include this info. [?]


    # LIFE IS GOOD FROM HERE

    def handle_cmp (op1,op2,const1,const2):
        '''
            Still to handle it.
        '''
        return

    def handle_jump (self, op, const1):
        '''
            Handle all jumps.
            op has direct mapping with jumps in assembly
            const1 has the label to jumpto as a string
        '''
        self.asm_code[self.curr_func].append(op.lower() + " " + const1)

    def handle_label (self, lhs, op1, const1):
        '''
        args:
            lhs: FUNC/NONFUNC Label
            op1: if func label, then get from symboltable
            const1: if non func, then simply take this
        '''
        if lhs == 'FUNC':
            ascode = op1.name + ":"
        else:
            ascode = const1 + ":"
        self.asm_code[self.curr_func].append(ascode)

    def handle_funccall (self,op1):
        '''
        args:
            op1 is a symbol table entry.
        '''
        self.asm_code[self.curr_func].append('call ' + op1.name)

    def handle_param(self,op1):
        '''
        args:
            op1 is the symbol table entry for the object to push
        '''
        self.asm_code[self.curr_func].append('push %' + op1.name)

    def handle_return(self):
        '''
            Empty return
        '''
        self.asm_code[self.curr_func].append('ret')

    def handle_returnval(self,op1):
        '''
        Have to look how values are returned
        '''
        self.asm_code[self.curr_func].append('ret')




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

        for key in self.OrderedCode:

            # key, according to the function names
            self.function_change(key)

            for codeLine in self.OrderedCode[key]:
                lineno, op, lhs, op1, op2, const1, const2 = codeLine

                ln = int(lineno)

                # DONE HOPEFULLY
                if op in ["+","-","*","/","MOD","AND","OR","SHL","SHR"]:
                    self.handle_binary (ln, op, lhs, op1, op2, const1, const2)

                # Would need to refer to handle_binary for most part
                elif op == 'CMP':
                    self.handle_cmp (op1, op2, const1, const2)
                
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
        self.asm_code['data'].append('.data \n')
        for var in self.symTab.table['Ident']:
            conv = self.symTab.Lookup(var).type
            self.asm_code['data'].append(var + ": " + type_to_asm[conv] + " 0")


    def setup_all(self):
        '''
            integrate across all the major parts
        '''
        # self.asm_code += 'section .text\nglobal _start\n\n'
        self.setup_text()
        self.setup_data()

    def display_code(self):
        print ('===========================================')
        print ('----------------- x86 code ----------------')
        print ('===========================================')
        for key in self.asm_code.keys():
            for codeLine in self.asm_code[key]:
                print codeLine
        # print (self.asm_code['text'])
        print ('===========================================')
