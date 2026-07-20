# Xodex

**EN** | [RU](README.ru.md)

Educational terminal-first Debian Live environment. Learn real UNIX: C/C++, Python, Rust, SQL, and Linux systems thinking — through exploration, documentation, and practice.

| | |
|---|---|
| **Interface** | Console only (no GUI) |
| **User** | login `xodex` / password `xodex` (sudo) |
| **Target size** | ~1–2 GB Live ISO |
| **Base** | Debian Bookworm + live-boot / live-config |
| **Languages** | Russian + English materials |

## Repository layout (monorepo)

```text
Xodex/
├── core/           # live-build config, hooks, package lists, chroot includes
├── docs/           # bilingual lessons (levels 0–10)
├── examples/       # ready-to-compile sample projects
├── courses/        # labs with tasks + test.sh
├── tools/          # shell UX: menu, prompt, progress schema
├── scripts/        # build-xodex.sh and helpers
├── Xodex_readme.md # full technical specification (RU)
└── README.md       # this file
```

## Quick start (build ISO)

> Requires Debian/Ubuntu host with root, ~10 GB free disk, and packages listed in `scripts/build-xodex.sh`.

```bash
# Install build dependencies (Debian/Ubuntu)
sudo apt update
sudo apt install -y live-build debootstrap squashfs-tools xorriso \
  grub-pc-bin grub-efi-amd64-bin mtools isolinux syslinux-common

# Configure and build
cd /path/to/Xodex
sudo ./scripts/build-xodex.sh
```

Output ISO path: `build/xodex-live-amd64.hybrid.iso` (exact name may vary with live-build).

Test in QEMU:

```bash
qemu-system-x86_64 -m 2048 -cdrom build/*.hybrid.iso -boot d
# UEFI (optional):
# qemu-system-x86_64 -m 2048 -bios /usr/share/OVMF/OVMF_CODE.fd -cdrom build/*.hybrid.iso
```

## Curriculum tracks (0 → 10)

Each track goes from absolute beginner (**0**) to confident intermediate/advanced (**10**).

| Track | Path | Focus |
|-------|------|--------|
| C | `docs/c/`, `courses/c/` | Memory, pointers, toolchain |
| Python | `docs/python/`, `courses/python/` | Language + tooling |
| Linux | `docs/linux/`, `courses/linux/` | Processes, FS, shell, networking |
| Rust | `docs/rust/`, `courses/rust/` | Ownership, safe systems code |
| SQL | `docs/sql/`, `courses/sql/` | SQLite-first data literacy |

In the Live system materials live under `/usr/local/xodex/`.

```bash
xodex-menu          # interactive menu
ls /usr/local/xodex/docs
```

Progress (bookmarks, completed lessons) is stored in `~/.xodex/progress.json`.

## Design goals

- University-style systems thinking, not click-through tutorials
- Offline core (docs + examples + compilers on ISO)
- Online extras via links and optional `git` sync later
- Rebuildable, auditable Debian Live image

Full architecture, package tables, and milestones: see **[Xodex_readme.md](Xodex_readme.md)** (Russian specification).

## Status

- [x] Monorepo scaffold
- [x] live-build core + package lists + hooks
- [x] Full bilingual curriculum structure 0–10
- [ ] First bootable ISO verified in QEMU (after maintainer approval)
- [ ] GitHub Releases with ISO artifacts

## License

MIT — see [LICENSE](LICENSE).

## Contributing

1. Prefer small, reviewable commits.
2. Keep lessons bilingual (`ru/` + `en/`).
3. Do not add GUI packages to the default image.
4. Test package-list changes with a full rebuild when possible.
