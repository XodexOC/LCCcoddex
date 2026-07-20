# [4/10] Error handling

> **Track:** Rust · **Level:** 4 · **Slug:** `04-error-handling`

## Learning goals

- Understand: Error handling
- Complete the lab exercise
- Know which man/docs to open next

## Theory

Result, ?, panic vs recoverable errors. unwrap carefully.

### Errors as values
```rust
fn read_it(p: &str) -> std::io::Result<String> {
    std::fs::read_to_string(p)
}
```
`?` propagates. Reserve `panic!` for bugs, not expected I/O failures.

## Practice

Read a file to String; propagate errors with ? from main via Result.

**Live paths:**
- Examples: `/usr/local/xodex/examples/rust`
- Lab: `/usr/local/xodex/courses/rust/level-04`

```bash
cd /usr/local/xodex/courses/rust/level-04
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://doc.rust-lang.org/book/

## Navigation

- Previous: level 3
- Go to the next numbered lesson.
- Index: `docs/rust/en/README.md`
