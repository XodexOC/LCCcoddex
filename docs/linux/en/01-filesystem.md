# [1/10] Filesystem hierarchy

> **Track:** Linux Systems · **Level:** 1 · **Slug:** `01-filesystem`

## Learning goals

- Understand: Filesystem hierarchy
- Complete the lab exercise
- Know which man/docs to open next

## Theory

FHS: /, /etc, /var, /home, /usr, /tmp, /proc, /sys. Permissions rwx.

### FHS map
| Path | Role |
|------|------|
| `/etc` | config |
| `/var` | variable data/logs |
| `/usr` | userland programs |
| `/home` | people |
| `/proc` `/sys` | kernel interfaces |

## Practice

Explain permissions of /etc/passwd and your home directory.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-01`

```bash
cd /usr/local/xodex/courses/linux/level-01
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 7 hier`, `man 1 systemctl`

## Navigation

- Previous: level 0
- Go to the next numbered lesson.
- Index: `docs/linux/en/README.md`
