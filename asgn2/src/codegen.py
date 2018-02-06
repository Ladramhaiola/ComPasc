
class codeGenerator():
    '''
        Issues:
            Transforming Labels
            Where to add each instruction to? Like how is the basic block interfacing happening?
    '''

    def __init__(self,symTab,threeAC):

        self.symTab = symTab
        self.threeAC = threeAC
        self.asm_code = ''

        # Memory descriptor
        self.memdescr = {}

        # Register descriptor
        self.regdescr = {}

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


    ### --------------------------- INDIVIDUAL ASSEMBLY INSTRUCTIONS -------------------- ###

    def handle_binary(self, lineno, op, lhs, op1, op2):
        '''
            Does this handle the case when op1 is constant ?
            For example a = a + 3?
        '''

        # GetReg gives a location L to perform Operation, L(loc) is a registor or memory location

        # Get descriptors for op1 and op2: loc_op1, loc_op2
        if loc_op1 != loc:
            self.code += "movb %" + loc_op1 + ", %" + loc + "\n"
        operation = self.op32_dict[op]
        self.code += operation + " %" + loc_op2 + ", %" + loc + "\n"

        # Update descriptors for L and LHS

        # If op1 and/or op2 have no next use, update descriptors to include this info. [?]

    def handle_jump(self,op1):
        self.code += "jmp " + op1.name

    def handle_jtrue(self,op1,op2):

    def handle_jfalse(self,op1,op2):

    def loadref(self):

    def storeref(self):


    def handle_funccall(self,op1):
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
        self.asm_code += '.data\n'

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
