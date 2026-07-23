global _start

section .data
    src db "Hello, World!", 0xa
    srclen equ $ - src

section .bss
    dst resb srclen

section .text
_start:
    cld
    mov rsi, src
    mov rdi, dst
    mov rcx, srclen
    rep movsb

    mov eax, 1
    mov edi, 1
    mov rsi, src
    mov rdx, srclen
    syscall

    mov eax, 1
    mov edi, 1
    mov rsi, dst
    mov rdx, srclen
    syscall

    mov eax, 1
    xor ebx, ebx
    int 0x80
