global square

section .text
square:
    mov eax, edi
    imul eax, eax
    ret
