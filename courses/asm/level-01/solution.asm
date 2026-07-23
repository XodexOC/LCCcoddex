; solution.asm — exit(42)
section .text
    global _start

_start:
    mov rax, 60     ; exit
    mov rdi, 42     ; code = 42
    syscall
