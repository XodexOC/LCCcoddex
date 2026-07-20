# [10/10] Systems thinking (capstone)

> **Track:** Linux Systems · **Level:** 10 · **Slug:** `10-systems-thinking`

## Learning goals

- Understand: Systems thinking (capstone)
- Complete the lab exercise
- Know which man/docs to open next

## Theory

How Live boot works (kernel, initrd, squashfs). Observability. Next: containers, servers.

### Capstone: understand the medium
Xodex is a **Live** system: kernel + initrd mount a squashfs root. Your experiments may vanish on reboot unless persistence is enabled later. That is a feature for learning.

## Practice

Map the Xodex boot path from ISO layout to login prompt in a short essay.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-10`

```bash
cd /usr/local/xodex/courses/linux/level-10
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- `man 7 hier`, `man 1 systemctl`

## Navigation

- Previous: level 9
- Capstone complete — revisit early labs with gdb/valgrind/strace.
- Index: `docs/linux/en/README.md`
