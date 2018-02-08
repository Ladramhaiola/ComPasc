.section .data 

	a: .long 0
	c: .long 0
	b: .long 0
	d: .long 0
	g: .long 0
	f: .long 0

.section .text
	.globl _start
	_start:
		addl %ebx,%eax
		addl $2,%eax
		addl $0,%eax
		addl $7,%ebx
		addl $0,%ebx
		addl $3,%ebx
		addl $1,%ecx
		addl $2,%ecx
		addl %ecx,%ebx
		addl $4,%edx
		addl $5,%edx
		addl $1,%eax
		addl $3,%eax
		addl %ecx,%eax
		jge foo
	foo:
		addl $2,%ebx
		ret
