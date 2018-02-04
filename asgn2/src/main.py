import SymTable as SymTab
import ThreeAddrCode as Three

def reader (tacf): # 3-addr code file
	f = open (tacf).readlines()
	content = [x.strip() for x in f]
	content = [x.split(',') for x in content]
	print (content)
	

reader("Code.3ac")