# Linnumber where dealloc is called:  9
#===========================================
#----------------- x86 code ----------------
#===========================================
.extern printf 

.data 

.formatINT : 
 .string "%d\n" 

.formatINT_INP : 
 .string "%d" 

.globl a
a: .long 4
.globl arr
arr: .fill 400
.globl b
b: .long 4
.globl d
d: .long 4

.text
	.global main
	main:
# Linenumber IR: 1
# Linenumber IR: 2
# message: Did not replace
		movl $0,%eax
# message: Did not replace
		movl $2,%eax
# Linenumber IR: 3
# message: Did not replace
		movl $0,%ebx
# message: Did not replace
		movl $7,%ebx
# Linenumber IR: 4
		addl %ebx, %eax
# Linenumber IR: 5
# message: Did not replace
		movl $0,%ecx
# message: Did not replace
		movl $3,%ecx
# Linenumber IR: 6
# loc_op1: ecx
		movl %ecx,b
		movl a,%ecx
		movl b,%edx
		movl %edx,arr(,%ecx,4)
# Linenumber IR: 7
# loc: ecx
		movl %ecx,a
		movl a,%ebx
		movl arr(,%ebx,4), %ecx
# Linenumber IR: 8
		#printF starts here

		movl %ecx,d
		movl %edx,b
		movl $0, %eax
		movl d,%esi
		movl $.formatINT, %edi
		call printf
		movl d,%ecx
		movl b,%edx
		#printF ends here
# Linenumber IR: 9
#movToMem starts here
		movl %ecx,d
#movToMem ends here
#movToMem starts here
		movl %ebx,a
#movToMem ends here
		ret
#===========================================
