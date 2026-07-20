# [8/10] Files & I/O

> **Track:** C Programming · **Level:** 8 · **Slug:** `08-files-io`

## Learning goals

- Understand: Files & I/O
- Complete the lab exercise
- Know which man/docs to open next

## Theory

fopen/fread/fwrite/fclose. Text vs binary. errno. Descriptor model vs FILE*.

### Streams
`FILE*` buffers I/O. Always check return values. For Unix systems programming you will later meet raw file descriptors (`open`, `read`, `write`) — start with stdio, then compare.

## Practice

Copy a file byte-by-byte. Handle errors with perror.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-08`

```bash
cd /usr/local/xodex/courses/c/level-08
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Navigation

- Previous: level 7
- Go to the next numbered lesson.
- Index: `docs/c/en/README.md`
