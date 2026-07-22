# [8/10] systemd & services

> **Track:** Linux Systems · **Level:** 8 · **Slug:** `08-systemd`

## Learning goals

- Understand: systemd & services
- Complete the lab exercise
- Know which man/docs to open next

## Theory

units, systemctl status/start/enable. journals with journalctl.

### Units
Services are unit files. Drop-ins in `*.service.d/` override snippets — Xodex autologin is one.

## Practice

Inspect getty@tty1 and explain Xodex autologin drop-in.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-08`

```bash
cd /usr/local/xodex/courses/linux/level-08
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 7 hier`, `man 1 systemctl`

## Navigation

- Previous: level 7
- Go to the next numbered lesson.
- Index: `docs/linux/en/README.md`
