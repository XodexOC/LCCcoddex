# [2/10] References & borrowing

> **Track:** Rust · **Level:** 2 · **Slug:** `02-borrowing`

## Learning goals

- Understand: References & borrowing
- Complete the lab exercise
- Know which man/docs to open next

## Theory

Shared vs mutable borrows. Lifetimes intuition (no deep syntax yet).

### Borrowing
`&T` shared immutable; `&mut T` exclusive mutable. Not both at once for the same data. That is the aliasing XOR mutability rule.

## Practice

Function that takes &str and returns length; one that mutates via &mut.

**Live paths:**
- Examples: `/usr/local/xodex/examples/rust`
- Lab: `/usr/local/xodex/courses/rust/level-02`

```bash
cd /usr/local/xodex/courses/rust/level-02
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://doc.rust-lang.org/book/

## Navigation

- Previous: level 1
- Go to the next numbered lesson.
- Index: `docs/rust/en/README.md`
