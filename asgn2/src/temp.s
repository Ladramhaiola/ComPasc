;===========================================
;----------------- x86 code ----------------
;===========================================
.section .data 

	a: .long 0
	: .long 0
	c: .long 0
	b: .long 0
	d: .long 0
	g: .long 0
	f: .long 0
.section .text
	.globl _start
	_start:
		add ebx,eax
		add $2,%eax
		add $0,%eax
		add $7,%ebx
		add $0,%ebx
		add $3,%ebx
		add $1,%ecx
		add $2,%ecx
		add %ecx,%ebx
		add $4,%edx
		add $5,%edx
		add $1,%eax
		add $3,%eax
		add %ecx,%eax
		mov %a(,1),%g(,1)
		add $1,%g(,1)
		jge foo
	foo:
		mov %a(,1),%ebx
		add $2,%ebx
		ret
;===========================================
