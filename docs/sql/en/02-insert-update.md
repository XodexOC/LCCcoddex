# [2/10] INSERT/UPDATE/DELETE

> **Track:** SQL & data · **Level:** 2 · **Slug:** `02-insert-update`

## Learning goals

- Understand: INSERT/UPDATE/DELETE
- Complete the lab exercise
- Know which man/docs to open next

## Theory

DML mutations. Transactions sketch BEGIN/COMMIT.

### Mutations
`INSERT`/`UPDATE`/`DELETE` change state. Wrap multi-step changes in transactions for atomicity.

## Practice

Insert three rows; update one; delete one inside a transaction.

**Live paths:**
- Examples: `/usr/local/xodex/examples/sql`
- Lab: `/usr/local/xodex/courses/sql/level-02`

```bash
cd /usr/local/xodex/courses/sql/level-02
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://www.sqlite.org/docs.html

## Navigation

- Previous: level 1
- Go to the next numbered lesson.
- Index: `docs/sql/en/README.md`
