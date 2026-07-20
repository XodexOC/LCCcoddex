# [9/10] Shell scripting

> **Track:** Linux Systems · **Level:** 9 · **Slug:** `09-shell-scripting`

## Learning goals

- Understand: Shell scripting
- Complete the lab exercise
- Know which man/docs to open next

## Theory

shebang, variables, quotes, if, loops, set -euo pipefail, functions.

### Robust scripts
```bash
#!/usr/bin/env bash
set -euo pipefail
```
Quote variables. Prefer `[[ ]]`. Check exit codes of critical commands.

## Practice

Write a script that backs up a directory with timestamp.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-09`

```bash
cd /usr/local/xodex/courses/linux/level-09
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 7 hier`, `man 1 systemctl`

## Navigation

- Previous: level 8
- Go to the next numbered lesson.
- Index: `docs/linux/en/README.md`
