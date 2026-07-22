# [8/10] Tests

> **Track:** Rust · **Level:** 8 · **Slug:** `08-testing`

## Learning goals

- Understand: Tests
- Complete the lab exercise
- Know which man/docs to open next

## Theory

#[cfg(test)], cargo test, assert macros.

### Tests next to code
```rust
#[cfg(test)]
mod tests {
  use super::*;
  #[test]
  fn it_works() { assert_eq!(2+2, 4); }
}
```

## Practice

Unit tests for a pure function; one edge case.

**Live paths:**
- Examples: `/usr/local/xodex/examples/rust`
- Lab: `/usr/local/xodex/courses/rust/level-08`

```bash
cd /usr/local/xodex/courses/rust/level-08
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://doc.rust-lang.org/book/

## Navigation

- Previous: level 7
- Go to the next numbered lesson.
- Index: `docs/rust/en/README.md`
