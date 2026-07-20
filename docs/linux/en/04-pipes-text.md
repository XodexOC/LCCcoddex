# [4/10] Pipes & text tools

> **Track:** Linux Systems · **Level:** 4 · **Slug:** `04-pipes-text`

## Learning goals

- Understand: Pipes & text tools
- Complete the lab exercise
- Know which man/docs to open next

## Theory

Pipes and redirection. grep, sed, awk, cut, sort, uniq, wc.

### Composition
Unix philosophy: small tools + pipes. Example:
```bash
tr -cs 'A-Za-z' '\n' < file | tr 'A-Z' 'a-z' | sort | uniq -c | sort -nr | head
```

## Practice

Count unique words in a file with a pipeline.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-04`

```bash
cd /usr/local/xodex/courses/linux/level-04
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 7 hier`, `man 1 systemctl`

## Navigation

- Previous: level 3
- Go to the next numbered lesson.
- Index: `docs/linux/en/README.md`
