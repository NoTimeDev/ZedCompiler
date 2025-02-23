# ┌---------------------------------┐
# |   Zura Syntax by TheDevConnor   |
# |   assembly by Soviet Pancakes   |
# └---------------------------------┘
# 
# What's New: Memory allocated / freed

# Everything beyond this point was generated automatically by the Zura compiler.
.att_syntax
.text
.globl _start
_start:
  call main
  xorq %rdi, %rdi
  movq $60, %rax
  syscall

.type main, @function
.globl main

main:
	.cfi_startproc
	pushq %rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq %rsp, %rbp
	.cfi_def_cfa_register 6
	# Variable declaration for 'x'
	movq $9, -8(%rbp)
	# End of variable declaration for 'x'
	# Variable declaration for 'y'
	movq $8, -16(%rbp)
	# End of variable declaration for 'y'
	# Retrieve identifier: 'y' located at -16(%rbp)
	movq -16(%rbp), %rbx
	# Retrieve identifier: 'x' located at -8(%rbp)
	movq -8(%rbp), %rax
	add %rbx, %rax
	movq %rax, %rdi
	movq $60, %rax
	syscall # SYS_EXIT
	popq %rbp
	ret
	.cfi_endproc
.size main, .-main
	
