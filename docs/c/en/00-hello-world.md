# [0/10] Hello World & toolchain

> **Track:** C Programming · **Level:** 0 · **Slug:** `00-hello-world`

## Learning goals

- Understand: Hello World & toolchain
- Complete the lab exercise
- Know which man/docs to open next

## Theory

C is a systems language. You write source, compile to machine code, run the binary.

### Toolchain steps
1. **Preprocessor** expands `#include` / `#define`.
2. **Compiler** turns C into assembly.
3. **Assembler** emits object code (`.o`).
4. **Linker** resolves symbols into an executable.

```bash
gcc -Wall -Wextra -O0 -g -o hello hello.c
./hello
gcc -v hello.c -o hello   # see real commands
```

### Why systems people still use C
Close to the machine model: memory is bytes, control is explicit, ABI is stable. That power includes footguns — Xodex teaches them early with tools (`gdb`, `valgrind`).

## Practice

Compile and run hello.c. Explain what gcc, as, and ld do at a high level.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-00`

```bash
cd /usr/local/xodex/courses/c/level-00
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Navigation

- This is the entry level (0).
- Go to the next numbered lesson.
- Index: `docs/c/en/README.md`
