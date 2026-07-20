# [7/10] Структуры и layout

> **Track:** Программирование на C · **Level:** 7 · **Slug:** `07-structs`

## Цели

- Понять: Структуры и layout
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

struct, typedef, padding, alignment. Вложенные struct. Opaque pointer в API.

### Layout
Компилятор вставляет padding. Порядок полей влияет на `sizeof`. Смотри `offsetof`.

## Практика

Point и Rectangle; площадь; sizeof и offsetof.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-07`

```bash
cd /usr/local/xodex/courses/c/level-07
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Навигация

- Предыдущий: уровень 6
- Переходи к следующему номеру.
- Index: `docs/c/ru/README.md`
