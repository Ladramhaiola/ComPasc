import pprint
import sys

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
        self.tNo = -1
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


    def RepresentsNum(self,s):
        '''
        Checks if the given entry is a number entry.
        '''
        try: 
            float(s)
            return True
        except ValueError:
            return False

    def symTabOp (self, x, typ, varfunc = 'VAR'):
        '''
        args:
            x: If it is a constant, then return nothing as the object to be appended to 3Ac line.
               Else, define it in the table, and return the symbolTable entry

        '''
        xEntry = None
        if (self.RepresentsNum(x) == True):
            return None
        if (x != ''):
            xEntry = self.Lookup(x)
        if (xEntry == None and x != ''):
            xEntry = self.Define(x, typ, varfunc)
        return xEntry


    def Define(self, v, typ, varfunc):
        
        curr_scope = self.table[self.currScope]
        e = None

        if self.getScope(v) != self.currScope:

            if (varfunc == "VAR"):
                if (v not in curr_scope['Ident']):
                    e = SymTableEntry (v, typ, "VAR")
                    curr_scope['Ident'][v] = e
            else:
                if (v not in curr_scope['Func']):
                    e = SymTableEntry (v, typ, "FUNC")
                    curr_scope['Func'][v] = e

        else:
            sys.exit(v + "is already initialised in this scope")

        return e.name

    def getScope(self, identifier):
        scope = self.currScope
        while scope != None:
            if identifier in self.table[scope]['Ident'].keys():
                return scope
            else:
                scope = self.table[scope]['ParentScope']

        return None
                
    def Lookup(self, identifier):
        scope = self.getScope(identifier)

        if scope == None:
            return None
        else:
            return self.table[scope]['Ident'][identifier]

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
