class Symbol (object):

    '''
    All of this has been done keeping in mind the link : https://www.tutorialspoint.com/compiler_design/compiler_design_symbol_table.htm
    '''
    def __init__(self):

        self.name = ""
        self.varOrFunc = ""
        self.varType = ""
        self.childSymTables = OrderedList();

    def assign(name, varOrFunc, typeOf):

        self.name = name
        self.varOrFunc = varOrFunc
        self.varType = typeOf
