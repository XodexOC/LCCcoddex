# [6/10] Indexes

> **Track:** SQL & data · **Level:** 6 · **Slug:** `06-indexes`

## Learning goals

- Understand: Indexes
- Complete the lab exercise
- Know which man/docs to open next

## Theory

B-tree sketch. CREATE INDEX. When indexes help and hurt.

### Indexes trade write cost for read speed
Index columns used in frequent `WHERE`/`JOIN`. Too many indexes slow writes and bloat storage.

## Practice

Explain query plan before/after index on a filter column.

**Live paths:**
- Examples: `/usr/local/xodex/examples/sql`
- Lab: `/usr/local/xodex/courses/sql/level-06`

```bash
cd /usr/local/xodex/courses/sql/level-06
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://www.sqlite.org/docs.html

## Navigation

- Previous: level 5
- Go to the next numbered lesson.
- Index: `docs/sql/en/README.md`
