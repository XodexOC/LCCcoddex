# Lab 03: Арифметика / Arithmetic

**Track:** Assembly / Ассемблер
**Slug:** `03-arithmetic`

## Task (EN)

1. Write a program that computes `(10 + 5) * 2 - (100 / 10)` and exits with the result.
   Expected: `(15) * 2 - (10) = 30 - 10 = 20`. Verify with `echo $?`.
2. Write a program that divides 100 by 7. Exit with the **remainder** (RDX).
   Expected: 100 / 7 = 14 remainder 2. Exit code should be 2.

## Задание (RU)

1. Напиши программу, вычисляющую `(10 + 5) * 2 - (100 / 10)`.
   Код возврата = результат. Проверь `echo $?`. Должно быть 20.
2. Напиши программу: 100 / 7. Код возврата = **остаток** (RDX).
   Должно быть 2 (100 / 7 = 14, остаток 2).

## Workflow

1. Read `docs/asm/en/03-*.md` and `docs/asm/ru/03-*.md`.
2. Write `solution.asm`.
3. Run `./test.sh`.
4. Mark complete.

## Tools

- `nasm`, `ld`
