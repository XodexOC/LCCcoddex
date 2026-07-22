# [1/10] Ownership

> **Track:** Rust · **Level:** 1 · **Slug:** `01-ownership`

## Learning goals

- Understand: Ownership
- Complete the lab exercise
- Know which man/docs to open next

## Theory

Move semantics, borrow checker motivation. Stack vs heap intro.

### Ownership rules (core)
1. Each value has one owner.
2. When owner goes out of scope, value is dropped.
3. Moves transfer ownership; clones are explicit.

This eliminates a class of use-after-free bugs at compile time.

## Practice

Show a compile error from use-after-move; fix with clone or borrow.

**Live paths:**
- Examples: `/usr/local/xodex/examples/rust`
- Lab: `/usr/local/xodex/courses/rust/level-01`

```bash
cd /usr/local/xodex/courses/rust/level-01
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://doc.rust-lang.org/book/

## Navigation

- Previous: level 0
- Go to the next numbered lesson.
- Index: `docs/rust/en/README.md`
