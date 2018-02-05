class SymTable (object):
    '''
    SymbolTable built after parsing
    symbol class is currently missing
    '''

    def __init__(self):
        self._symbols = OrderedDict();

    def define(self, symbol):
        '''
            Need to store the symbol object in the table
        '''
        print('Define: %s' % symbol)
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        '''
            Returns the symbol object, where the object holds all kind of info for this variable/ident.
            Args:
                name(String): name of the variable looking for
        '''
        print('Lookup: %s' % name)
        symbol = self._symbols.get(name)
        return symbol
