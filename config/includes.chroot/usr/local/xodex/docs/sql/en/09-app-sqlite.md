# [9/10] SQLite from apps

> **Track:** SQL & data · **Level:** 9 · **Slug:** `09-app-sqlite`

## Learning goals

- Understand: SQLite from apps
- Complete the lab exercise
- Know which man/docs to open next

## Theory

Python sqlite3 module. Parameterized queries (no string concat!).

### App access
Always parameterize:
```python
cur.execute("INSERT INTO u(name) VALUES (?)", (name,))
```
String-built SQL invites injection.

## Practice

Python script inserting users safely with placeholders.

**Live paths:**
- Examples: `/usr/local/xodex/examples/sql`
- Lab: `/usr/local/xodex/courses/sql/level-09`

```bash
cd /usr/local/xodex/courses/sql/level-09
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://www.sqlite.org/docs.html

## Navigation

- Previous: level 8
- Go to the next numbered lesson.
- Index: `docs/sql/en/README.md`
