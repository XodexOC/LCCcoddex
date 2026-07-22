# [3/10] Types & constraints

> **Track:** SQL & data · **Level:** 3 · **Slug:** `03-types-constraints`

## Learning goals

- Understand: Types & constraints
- Complete the lab exercise
- Know which man/docs to open next

## Theory

INTEGER, TEXT, REAL, BLOB. PRIMARY KEY, NOT NULL, UNIQUE, CHECK.

### Integrity
Constraints catch bad data early. Application checks are not a substitute for DB constraints.

## Practice

Create table with PK and UNIQUE email; try violating it.

**Live paths:**
- Examples: `/usr/local/xodex/examples/sql`
- Lab: `/usr/local/xodex/courses/sql/level-03`

```bash
cd /usr/local/xodex/courses/sql/level-03
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://www.sqlite.org/docs.html

## Navigation

- Previous: level 2
- Go to the next numbered lesson.
- Index: `docs/sql/en/README.md`
