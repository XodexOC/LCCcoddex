# [6/10] Errors & files

> **Track:** Python · **Level:** 6 · **Slug:** `06-errors-files`

## Learning goals

- Understand: Errors & files
- Complete the lab exercise
- Know which man/docs to open next

## Theory

try/except/else/finally. Custom exceptions. pathlib and context managers.

### Context managers
```python
with open(path, encoding="utf-8") as f:
    data = f.read()
```
Files close even if exceptions occur. Custom managers implement `__enter__` / `__exit__`.

## Practice

Read JSON config with clear errors if missing keys.

**Live paths:**
- Examples: `/usr/local/xodex/examples/python`
- Lab: `/usr/local/xodex/courses/python/level-06`

```bash
cd /usr/local/xodex/courses/python/level-06
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://docs.python.org/3/tutorial/

## Navigation

- Previous: level 5
- Go to the next numbered lesson.
- Index: `docs/python/en/README.md`
