# [4/10] Pointers

> **Track:** C Programming · **Level:** 4 · **Slug:** `04-pointers`

## Learning goals

- Understand: Pointers
- Complete the lab exercise
- Know which man/docs to open next

## Theory

A pointer holds an address. * dereference, & address-of. NULL. Pointer arithmetic on arrays.

### Pointers are addresses
```c
int x = 42;
int *p = &x;
*p = 7; /* x is now 7 */
```
`NULL` means “no object”. Dereferencing NULL is undefined. Pointer arithmetic scales by `sizeof(*p)` — only valid within arrays (and one-past-end).

## Practice

Swap two ints via pointers. Explain why swap without pointers fails.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-04`

```bash
cd /usr/local/xodex/courses/c/level-04
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Navigation

- Previous: level 3
- Go to the next numbered lesson.
- Index: `docs/c/en/README.md`
