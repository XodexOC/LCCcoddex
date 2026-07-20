# [6/10] Dynamic memory

> **Track:** C Programming · **Level:** 6 · **Slug:** `06-memory`

## Learning goals

- Understand: Dynamic memory
- Complete the lab exercise
- Know which man/docs to open next

## Theory

malloc/calloc/realloc/free. Ownership: who frees? Leaks and double-free. Valgrind.

### Heap discipline
```c
int *a = malloc(n * sizeof *a);
if (!a) { perror("malloc"); return 1; }
/* use a */
free(a);
a = NULL; /* optional hygiene */
```
Every successful `malloc` needs exactly one `free`. Use **valgrind** on Xodex to catch leaks and invalid accesses.

## Practice

Build a dynamic int array (push). Run under valgrind --leak-check=full.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-06`

```bash
cd /usr/local/xodex/courses/c/level-06
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Navigation

- Previous: level 5
- Go to the next numbered lesson.
- Index: `docs/c/en/README.md`
