# [2/10] Users & sudo

> **Track:** Linux Systems · **Level:** 2 · **Slug:** `02-users-sudo`

## Learning goals

- Understand: Users & sudo
- Complete the lab exercise
- Know which man/docs to open next

## Theory

UID/GID, /etc/passwd, groups, sudo model. Why not daily root.

### Least privilege
Daily work as `xodex`. Elevate only for admin tasks. Xodex Live uses passwordless sudo for classroom speed — production servers should not.

## Practice

As xodex, run a command with sudo and inspect /etc/sudoers.d/xodex.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-02`

```bash
cd /usr/local/xodex/courses/linux/level-02
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 7 hier`, `man 1 systemctl`

## Navigation

- Previous: level 1
- Go to the next numbered lesson.
- Index: `docs/linux/en/README.md`
