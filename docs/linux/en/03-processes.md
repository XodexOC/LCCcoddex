# [3/10] Processes

> **Track:** Linux Systems · **Level:** 3 · **Slug:** `03-processes`

## Learning goals

- Understand: Processes
- Complete the lab exercise
- Know which man/docs to open next

## Theory

PID, parent, states. ps, top/htop, kill, jobs, foreground/background.

### Process tree
PID 1 is init (`systemd`). Children inherit environment. Signals deliver asynchronous notifications (`SIGTERM` polite, `SIGKILL` not).

## Practice

Start sleep in background, find PID, send SIGTERM.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-03`

```bash
cd /usr/local/xodex/courses/linux/level-03
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 7 hier`, `man 1 systemctl`

## Navigation

- Previous: level 2
- Go to the next numbered lesson.
- Index: `docs/linux/en/README.md`
