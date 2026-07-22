# [6/10] Packages (apt)

> **Track:** Linux Systems · **Level:** 6 · **Slug:** `06-packages`

## Learning goals

- Understand: Packages (apt)
- Complete the lab exercise
- Know which man/docs to open next

## Theory

apt update/install/remove. Repos. --no-install-recommends. What is a .deb.

### Packages
Debian packages declare dependencies. Live images install with `--no-install-recommends` to stay small. Inspect with `apt-cache depends`.

## Practice

Search a package with apt-cache and explain dependencies of git.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-06`

```bash
cd /usr/local/xodex/courses/linux/level-06
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 7 hier`, `man 1 systemctl`

## Navigation

- Previous: level 5
- Go to the next numbered lesson.
- Index: `docs/linux/en/README.md`
