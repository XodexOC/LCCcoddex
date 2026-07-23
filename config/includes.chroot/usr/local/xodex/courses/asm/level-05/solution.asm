global _start

section .data
    arr dd 10, 20, 30, 40, 50
    len equ ($ - arr) / 4

section .text
_start:
    xor eax, eax
    xor esi, esi
loop:
    cmp esi, len
    jge done
    add eax, [arr + esi*4]
    inc esi
    jmp loop
done:
    mov ebx, eax
    mov eax, 1
    int 0x80
