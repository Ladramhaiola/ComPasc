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
            move to memory, and update the descriptors
        '''
        # print (v)
        ascode = "\t\tmovl " + "%" + reg + "," + v
        self.symbolToRegister[v] = ''
        self.registerToSymbol[reg] = ''
        self.asm_code[self.curr_func].append(ascode)

    def getFromMem (self, x):
        '''
        '''
        ascode = x
        return ascode

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
        # line = self.code[lineno - 1]
        # print ('line = ' , line, 'lineno = ' , lineno)
        
        op = self.op32_dict[operation] # add/sub/idiv
        # lineno, operator, lhs, op1, op2 = line

        statTyp = self.StatementType(operation,op1,op2,const1,const2)
        # print (statTyp)

        blockIndex = self.varAllocate.line2Block(lineno)

        # #For debugging
        # self.asm_code[self.curr_func].append("#This is for line number %d"%(lineno))

        # Have assigned loc_op1 and loc_op2 above to aid in handling the case for lhs == op1
        # We use Loc_op1 for printing inside ascode and loc_op1 for accessing the data structures. This helps in removing the specificity in print statements
        if op1 != None:
            if self.symbolToRegister[op1.name] != "":
                loc_op1 = self.symbolToRegister[op1.name] # Fetching register, which is prefered if it exists
                Loc_op1 = "%" + loc_op1
            else:
                loc_op1 = self.getFromMem(op1.name)
                Loc_op1 = loc_op1


        if op2 != None:
            if self.symbolToRegister[op2.name] != "":
                loc_op2 = self.symbolToRegister[op2.name] 
                Loc_op2 = '%' + loc_op2 
            else:
                loc_op2 = self.getFromMem(op2.name)
                Loc_op2 = loc_op2

        # handle cases a = a + b  (cases like a = a + 1 will be handled in BA_1CR)
        if (op1 == lhs and op2 != None):

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

        # Done this after getting loc_op1 and loc_op2 for preventing redundant movl operations  
        if (loc in self.Registers and self.registerToSymbol[loc] != "" and lhs.name != self.registerToSymbol[loc]):

            s_code = '\t\tmovl ' + Loc + "," + self.registerToSymbol[loc]
            self.symbolToRegister[self.registerToSymbol[loc]] = ""
            self.asm_code[self.curr_func].append(s_code)

        ascode = ''

        # This needs to be done for every such case nonetheless
        if (msg == "Did not replace"):
            l_code = "\t\tmovl $0," + Loc
            # Setting setNewLine is required whenever we enter a line into code
            self.asm_code[self.curr_func].append(l_code)

        if (statTyp == 'BA_2C'):

            # This is an optimization
            n = self.optOP(operation,int(const1),int(const2))
            ascode += "\t\t" + op + " $" + str(n) + "," + Loc

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

                    if (self.registerToSymbol[loc] != "" and op1.name != self.registerToSymbol[loc]):
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

        self.asm_code[self.curr_func].append(ascode)


        ### ------------ Update descriptors for L and LHS ------------ ###

        if loc in self.Registers:
            lhs_reg = self.symbolToRegister[lhs.name]
            if (lhs_reg != "" and loc != lhs_reg):
                self.varAllocate.unusedRegisters.append(lhs_reg)
                self.varAllocate.usedRegisters.remove(lhs_reg)
                self.registerToSymbol[lhs_reg] = ""
            self.registerToSymbol[loc] = lhs.name
            self.symbolToRegister[lhs.name] = loc                # if it is a register, update the first entry

        # If op1 and/or op2 have no next use, update descriptors to include this info. [?]

    def printF (self, x, typ):
        #self.asm_code[self.curr_func].append('#printF starts here')
        v = self.registerToSymbol['eax']
        if (v == ''):
            ascode = ''
        else:
            ascode = "\t\tmovl " + "%eax" + "," + v
        flag = 1
        if x == v:
            flag = 0
        if (x in self.symbolToRegister.keys() and self.symbolToRegister[x] != "" and flag == 1):
            x = '%' + self.symbolToRegister[x] 

        # central code 
        ascode += "\t\tmovl $0, %eax"
        ascode += "\n\t\tmovl " + x + ",%esi"
        ascode += "\n\t\tmovl $.formatINT, %edi"
        ascode += "\n\t\tcall printf" 

        # restore mapping when variable did not have a symbol in the first place
        if (v != ''):
            ascode += "\n\t\tmovl " + v + ", %eax" 
            self.registerToSymbol['eax'] = v
            self.symbolToRegister[v] = 'eax'
        self.asm_code[self.curr_func].append(ascode)
        #self.asm_code[self.curr_func].append('#printF ends here')
        # self.asm_code[self.curr_func].append('' + self.registerToSymbol)
        # print (self.registerToSymbol)

    def handle_print (self, lineno, op1, const1):
        if (op1 != None):
            self.printF(op1.name, 'int')
        else:
            self.printF('$'+const1, 'int')

    def handle_input (self, lineno, op1):

        self.asm_code[self.curr_func].append('#scanF starts here')
        # central code 
   	# ascode += "\n\t\tpush %ebp"
        ascode += "\t\tmovl $0, %eax"
        ascode += "\n\t\tmovl " + x + ",%esi"
        ascode += "\n\t\tmovl $.formatINT, %edi"
        ascode += "\n\t\tcall scanf" 
        # ascode += "\n\t\tpop %ebp"

        self.asm_code[self.curr_func].append(ascode)
        self.asm_code[self.curr_func].append('#scanF ends here')

    def handle_cmp (self, lineno, op1, op2, const1, const2):
        '''
            const1 and const2 are strings
            op1 and op2 are SymbolTable objects
            two are definitely useless for a instruction
        '''
        if op1 != None:
            if self.symbolToRegister[op1.name] != "":
                loc_op1 = self.symbolToRegister[op1.name] # Fetching register, which is prefered if it exists
                Loc_op1 = '%' + loc_op1
            else:
                loc_op1 = self.getFromMem(op1.name)
                Loc_op1 = loc_op1

        if op2 != None:
            if self.symbolToRegister[op2.name] != "":
                loc_op2 = self.symbolToRegister[op2.name]
                Loc_op2 = '%' + loc_op2
            else:
                loc_op2 = self.getFromMem(op2.name)
                Loc_op2 = loc_op2

        if op1 == None and op2 == None:
            ascode = "\t\tcmpl $" + const1 + ",$ " + const2
        elif op1 == None and op2 != None:
            ascode = "\t\tcmpl $" + const1 + ",% " + loc_op2
        elif op1 != None and op2 == None:
            ascode = "\t\tcmpl " + Loc_op1 + ",$ " + const2
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


    def handle_return(self,op1):
        '''
            Currently moving the variable to be returned to the eax register, and updating the descriptors
        '''
        if op1 != None and op1 != '':
            # Clear EAX before putting the return value
            self.movToMem('eax',self.registerToSymbol['eax'])

            # Move the actual value to eax
            self.asm_code[self.curr_func].append('\t\tmovl ' + op1.name + ',%eax')

            # Register descriptor update
            self.registerToSymbol['eax'] = op1.name

            # memvariable update
            self.symbolToRegister[op1.name] = 'eax'

            self.asm_code[self.curr_func].append('\t\tret')
        else:
            # print ('tati')
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

        self.asm_code['text'].append('\n.text\n\t.global main\n\tmain:')

        for key in self.functionBlocks.keys():

            # key, according to the function names
            # print key
            self.function_change(key)

            start, end = self.functionBlocks[key]

            for i in range(start-1,end):
                # i is the index into self.code

                lineno, op, lhs, op1, op2, const1, const2 = self.code[i]
                # print lhs.name

                ln = int(lineno)

                # DONE HOPEFULLY
                if op in ["+","-","*","/","MOD","AND","OR","SHL","SHR"]:
                    self.handle_binary (ln, op, lhs, op1, op2, const1, const2)
                    # pass

                # Would need to refer to handle_binary for most part
                elif op == 'CMP':
                    self.handle_cmp (ln, op1, op2, const1, const2)
                
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
                    self.handle_return (op1)

                elif op == 'LOADREF':
                    self.handle_loadref ()

                elif op == 'STOREREF':
                    self.handle_storeref ()

                elif op == 'PRINT':
                    self.handle_print (ln,op1,const1)


                blockIndex =  self.varAllocate.line2Block(ln)

                # deallocate all registers at the end of each basic block
                if (ln == self.varAllocate.basicBlocks[blockIndex][1]):
                    self.deallocRegs()

                # print (self.registerToSymbol)
                # print (self.symbolToRegister)


    def setup_data(self):
        '''
            data section
        '''
        type_to_asm = {'int':".long",'float':''}
        self.asm_code['data'] = []
        self.asm_code['data'].append('.extern printf \n')
        self.asm_code['data'].append('.data \n')
        self.asm_code['data'].append('.formatINT : \n .string \"%d\\n\" \n')
        for var in self.symTab.table['Ident']:
            conv = self.symTab.Lookup(var).typ
            self.asm_code['data'].append(".globl " + var + "\n" + var + ": " + type_to_asm[conv] + " 0")


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

        for key in self.asm_code.keys():
            if key!= 'data':
                for codeLine in self.asm_code[key]:
                    print codeLine
        # print (self.asm_code['text'])
        print ('#===========================================')
