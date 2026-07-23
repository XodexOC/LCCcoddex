# Lab 02: Регистры и mov / Registers and mov

**Track:** Assembly / Ассемблер
**Slug:** `02-registers-and-mov`

## Task (EN)

1. Write a program that sets RAX=10, RBX=20, RCX=30, copies RAX to RDX, then prints something.
2. Write a program that sets RAX=0xFFFFFFFFFFFFFFFF, zeros it via EAX, and exits.
3. (Bonus) Write a program that sets AL=10, AH=20, then prints the value of AX.
   Hint: AX = AH * 256 + AL. You'll need to write the number as a string somehow
   or just check via a debugger.

## Задание (RU)

1. Напиши программу: RAX=10, RBX=20, RCX=30, скопируй RAX в RDX. Выведи что-нибудь.
2. Напиши программу: RAX=0xFFFFFFFFFFFFFFFF, обнули через EAX. Завершись.
3. (Бонус) Напиши: AL=10, AH=20. Чему равен AX? Проверь через gdb или выведи.

## Workflow

1. Read `docs/asm/en/02-*.md` and `docs/asm/ru/02-*.md`.
2. Write `solution.asm` in this directory.
3. Run `./test.sh`.
4. Mark complete.

## Tools

- `nasm`, `ld`
- `gdb` for register inspection
