global _start

section .data
    msg1 db "Hello from ASM", 0xa
    len1 equ $ - msg1
    msg2 db "Stack and subroutines", 0xa
    len2 equ $ - msg2

section .text
_start:
    mov rsi, msg1
    mov rdx, len1
    call print_string

    mov rsi, msg2
    mov rdx, len2
    call print_string

    mov eax, 1
    xor ebx, ebx
    int 0x80

print_string:
    mov eax, 1
    mov edi, 1
    syscall
    ret
