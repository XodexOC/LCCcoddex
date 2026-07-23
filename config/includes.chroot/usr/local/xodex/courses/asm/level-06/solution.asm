global _start

section .text
_start:
    mov eax, 10
    mov ebx, 25
    mov ecx, 15

    cmp eax, ebx
    jge check_c
    mov eax, ebx
check_c:
    cmp eax, ecx
    jge done
    mov eax, ecx
done:
    mov ebx, eax
    mov eax, 1
    int 0x80
