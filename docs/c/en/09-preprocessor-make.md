# [9/10] Preprocessor & Make

> **Track:** C Programming · **Level:** 9 · **Slug:** `09-preprocessor-make`

## Learning goals

- Understand: Preprocessor & Make
- Complete the lab exercise
- Know which man/docs to open next

## Theory

#include, #define, include guards, macros pitfalls. Makefile targets and dependencies.

### Build systems
A Makefile encodes a dependency graph. Rebuild only what changed. Flags for learning builds:
```make
CFLAGS = -std=c11 -Wall -Wextra -Werror -g
```
Include guards:
```c
#ifndef FOO_H
#define FOO_H
/* ... */
#endif
```

## Practice

Split a mini project into .h/.c with Makefile and -Wall -Wextra -Werror.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-09`

```bash
cd /usr/local/xodex/courses/c/level-09
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Navigation

- Previous: level 8
- Go to the next numbered lesson.
- Index: `docs/c/en/README.md`
