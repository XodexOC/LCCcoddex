# [5/10] Arrays & strings

> **Track:** C Programming · **Level:** 5 · **Slug:** `05-arrays-strings`

## Learning goals

- Understand: Arrays & strings
- Complete the lab exercise
- Know which man/docs to open next

## Theory

Arrays decay to pointers. C strings are char* with NUL terminator. Buffer overflows are real.

### Arrays and C strings
`char s[] = "hi";` is `{'h','i','\0'}`. Most string APIs stop at the first NUL. Prefer bounds-aware functions (`snprintf`) over `strcpy`/`gets` (forbidden).

Array parameters decay to pointers — `sizeof` inside a function does **not** give the caller’s array length.

## Practice

Implement safe_strlen and reverse a string in place.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-05`

```bash
cd /usr/local/xodex/courses/c/level-05
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Navigation

- Previous: level 4
- Go to the next numbered lesson.
- Index: `docs/c/en/README.md`
