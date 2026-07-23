# Lab 04: Память: .data / Memory: .data

**Track:** Assembly / Ассемблер
**Slug:** `04-memory-basics`

## Task (EN)

1. Declare an array `arr dd 7, 14, 21, 28, 35` in `.data`. Read `arr[3]` (index 3) into RAX and exit with it as the exit code. Should be 28.
2. Declare a string `msg db "Xodex OS", 10`. Print it using write syscall.
3. (Bonus) Declare two arrays `a dd 1, 2, 3` and `b dd 4, 5, 6`. Compute a[0] + b[0] + a[1] + b[1] + a[2] + b[2] and exit with the result. Should be 21.

## Задание (RU)

1. Объяви массив `arr dd 7, 14, 21, 28, 35` в `.data`. Прочитай `arr[3]` (индекс 3) в RAX, выйди с этим кодом. Должно быть 28.
2. Объяви строку `msg db "Xodex OS", 10`. Выведи через write.
3. (Бонус) Два массива: `a dd 1,2,3` и `b dd 4,5,6`. Сложи a[0]+b[0]+a[1]+b[1]+a[2]+b[2]. Код возврата = сумма (должно быть 21).

## Workflow

1. Read `docs/asm/en/04-*.md` and `docs/asm/ru/04-*.md`.
2. Write `solution.asm`.
3. Run `./test.sh`.
4. Mark complete.

## Tools

- `nasm`, `ld`, `echo $?`
