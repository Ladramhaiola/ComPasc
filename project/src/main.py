import ply.yacc as yacc
import ply.lex as lex
from tokens import *
from lexer import *
from SymTable import SymTable
from SymTable import SymTableEntry
from ThreeAddrCode import ThreeAddrCode
from codegen import CodeGenerator
from varAllocateRegister import varAllocateRegister
import collections
import sys
from parser import parse

jump_list = ["JMP","JL","JG","JGE","JLE","JNE","JE","JZ"]
binary_list = ["+","-","*","/","MOD","OR","AND","SHL","SHR","CMP"]
operator_list = ["UNARY","=","LOADREF","STOREREF","CALL","LABEL","PARAM","RETURN","RETRUNVAL","PRINT","SCAN"]

def representsNum(s):
        '''
        Checks if the given entry is a number entry.
        '''
        s = getName(s)
        try: 
            float(s)
            return True
        except ValueError:
            return False

def getName(symbol):

        if isinstance(symbol, SymTableEntry):
            return symbol.name
        else:
            return symbol
    
def modify3ACforCodegen(symTab,tac,listCode):

        newCode = []
        for codeLine in listCode:        

            temp = [None] * 7
            lineno, operator, lhs, op1, op2 = codeLine
            temp[0] = lineno
            temp[1] = operator

            if (operator == 'LABEL'):
                temp[2] = lhs
                if (lhs == 'FUNC'):
                    temp[3] = op1
                else:
                    temp[5] = op1
            elif (operator in jump_list):
                    temp[3] = op1
                    temp[5] = op1
            elif (operator in binary_list):
                temp[2] = lhs
                temp[3] = op1
                if representsNum(temp[3]):
                    temp[5] = op1
                temp[4] = op2
                if representsNum(temp[4]):
                    temp[6] = op2
            elif (operator == 'RETURN'):
                temp[3] = op1
                temp[4] = op2
            elif (operator == "PRINT"):
                temp[3] = op1
                if representsNum(temp[3]):
                    temp[5] = op1
            elif (operator == "SCAN"):
                temp[2] = lhs
            elif (operator == "LOADREF"): # x = a[i]
                temp[2] = lhs
                temp[3] = op1
                temp[4] = op2
                if representsNum(temp[4]):
                    temp[6] = op2
            elif (operator == "STOREREF"): # a[i] = x
                temp[2] = lhs
                temp[3] = op1
                if representsNum(temp[3]):
                    temp[5] = op1
                temp[4] = op2
                if representsNum(temp[4]):
                    temp[6] = op2

            newCode.append(temp) # Storing it to the global code store
        tac.code = newCode

def reader (tacf): # 3-addr code file
	f = open(tacf).readlines()
	content = [x.strip() for x in f]
	content = [x.split(',') for x in content]
	for i in range (len(content)):
		content[i] = [x.strip() for x in content[i]]
		while (len(content[i]) != 5):
			content[i].append('')
	return content

def divideToFunctions (ac3code):
	FB = {}
	flag = 0
        name = ''
	for i in range(len(ac3code)):
		codeline = ac3code[i]
		#print (codeline)
		if (codeline[1] == 'LABEL' and codeline[2] == 'FUNC'):
                        name = codeline[3]
			if (flag == 0):
				FB['main'] = [1,i]
				flag = 1
			for j in range (i,len(ac3code)):
				if (ac3code[j][1] == 'RETURN' and ac3code[j][4] == name):
					break
                        FB[name] = [i+1,j+1]
			i = j + 1
	if (flag == 0):
                # print ('Value of i',i)
		FB['main'] = [1,i+1]
	return FB

def main():

        inputfile = open(sys.argv[1],'r').read()
        symTab,tac = parse(inputfile)
        tac.addlineNumbers()
        print("\n#Displaying 3AC\n")
        tac.display_code()
        modify3ACforCodegen(symTab,tac,tac.code)

	FB = divideToFunctions(tac.code)
	regAlloc = varAllocateRegister(symTab,tac)

    	codeGen = CodeGenerator(symTab, tac, regAlloc, FB)
    	codeGen.setup_all()
    	codeGen.display_code()

if __name__ == '__main__':
	main()
