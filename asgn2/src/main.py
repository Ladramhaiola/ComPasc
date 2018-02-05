import SymTable as SymTab
from ThreeAddrCode import ThreeAddrCode as Three
import sys

def reader (tacf): # 3-addr code file
	f = open (tacf).readlines()
	content = [x.strip() for x in f]
	content = [x.split(',') for x in content]
	return content

def main():
	file = sys.argv[1]
	content = reader(file)
	ac3 = Three(None)
	ac3.addTo3AC(content)	

if __name__ == '__main__':
	main()