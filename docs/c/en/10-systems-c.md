# [10/10] Systems C (capstone)

> **Track:** C Programming · **Level:** 10 · **Slug:** `10-systems-c`

## Learning goals

- Understand: Systems C (capstone)
- Complete the lab exercise
- Know which man/docs to open next

## Theory

syscalls via libc, processes (fork/exec overview), signals sketch, reading man 2/3.

### Capstone: tiny shell
You combine: strings, memory, process API (`fork`, `execvp`, `waitpid`). Read `man 2 fork` and `man 3 exec`. This is the bridge from language C to Linux systems (see **linux** track).

## Practice

Write a tiny shell loop: read line, fork, execvp, wait. Handle empty input.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-10`

```bash
cd /usr/local/xodex/courses/c/level-10
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Navigation

- Previous: level 9
- Capstone complete — revisit early labs with gdb/valgrind/strace.
- Index: `docs/c/en/README.md`
