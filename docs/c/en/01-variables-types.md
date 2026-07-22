# [1/10] Variables & types

> **Track:** C Programming · **Level:** 1 · **Slug:** `01-variables-types`

## Learning goals

- Understand: Variables & types
- Complete the lab exercise
- Know which man/docs to open next

## Theory

Integers, floats, chars. Size matters: sizeof, signed vs unsigned, integer promotion.

### Width and representation
`int` is at least 16 bits (usually 32). Prefer fixed-width types from `<stdint.h>` when layout matters (`uint32_t`).

```c
#include <stdio.h>
#include <stdint.h>
int main(void) {
  printf("int=%zu long=%zu size_t=%zu\n", sizeof(int), sizeof(long), sizeof(size_t));
  uint8_t x = 255; x += 1; /* wraps to 0 */
  printf("wrap=%u\n", x);
}
```

Signed overflow is undefined behavior — never rely on it.

## Practice

Print sizeof for int, long, size_t, char. Predict overflow of unsigned char.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-01`

```bash
cd /usr/local/xodex/courses/c/level-01
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Navigation

- Previous: level 0
- Go to the next numbered lesson.
- Index: `docs/c/en/README.md`
