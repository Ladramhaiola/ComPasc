import pprint
import sys

class SymTable (object):
    '''
    Some changes made keeping in mind the link : https://www.tutorialspoint.com/compiler_design/compiler_design_symbol_table.htm 
    '''

    def __init__(self): # local variables can be inside functions and functions only

        # default values
        self.table = {
            'main': {
                'Name': 'main',
                'ParentScope' : None,
                'Type' : 'function', # This can be function or loop
                'ReturnType' : None,
                'Func' : {},
                'Ident' : {},
                'ReturnSet' : False
            }
        }
        self.currScope = 'main'
        self.tNo = -1
        self.lNo = -1
        self.scopeNo = -1

    def PrintSymTable(self):
        pprint.pprint(self.table)

    def GetCurrentScopeName(self):
        return self.currScope 

    def AddScope (self, name, Type):
        scopeName = self.newScopeName()
        temp_scope = {
            'Name': name,
            'ParentScope' : self.currScope,
            'Type' : Type, # Type of scope
            'ReturnType' : 'undefined', # default value
            'Func' : {},
            'Ident' : {},
            'ReturnSet': False
        }
        self.table[scopeName] = temp_scope
        self.currScope = scopeName

    def width(self,typ):

        if typ == 'INTEGER':
            return 4
        elif typ == 'CHAR':
            return 1
        else:
            return 0
        
    def getWidth(self, v):
        vEntry = self.Lookup(v,'Ident')
        if vEntry.params == '':
            return self.width(vEntry.typ)
        elif vEntry.cat == 'array':
            size = 1
            for Range in vEntry.params:
                size = size*(Range['end']-Range['start']+1)
            arrayType = vEntry.typ
            arrayEntry = self.Lookup(arrayType, 'Ident')
            if self.width(vEntry.typ) != 0:
                return self.width(vEntry.typ)*size
            else:
                return self.width(arrayEntry.typ)*size
        
    def Define(self, v, typ, cat, params = '', offset = ''):
        
        curr_scope = self.table[self.currScope]
        e = None

        if self.getScope(v) != self.currScope:
        # If the current scope is not same as the scope where this variable already exists

            if (cat == "VAR"):
                #print "Defining var: ",v
                if (v not in curr_scope['Ident']):
                    e = SymTableEntry (v, typ, 'variable', params, offset)
                    curr_scope['Ident'][v] = e
                else:
                    sys.exit(v + " is already initialised in this scope")
            elif (cat=="CONST"):
                #print "Defining constant: ",v
                if (v not in curr_scope['Ident']):
                    e = SymTableEntry (v, typ, 'constant', params, offset)
                    curr_scope['Ident'][v] = e
                else:
                    sys.exit(v + " is already initialised in this scope")
            elif (cat=="ARRAY"):
                #print "Defining array: ",v
                if (v not in curr_scope['Ident']):
                    e = SymTableEntry (v, typ, 'array', params, offset)
                    curr_scope['Ident'][v] = e
                else:
                    sys.exit(v + " is already initialised in this scope")
            elif (cat=="OBJECT"):
                if (v not in curr_scope['Ident']):
                    e = SymTableEntry (v, typ, 'object', params, offset)
                    curr_scope['Ident'][v] = e
                else:
                    sys.exit(v + " is already initialised in this scope")
            else:
                if (v not in curr_scope['Func']):
                    # If function, then: v - name, typ - return type, category = function
                    e = SymTableEntry (v, typ, 'function', params, offset)
                    curr_scope['Func'][v] = e
                else:
                    sys.exit(v + " is already initialised in this scope")

        else:
            sys.exit(v + " is already initialised in this scope")

            
        if e != None:
            return e.name
        else:
            return None


    def getScope(self, identifier, idFunc = 'Ident'):

        for scope in self.table.keys():
            if identifier in self.table[scope][idFunc].keys():
                return scope

        return None


    def Lookup(self, name, idFunc):

        scope = self.getScope(name, idFunc)

        if scope == None:
            return None
        else:
            return self.table[scope][idFunc][name]


    def endScope(self):
        self.currScope = self.table[self.currScope]['ParentScope']


    def getTemp(self):
        self.tNo += 1
        newTemp = "t" + str(self.tNo) 
        return newTemp


    def getLabel(self):
        self.lNo += 1
        newTemp = "l" + str(self.lNo) 
        return newTemp


    def newScopeName(self):
        self.scopeNo += 1
        newScope = "s" + str(self.scopeNo) 
        return newScope


class SymTableEntry(object):
    '''
    Create a symbol table entry
    '''
    def __init__(self, name, typ, category = "variable", params = '', offset = ''):
        self.name = name
        self.typ = typ # for var: int, char, double | for function: typ is return type
        self.cat = category # either variable, constant, function, class or object
        self.params = params # For function, this is a list of param types, for constant, this is value of the constant and for array this is the range of array rows and columns 
        self.num_params = len(self.params)
        self.assigned = False # This is for knowing whether a variable has been assigned before use or not (won't work for arrays)
        self.offset = offset
