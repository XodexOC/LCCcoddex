# [10/10] Системный C (итог)

> **Track:** Программирование на C · **Level:** 10 · **Slug:** `10-systems-c`

## Цели

- Понять: Системный C (итог)
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

Системные вызовы через libc, процессы (fork/exec), сигналы, man 2/3.

### Итог: мини-shell
Строки + память + `fork`/`execvp`/`waitpid`. Мост к треку **linux**.

## Практика

Мини-shell: read, fork, execvp, wait. Пустой ввод обрабатывать.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-10`

```bash
cd /usr/local/xodex/courses/c/level-10
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Навигация

- Предыдущий: уровень 9
- Итог пройден — вернись к ранним лабам с gdb/valgrind/strace.
- Index: `docs/c/ru/README.md`
