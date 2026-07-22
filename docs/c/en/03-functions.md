# [3/10] Functions & stack

> **Track:** C Programming · **Level:** 3 · **Slug:** `03-functions`

## Learning goals

- Understand: Functions & stack
- Complete the lab exercise
- Know which man/docs to open next

## Theory

Call by value. Stack frames. Prototypes vs definitions. Recursion depth limits.

### Calling convention (mental model)
Arguments and return address live on the stack (or registers — ABI-dependent). Local variables die when the function returns — never return a pointer to a local.

Always declare prototypes before use; put them in headers for multi-file projects.

## Practice

Implement factorial both iterative and recursive; compare for n=10.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-03`

```bash
cd /usr/local/xodex/courses/c/level-03
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Navigation

- Previous: level 2
- Go to the next numbered lesson.
- Index: `docs/c/en/README.md`
