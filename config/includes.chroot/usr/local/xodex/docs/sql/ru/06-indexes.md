# [6/10] Индексы

> **Track:** SQL и данные · **Level:** 6 · **Slug:** `06-indexes`

## Цели

- Понять: Индексы
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

B-tree. CREATE INDEX. Когда индекс помогает и мешает.

### Индексы
Ускоряют чтение, замедляют запись. Смотри `EXPLAIN QUERY PLAN`.

## Практика

EXPLAIN QUERY PLAN до/после индекса.

**Live paths:**
- Examples: `/usr/local/xodex/examples/sql`
- Lab: `/usr/local/xodex/courses/sql/level-06`

```bash
cd /usr/local/xodex/courses/sql/level-06
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- https://www.sqlite.org/docs.html

## Навигация

- Предыдущий: уровень 5
- Переходи к следующему номеру.
- Index: `docs/sql/ru/README.md`
