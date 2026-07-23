; solution.asm — (10 + 5) * 2 - (100 / 10) = 20
section .text
    global _start

_start:
    ; (10 + 5) = 15
    mov rax, 10
    add rax, 5          ; rax = 15

    ; * 2 = 30
    mov rbx, 2
    mul rbx             ; rax = 30

    ; сохраняем
    mov rcx, rax        ; rcx = 30

    ; 100 / 10 = 10
    mov rax, 100
    xor rdx, rdx
    mov rbx, 10
    div rbx             ; rax = 10

    ; 30 - 10 = 20
    sub rcx, rax        ; rcx = 20

    ; exit(20)
    mov rax, 60
    mov rdi, rcx
    syscall
