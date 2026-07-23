# Assembly — levels 00-10

Overview of the assembly track for x86-64 Linux with NASM.

| Level | Topic | Description |
|:-----:|-------|-------------|
| 00 | How computers work | Bits, bytes, hex, CPU registers, RAM, instructions, assembler vs linker |
| 01 | First program: syscall | `exit(0)`, `hello.asm`, section .data/.text, syscall mechanics, write |
| 02 | Registers and mov | RAX/EAX/AX/AL/AH, mov immediate/reg/mem, addressing vs value, size rules |
| 03 | Arithmetic | `add`/`sub`/`inc`/`dec`, `mul`/`imul`, `div`/`idiv`, flags ZF/CF/SF/OF |
| 04 | Memory basics | `.data` section, `db`/`dw`/`dd`/`dq`/`resb`, labels, arrays, `equ`/`$` |
| 05 | Addressing modes | direct, register indirect, base+displacement, indexed, full, LEA |
| 06 | Comparison and jumps | `cmp`, `test`, conditional jumps (`je`/`jg`/`jl`/`ja`/`jb`), if/else/while/for |
| 07 | Stack and subroutines | `push`/`pop`, `call`/`ret`, stack frame, prologue/epilogue, local vars, recursion |
| 08 | Calling convention | System V AMD64 ABI: arg registers, caller/callee-saved, stack alignment, `cqo` |
| 09 | Strings and REP | `lodsb`/`stosb`/`movsb`/`scasb`/`cmpsb`, `rep`/`repe`/`repne`, strlen, strcpy |
| 10 | Capstone: C + Assembly | `extern`/`global`, calling C from asm, calling asm from C, `printf`, inline asm |