# [7/10] Structs & data layout

> **Track:** C Programming · **Level:** 7 · **Slug:** `07-structs`

## Learning goals

- Understand: Structs & data layout
- Complete the lab exercise
- Know which man/docs to open next

## Theory

struct, typedef, padding, alignment. Nested structs. Opaque pointers for APIs.

### Layout and ABI
Compilers insert **padding** for alignment. Two structs with the same logical fields can differ in size if field order differs. Use `offsetof` from `<stddef.h>` when debugging binary layouts.

## Practice

Define Point and Rectangle; compute area; print sizeof and offsets with offsetof.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-07`

```bash
cd /usr/local/xodex/courses/c/level-07
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Navigation

- Previous: level 6
- Go to the next numbered lesson.
- Index: `docs/c/en/README.md`
