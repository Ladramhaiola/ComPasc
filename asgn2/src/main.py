from SymTable import SymTable
from ThreeAddrCode import ThreeAddrCode
from codegen import CodeGenerator
from varAllocateRegister import varAllocateRegister
import sys

def reader (tacf): # 3-addr code file
	f = open (tacf).readlines()
	content = [x.strip() for x in f]
	content = [x.split(',') for x in content]
	for i in range (len(content)):
		content[i] = [x.strip() for x in content[i]]
		while (len(content[i]) != 5):
			content[i].append('')
	return content

def main():
	file = sys.argv[1]
	content = reader(file)

        # Construct the Symbol Table ?
	SymTab = SymTable()
	ac3 = ThreeAddrCode(SymTab)

        # add to 3AC structures
	ac3.addTo3AC(content)

	# print (ac3.display_code())
        # SymTab.PrintSymTable()

        # Register allocater and other auxiliaries
	regAlloc = varAllocateRegister(SymTab,ac3)

        # Codegen object
        codeGen = CodeGenerator(SymTab, ac3, regAlloc)
        codeGen.setup_all()
        codeGen.display_code()

if __name__ == '__main__':
	main()
