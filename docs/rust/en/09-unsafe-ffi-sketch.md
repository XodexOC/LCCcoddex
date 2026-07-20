# [9/10] Unsafe & FFI sketch

> **Track:** Rust · **Level:** 9 · **Slug:** `09-unsafe-ffi-sketch`

## Learning goals

- Understand: Unsafe & FFI sketch
- Complete the lab exercise
- Know which man/docs to open next

## Theory

When unsafe is needed. raw pointers. FFI to C at high level only.

### Unsafe is a boundary
`unsafe` does not turn off the borrow checker entirely; it allows a few extra operations you must uphold manually. Prefer safe wrappers.

## Practice

Read docs: list three rules before writing unsafe.

**Live paths:**
- Examples: `/usr/local/xodex/examples/rust`
- Lab: `/usr/local/xodex/courses/rust/level-09`

```bash
cd /usr/local/xodex/courses/rust/level-09
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://doc.rust-lang.org/book/

## Navigation

- Previous: level 8
- Go to the next numbered lesson.
- Index: `docs/rust/en/README.md`
