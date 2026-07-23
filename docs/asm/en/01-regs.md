# Lesson 01: Registers and syscalls

## x86_64 main registers

| Register | Purpose              |
|----------|----------------------|
| `rax`    | Accumulator / syscall|
| `rbx`    | Base register        |
| `rcx`    | Counter              |
| `rdx`    | Data register        |
| `rdi`    | Destination (arg 1)  |
| `rsi`    | Source (arg 2)       |
| `rsp`    | Stack pointer        |
| `rbp`    | Base pointer         |

## Linux syscalls

| Number | Name    | Description        |
|--------|---------|--------------------|
| 0      | `read`  | Read from file     |
| 1      | `write` | Write to file      |
| 60     | `exit`  | Exit process       |
