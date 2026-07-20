; NASM Linux x86_64 write+exit
section .data
msg db 'Hello, Xodex (ASM)', 10
len equ $-msg
section .text
global _start
_start:
  mov rax, 1
  mov rdi, 1
  mov rsi, msg
  mov rdx, len
  syscall
  mov rax, 60
  xor rdi, rdi
  syscall
