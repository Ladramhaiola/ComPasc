import pprint

class SymTable (object):
    '''
    SymbolTable built after parsing
    Some changes made keeping in mind the link : https://www.tutorialspoint.com/compiler_design/compiler_design_symbol_table.htm 
    '''

    def __init__(self): # local variables can be inside functions and functions only

        # default values
        self.table = {
            'Main': {
                'ParentScope' : None,
                'Type' : 'function', # This can be function or loop
                'ReturnType' : 'undefined',
                'Func' : {},
                'Ident' : {}
            }
        }
        self.currScope = 'Main'
        # add itself, at least! Index 0 has highest, 1 is inside 0, 2 is inside 1 ...
        # Current scope is always at index [-1]

    def PrintSymTable(self):
        pprint.pprint(self.table)

    def GetCurrentScopeName(self):
        return self.currScope 

    def AddScope (self, Type):
        scopeName = self.newScopeName
        temp_scope = {
            'ParentScope' : self.currScope,
            'Type' : Type, # Type of scope
            'ReturnType' : 'undefined', # default value
            'Func' : {},
            'Ident' : {},
        }
        self.table[scopeName] = temp_scope

    def Define(self, v, typ, varfunc):
        '''
            args:
                symbol: an object of class SymTable entry
        '''

        curr_scope = self.scopelist[-1]
        e = None
        if (varfunc == "var"):
            if (v not in curr_scope['Ident']):
                e = SymTableEntry (v, typ, "var")
                curr_scope['Ident'][v] = e
        else:
            if (v not in curr_scope['Func']):
                e = SymTableEntry (v, typ, "func")
                curr_scope['Func'][v] = e
        # else:
            # print ('Symbol already exists!')
        return e

    def getScope(self, identifier):
        scope = self.currScope
        while scope != None:
            if identifier in self.table[scope]['Ident']:
                return scope
            else:
                scope = self.table[scope]['ParentScope']

        return None
                
    def Lookup(self, identifier):
        scope = self.getScope(identifier)

        if scope == None:
            return False
        else:
            return True

    def endScope(self, scopeName):
        self.currScope = self.table[self.currScope]['ParentScope']

    def getTemp(self):
        self.tNo += 1
        newTemp = "t" + str(self.tNo) 
        return newTemp

    def newScopeName(self):
        self.scopeNo += 1
        newScope = "s" + str(self.scopeNo) 
        return newScope

class SymTableEntry(object):
    '''
    Create a symbol table entry
    '''
    def __init__(self,name,typ,varfunc = "var", memsize = 4):
        self.name = name
        self.varfunc = varfunc # either var, function, class or object
        self.typ = typ # for var: int, char, double | for function: typ is return type
        self.memsize = memsize # number of elements in the array
