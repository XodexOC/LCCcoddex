# [5/10] Permissions & links

> **Track:** Linux Systems · **Level:** 5 · **Slug:** `05-permissions-links`

## Learning goals

- Understand: Permissions & links
- Complete the lab exercise
- Know which man/docs to open next

## Theory

chmod, chown, umask. Hard vs symbolic links. Sticky bit sketch.

### Links
Hard link: another name for the same inode (same filesystem). Symlink: path pointer, can dangle.

## Practice

Create a private directory mode 700 and a symlink to a lesson file.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-05`

```bash
cd /usr/local/xodex/courses/linux/level-05
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 7 hier`, `man 1 systemctl`

## Navigation

- Previous: level 4
- Go to the next numbered lesson.
- Index: `docs/linux/en/README.md`
