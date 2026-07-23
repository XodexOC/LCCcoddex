global _start

section .text
_start:
    mov edi, 10
    mov esi, 20
    mov edx, 30
    call sum_three

    mov ebx, eax
    mov eax, 1
    int 0x80

sum_three:
    mov eax, edi
    add eax, esi
    add eax, edx
    ret
