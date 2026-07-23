; solution.asm — регистры и mov
section .data
    msg db "Registers set", 10

section .text
    global _start

_start:
    mov rax, 10
    mov rbx, 20
    mov rcx, 30
    mov rdx, rax        ; rdx = 10

    ; print
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, 15
    syscall

    ; exit(0)
    mov rax, 60
    xor rdi, rdi
    syscall
