; solution.asm — массив + строка
section .data
    msg db "Xodex OS", 10
    len equ $ - msg
    arr dd 7, 14, 21, 28, 35

section .text
    global _start

_start:
    ; arr[3] = 28
    mov eax, [arr + 12]   ; 3 * 4 = 12
    ; eax = 28

    ; сохраняем результат
    mov rdi, rax          ; rdi = 28 (код возврата)

    ; выводим строку
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, len
    syscall

    ; exit(28)
    mov rax, 60
    ; rdi уже 28
    syscall
