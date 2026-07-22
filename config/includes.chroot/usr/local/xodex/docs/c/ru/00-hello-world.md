# [0/10] Hello World и toolchain

> **Track:** Программирование на C · **Level:** 0 · **Slug:** `00-hello-world`

## Цели

- Понять: Hello World и toolchain
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

C — язык системного программирования. Исходник → компиляция → запуск бинарника.

### Шаги toolchain
1. **Препроцессор** раскрывает `#include` / `#define`.
2. **Компилятор** переводит C в ассемблер.
3. **Ассемблер** даёт объектный код (`.o`).
4. **Линковщик** собирает исполняемый файл.

```bash
gcc -Wall -Wextra -O0 -g -o hello hello.c
./hello
```

### Зачем C
Близко к модели машины: память — байты, контроль явный, ABI стабилен. Сила = ответственность. Учись с `gdb` и `valgrind`.

## Практика

Скомпилируй и запусти hello.c. Кратко объясни роль gcc, as и ld.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-00`

```bash
cd /usr/local/xodex/courses/c/level-00
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Навигация

- Это входной уровень (0).
- Переходи к следующему номеру.
- Index: `docs/c/ru/README.md`
