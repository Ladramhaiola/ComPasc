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
		movl $0,%eax
		addl $2,%eax
		movl $0,%ebx
		addl $7,%ebx
		addl %ebx, %eax
		movl $0,%ecx
		addl $3,%ecx
		movl $0,%edx
		addl %eax,%edx
		addl %ecx,%edx
		movl $0,%ebx
		addl $9,%ebx
		movl %ecx,b
		addl $4,%ecx
		movl %ecx,f
		addl b,%ecx
		movl %eax,a
		movl $0, %eax 
		movl %ecx,%esi
		movl $.formatINT, %edi
		call printf
		movl a, %eax 

		movl %eax,a
		addl $1,%eax
		movl %eax,g
		movl $0, %eax 
		movl g,%esi
		movl $.formatINT, %edi
		call printf
		movl g, %eax 

		cmpl %eax, a
		jge foo
		movl %eax,g
		movl %ebx,d
		ret
	foo:
		movl $0,%ecx
		movl a,%ecx
		addl $2,%ecx

		movl $0, %eax 
		movl %ecx,%esi
		movl $.formatINT, %edi
		call printf
		ret
#===========================================
