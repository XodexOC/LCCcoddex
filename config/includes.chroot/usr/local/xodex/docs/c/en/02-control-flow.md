# [2/10] Control flow

> **Track:** C Programming · **Level:** 2 · **Slug:** `02-control-flow`

## Learning goals

- Understand: Control flow
- Complete the lab exercise
- Know which man/docs to open next

## Theory

if/else, switch, while, for, do-while. Boolean is int. Prefer clear loops over clever ones.

### Branching and loops
C has no dedicated boolean type in older standards (`_Bool` exists in C99). Conditions use scalar zero/non-zero.

Prefer:
```c
for (int i = 0; i < n; i++) { ... }
```
over clever pointer tricks until you measure a need.

## Practice

Write FizzBuzz 1..100 in C without looking at solutions.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-02`

```bash
cd /usr/local/xodex/courses/c/level-02
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Navigation

- Previous: level 1
- Go to the next numbered lesson.
- Index: `docs/c/en/README.md`
