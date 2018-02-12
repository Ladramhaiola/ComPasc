#===========================================
#----------------- x86 code ----------------
#===========================================
.extern printf 

.data 

.formatINT : 
 .string "%d\n" 

.globl a
a: .long 0
.globl c
c: .long 0
.globl b
b: .long 0

.text
	.global main
	main:
#This is for line number 1
		movl $0,%eax
		addl $1,%eax
#This is for line number 2
		movl $0,%ebx
		addl $10,%ebx
#This is for line number 3
		movl $0,%ecx
		addl $1,%ecx
		movl %eax,a
		movl %ecx,c
	aa:
		cmpl %ebx, a
		jge loo
#printF starts here
		movl $0, %eax 
		movl a,%esi
		movl $.formatINT, %edi
		call printf
#printF ends here
#This is for line number 8
		movl $0,%edx
		movl a,%edx
		addl $1,%edx
		movl %edx, a
		jmp aa
	loo:
		ret
#===========================================
