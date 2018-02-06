import SymTable as SymTab
from ThreeAddrCode import ThreeAddrCode as Three
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
	ac3 = Three(None)
	ac3.addTo3AC(content)	
	print (ac3.code)

if __name__ == '__main__':
	main()