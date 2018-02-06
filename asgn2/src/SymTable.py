class SymTable (object):
    '''
    SymbolTable built after parsing
    Some changes made keeping in mind the link : https://www.tutorialspoint.com/compiler_design/compiler_design_symbol_table.htm 
    '''

    def __init__(self):

        self.parent = None; 
        self._symbols = OrderedDict();

    def define(self, symbol):
        '''
            args:
                symbol: an object of class SymTable entry
        '''
        print('Define: %s' % symbol.name)
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        '''
            Returns the symbol object, where the object holds all kind of info for this variable/ident.
            Args:
                name(String): name of the variable looking for
            returns:
                SymTableEntry object
        '''
        print('Lookup: %s' % name)
        symbol = self._symbols.get(name)
        return symbol

class SymTableEntry(object):
    '''

    '''
        def __init__(self,name,varfunc = "var",typ,size):
            self.name = name
            self.varfunc = varfunc # either var or function
            self.typ = typ # for var: int, char, double | for function: typ is return type
            self.size = size

