# [10/10] Data literacy (capstone)

> **Track:** SQL & data · **Level:** 10 · **Slug:** `10-data-literacy`

## Learning goals

- Understand: Data literacy (capstone)
- Complete the lab exercise
- Know which man/docs to open next

## Theory

Schema design, integrity, backups .dump. Postgres client awareness.

### Capstone schema
Model Xodex itself: tracks, lessons, student progress. Export with `.dump` for backups.

## Practice

Design a mini schema for courses/lessons/progress; implement in SQLite.

**Live paths:**
- Examples: `/usr/local/xodex/examples/sql`
- Lab: `/usr/local/xodex/courses/sql/level-10`

```bash
cd /usr/local/xodex/courses/sql/level-10
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://www.sqlite.org/docs.html

## Navigation

- Previous: level 9
- Capstone complete — revisit early labs with gdb/valgrind/strace.
- Index: `docs/sql/en/README.md`
