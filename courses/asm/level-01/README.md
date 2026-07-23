# Lab 01: Первая программа: syscall / First program: syscall

**Track:** Assembly / Ассемблер
**Slug:** `01-first-program-syscall`

## Task (EN)

1. Write `exit.asm` that calls `exit(42)`. Build, run, verify with `echo $?`.
2. Write `hello.asm` that prints "Xodex OS" on one line.
3. (Bonus) Write a program with TWO write syscalls: first line "Hello", second line "World".

## Задание (RU)

1. Напиши `exit.asm` с `exit(42)`. Собери, запусти, проверь `echo $?`.
2. Напиши `hello.asm`, который выводит "Xodex OS" на одной строке.
3. (Бонус) Напиши программу с ДВУМЯ write: первая строка "Hello", вторая "World".

## Workflow

1. Read `docs/asm/en/01-*.md` and `docs/asm/ru/01-*.md`.
2. Write your solution as `solution.asm` in this directory.
3. Run `./test.sh` to check.
4. Mark complete in `~/.xodex/progress.json` when ready.

## Tools

- `nasm` — assembler
- `ld` — linker
- `echo $?` — check exit code
