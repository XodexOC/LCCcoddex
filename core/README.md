# Xodex core (live-build)

This directory holds the **Debian live-build** configuration used by `scripts/build-xodex.sh`.

## Layout

```text
core/
├── auto/                 # optional lb auto/* helpers (generated/used by script)
├── config/               # live-build config tree (copied/synced into build/)
│   ├── package-lists/    # .list.chroot package sets
│   ├── hooks/            # chroot and binary hooks
│   └── includes.chroot/  # files overlayed into the Live rootfs
└── README.md
```

## Package lists

| File | Role |
|------|------|
| `base.list.chroot` | Kernel, live-boot, console, locales, essential tools |
| `dev.list.chroot` | Compilers, languages, debug tools |
| `utils.list.chroot` | Comfort utilities (tmux, mc, htop, w3m, …) |

All installs should prefer `--no-install-recommends` (set in `build-xodex.sh` via `lb config`).

## User model

- User: `student` (sudo)
- Root password: locked / not set for login
- Optional autologin on tty1 via systemd drop-in

## Rebuild flow

See repository root `scripts/build-xodex.sh`. Do not run `lb build` from a dirty tree without reading the script — it prepares a clean `build/` workspace and injects docs/examples/courses/tools.
