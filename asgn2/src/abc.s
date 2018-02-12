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
.globl d
d: .long 0
.globl g
g: .long 0
.globl f
f: .long 0

.text
	.global main
	main:
#This is for line number 1
		movl $0,%eax
		addl $2,%eax
#This is for line number 2
		movl $0,%ebx
		addl $7,%ebx
#This is for line number 3
		addl %ebx, %eax
#This is for line number 4
		movl $0,%ecx
		addl $3,%ecx
#This is for line number 5
		movl $0,%edx
		addl %eax,%edx
		addl %ecx,%edx
#This is for line number 6
		movl $0,%ebx
		addl $9,%ebx
#This is for line number 7
		movl %ecx,b

		addl $4,%ecx
#This is for line number 8
		movl %ecx,f

		addl b,%ecx
#printF starts here
		movl %eax,a
		movl $0, %eax 
		movl %ecx,%esi
		movl $.formatINT, %edi
		call printf
		movl a, %eax
#printF ends here
#This is for line number 10

		movl %eax,%ecx
		addl $1,%ecx
#printF starts here
		movl %eax,a
		movl $0, %eax 
		movl a,%esi
		movl $.formatINT, %edi
		call printf
		movl a, %eax
#printF ends here
		cmpl %ecx, %eax
		jge foo
		movl %eax,a
		movl %edx,c
		ret
	foo:
#This is for line number 16
		movl $0,%eax
		movl a,%eax
		addl $5,%eax
#printF starts here
		movl %eax,g
		movl $0, %eax 
		movl g,%esi
		movl $.formatINT, %edi
		call printf
		movl g, %eax
#printF ends here
		ret
#===========================================
