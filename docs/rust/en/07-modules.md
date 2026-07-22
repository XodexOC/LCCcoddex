# [7/10] Modules & crates

> **Track:** Rust · **Level:** 7 · **Slug:** `07-modules`

## Learning goals

- Understand: Modules & crates
- Complete the lab exercise
- Know which man/docs to open next

## Theory

mod, use, visibility, lib vs bin, workspaces sketch.

### Module tree
`mod foo;` loads `foo.rs` or `foo/mod.rs`. `pub` controls visibility. Binary crates can depend on a library crate in the same package.

## Practice

Split code into lib + bin calling a public function.

**Live paths:**
- Examples: `/usr/local/xodex/examples/rust`
- Lab: `/usr/local/xodex/courses/rust/level-07`

```bash
cd /usr/local/xodex/courses/rust/level-07
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://doc.rust-lang.org/book/

## Navigation

- Previous: level 6
- Go to the next numbered lesson.
- Index: `docs/rust/en/README.md`
