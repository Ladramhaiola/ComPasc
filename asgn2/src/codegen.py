
class codeGenerator():
    '''
        Issues:
            Transforming Labels
            Where to add each instruction to? Like how is the basic block interfacing happening?
        Args:
            symTab: Symbol Table formed in main.py
            threeAC: Three AC code formed in main.py
            varAllocate: the varAllocate object from main.py
    '''

    def __init__(self,symTab,threeAC,varAllocate):

        self.symTab = symTab
        self.threeAC = threeAC
        self.asm_code = {}
        self.curr_func = '' # to know which function we are generating for right now
        self.varAllocate = varAllocate

        # Register descriptor
        self.registerToSymbol = self.varAllocate.registerToSymbol

        # Memory descriptor
        self.symbolToRegister = self.varAllocate.symbolToRegister # dict with key value pairs.
        # For a given register, we get a list, whos first element is the register, and second is the memory location


        # Redundant, but required now for referencing
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
                        "SHR":"shr"}

    def updateDescriptors(self):
        '''
            Update the descriptors as and when required by the algorithm
        '''



    ### --------------------------- INDIVIDUAL ASSEMBLY INSTRUCTIONS -------------------- ###

    def handle_binary (self, lineno, op, lhs, op1, op2):
        '''
            Does this handle the case when op1 is constant
            For example a = a + 3?
        '''

        # GetReg gives a location L to perform Operation, L(loc) is a registor or memory location
        loc = self.varAllocate.getReg() # Need to send things from here. What though?

        # Get descriptors for op1 and op2: loc_op1, loc_op2
        if self.symbolToRegister[op1.name][0] is not None:
            loc_op1 = self.symbolToRegister[op1.name][0] # Fetching register, which is prefered if it exists
        else:
            loc_op1 = self.symbolToRegister[op1.name][1] # if not available, get the memory location


        if self.symbolToRegister[op2.name][0] is not None:
            loc_op2 = self.symbolToRegister[op2.name][0] # Fetching register, which is prefered if it exists
        else:
            loc_op2 = self.symbolToRegister[op2.name][1] # if not available, get the memory location


        if loc_op1 != loc:
            self.code += "movb %" + loc_op1 + ", %" + loc + "\n"

        # Get the machine instruction
        operation = self.op32_dict[op]
        self.code += operation + " %" + loc_op2 + ", %" + loc + "\n"


        ### --- Update descriptors for L and LHS --- ###

        # For L, if it is a register
        if loc in self.validreglist:
            self.registerToSymbol[loc] = lhs.name
        # For lhs, and updating symbol to mem map
        if loc in self.validreglist:
            self.symbolToRegister[lhs.name][0] = loc # if it is a register, update the first entry
        else:
            self.symbolToRegister[lhs.name][1] = loc # if mem, the second entry


        # If op1 and/or op2 have no next use, update descriptors to include this info. [?]

    def handle_jump (self,op1):
        self.code += "jmp " + op1.name


    def handle_jtrue (self,op1,op2):

    def loadref (self):

    def storeref (self):


    def handle_funccall (self,op1):
        '''
        WARNING: Have to take into account context of function, or global.
        Not doing that currently.
        Essentially, self.code needs to be something more elaborate.
        '''
        self.code += 'call ' + op1.name + '\n'

    def handle_param(self,op1):
        self.code += 'push %' + op1.name + '\n'

    def handle_return(self):
        self.code += 'ret\n'

    def handle_returnval(self,op1):
        '''
        Have to look how values are returned
        '''
        self.code += '\nret'


    ### ---------------------------- AGGREGATORS ---------------------------------------- ###


    def setup_text(self):
        '''
            text section
            Refer to 3AC_complete.md for exact 3 Abstract Code definitions
        '''

        for codeLine in self.threeAC:
            lineno, op, lhs, op1, op2 = codeLine
            # lineno, op are NEVER NULL
            if op == 'unary':
                self.handle_unary()

            elif op == 'jmp':
                self.handle_jmp()

            elif op == 'jtrue':
                self.handle_jtrue()

            elif op == 'jfalse':
                self.handle_jfalse()

            elif op == 'loadref':
                self.handle_loadref()

            elif op == 'storeref':
                self.handle_storeref()

            elif op == 'label':
                self.handle_label()

            elif op == 'call':
                self.handle_funccall(op1)

            elif op == 'param':
                self.handle_param(op1)

            elif op = 'return':
                self.handle_return()

            elif op == 'returnval':
                self.handle_returnval(op1)

            else:
                handle_binary(lineno,op,lhs,op1,op2)


    def setup_data(self):
        '''
            data section
            FFT: Just pick stuff from symbol table?
        '''

        self.asm_code['data'] = []
        self.asm_code['data'] += '.data'

    def setup_all(self):
        '''
            integrate across all the major parts
        '''
        self.asm_code += 'section .text\nglobal _start\n\n'
        self.setup_text()
        self.setup_data()

    def display_code(self):
        print ';============================'
        print ';--------- x86 code ---------'
        print ';============================'
        print self.asm_code
        print ';============================'
        print ';============================'
