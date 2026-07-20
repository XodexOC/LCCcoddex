# [6/10] Динамическая память

> **Track:** Программирование на C · **Level:** 6 · **Slug:** `06-memory`

## Цели

- Понять: Динамическая память
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

malloc/calloc/realloc/free. Владелец free? Утечки и double-free. Valgrind.

### Куча
Каждый успешный `malloc` — ровно один `free`. Valgrind ловит утечки и выход за границы.

## Практика

Динамический массив int (push). Проверь valgrind --leak-check=full.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-06`

```bash
cd /usr/local/xodex/courses/c/level-06
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Навигация

- Предыдущий: уровень 5
- Переходи к следующему номеру.
- Index: `docs/c/ru/README.md`
