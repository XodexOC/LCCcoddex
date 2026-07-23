# Lesson 00: Introduction to Assembly

Assembly is a low-level language where each instruction
corresponds to a single CPU machine command.

## Tools

- `nasm` — assembler
- `ld` — linker

### Building a program

```bash
nasm -f elf64 hello.asm -o hello.o
ld hello.o -o hello
./hello
```
