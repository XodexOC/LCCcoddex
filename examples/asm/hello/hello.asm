; hello.asm — Hello World для x86_64 Linux
; Сборка:
;   nasm -f elf64 hello.asm -o hello.o
;   ld hello.o -o hello

section .data
    msg db "Hello, Xodex!", 0xa
    len equ $ - msg

section .text
    global _start

_start:
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    mov rsi, msg
    mov rdx, len
    syscall

    mov rax, 60         ; sys_exit
    xor rdi, rdi
    syscall
