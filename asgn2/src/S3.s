# Linnumber where dealloc is called:  16
# Linnumber where dealloc is called:  17
# Linnumber where dealloc is called:  22
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
.globl c
c: .long 4
.globl b
b: .long 4
.globl d
d: .long 4
.globl g
g: .long 4
.globl f
f: .long 4
.globl x
x: .long 4

.text
	.global main
	main:
# Linenumber IR: 1
# message: Did not replace
		movl $0,%eax
# message: Did not replace
		movl $2,%eax
# Linenumber IR: 2
# message: Did not replace
		movl $0,%ebx
# message: Did not replace
		movl $7,%ebx
# Linenumber IR: 3
		addl %ebx, %eax
# Linenumber IR: 4
# message: Did not replace
		movl $0,%ecx
# message: Did not replace
		movl $3,%ecx
# Linenumber IR: 5
# message: Did not replace
		movl $0,%edx
# message: Did not replace

		addl %eax,%edx
		addl %ecx,%edx
# Linenumber IR: 6
# message: Did not replace
		movl $0,%ebx
# message: Did not replace
		movl $9,%ebx
# Linenumber IR: 7
		# loc: ecx
		movl %ecx,b
# message: Replaced NextUse , b
		movl $4,%ecx
# Linenumber IR: 8
		#printF starts here

		movl %eax,a
		movl %ecx,f
		movl %edx,c
		movl $0, %eax
		movl f,%esi
		movl $.formatINT, %edi
		call printf
		movl a,%eax
		movl f,%ecx
		movl c,%edx
		#printF ends here
# Linenumber IR: 9
		#printF starts here

		movl %eax,a
		movl %ecx,f
		movl %edx,c
		movl $0, %eax
		movl b,%esi
		movl $.formatINT, %edi
		call printf
		movl a,%eax
		movl f,%ecx
		movl c,%edx
		#printF ends here
# Linenumber IR: 10
		# loc: ecx
		movl %ecx,f
# message: Replaced op1
		addl b,%ecx
# Linenumber IR: 11
		#printF starts here

		movl %eax,a
		movl %ecx,g
		movl %edx,c
		movl $0, %eax
		movl g,%esi
		movl $.formatINT, %edi
		call printf
		movl a,%eax
		movl g,%ecx
		movl c,%edx
		#printF ends here
# Linenumber IR: 12
		# loc: eax
		movl %eax,a
# message: Replaced NextUse , a

		addl $1,%eax
# Linenumber IR: 13
		#printF starts here

		movl %eax,g
		movl %edx,c
		movl $0, %eax
		movl g,%esi
		movl $.formatINT, %edi
		call printf
		movl g,%eax
		movl c,%edx
		#printF ends here
# Linenumber IR: 14
#scanF starts here
		movl %eax,g
		movl $0, %eax
		movl $x,%esi
		movl $.formatINT_INP, %edi
		call scanf
		movl g, %eax
#scanF ends here
# Linenumber IR: 15
		cmpl %eax, a
# Linenumber IR: 16
#movToMem starts here
		movl %eax,g
#movToMem ends here
#movToMem starts here
		movl %ebx,d
#movToMem ends here
		jle foo
# Linenumber IR: 17
#movToMem starts here
		movl %edx,c
#movToMem ends here
		ret
# Linenumber IR: 18
	foo:
# Linenumber IR: 19
# message: Did not replace
		movl $0,%ecx
# message: Did not replace

		movl a,%ecx
		addl x,%ecx
# Linenumber IR: 20
		#printF starts here

		movl %ecx,g
		movl $0, %eax
		movl g,%esi
		movl $.formatINT, %edi
		call printf
		movl g,%ecx
		#printF ends here
# Linenumber IR: 21
		#printF starts here

		movl %ecx,g
		movl $0, %eax
		movl x,%esi
		movl $.formatINT, %edi
		call printf
		movl g,%ecx
		#printF ends here
# Linenumber IR: 22
#movToMem starts here
		movl %ecx,g
#movToMem ends here
		ret
#===========================================
