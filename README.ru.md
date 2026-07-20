# Xodex

[EN](README.md) | **RU**

Образовательная Live-среда на базе Debian с упором на терминал. Цель — «университетский» опыт реальной UNIX-системы: C/C++, Python, Rust, SQL и системное мышление через исследование, документацию и практику.

| | |
|---|---|
| **Интерфейс** | Только консоль (без GUI) |
| **Пользователь** | `student` с sudo; root только через `sudo` |
| **Размер** | Live ISO ~1–2 ГБ |
| **База** | Debian Bookworm + live-boot / live-config |
| **Языки** | Материалы на русском и английском |

## Структура monorepo

```text
Xodex/
├── core/           # live-build: конфиги, hooks, списки пакетов, includes
├── docs/           # двуязычные уроки (уровни 0–10)
├── examples/       # готовые примеры кода
├── courses/        # лаборатории: задания + test.sh
├── tools/          # меню, prompt, схема прогресса
├── scripts/        # build-xodex.sh и вспомогательные скрипты
├── Xodex_readme.md # полное ТЗ
└── README.md       # краткое описание (EN)
```

## Быстрый старт (сборка ISO)

> Нужен хост Debian/Ubuntu, root, ~10 ГБ свободного места.

```bash
sudo apt update
sudo apt install -y live-build debootstrap squashfs-tools xorriso \
  grub-pc-bin grub-efi-amd64-bin mtools isolinux syslinux-common

cd /path/to/Xodex
sudo ./scripts/build-xodex.sh
```

ISO: `build/xodex-live-amd64.hybrid.iso` (имя может отличаться).

Проверка в QEMU:

```bash
qemu-system-x86_64 -m 2048 -cdrom build/*.hybrid.iso -boot d
```

## Курсы (0 → 10)

Каждый трек — от новичка (**0**) до уверенного уровня (**10**).

| Трек | Путь | Фокус |
|------|------|--------|
| C | `docs/c/`, `courses/c/` | Память, указатели, toolchain |
| Python | `docs/python/`, `courses/python/` | Язык и инструменты |
| Linux | `docs/linux/`, `courses/linux/` | Процессы, ФС, shell, сеть |
| Rust | `docs/rust/`, `courses/rust/` | Ownership, безопасный systems-код |
| SQL | `docs/sql/`, `courses/sql/` | SQLite и основы данных |

В Live-системе материалы: `/usr/local/xodex/`.

```bash
xodex-menu
ls /usr/local/xodex/docs
```

Прогресс: `~/.xodex/progress.json`.

## Цели

- Системное мышление, а не «кликни дальше»
- Офлайн-ядро (docs + examples + компиляторы в ISO)
- Онлайн-расширения через ссылки и (позже) `git`-синхронизацию
- Воспроизводимый, аудируемый Debian Live-образ

Полное ТЗ: **[Xodex_readme.md](Xodex_readme.md)**.

## Статус

- [x] Каркас monorepo
- [x] live-build core + package lists + hooks
- [x] Полная двуязычная структура курсов 0–10
- [ ] Первый загружаемый ISO в QEMU (после одобрения)
- [ ] GitHub Releases с ISO

## Лицензия

MIT — [LICENSE](LICENSE).

## Участие

1. Небольшие коммиты.
2. Уроки на двух языках (`ru/` + `en/`).
3. Не добавлять GUI-пакеты в образ по умолчанию.
4. Изменения package-lists по возможности проверять полной пересборкой.
