# [5/10] Массивы и строки

> **Track:** Программирование на C · **Level:** 5 · **Slug:** `05-arrays-strings`

## Цели

- Понять: Массивы и строки
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

Массив «сжимается» к указателю. Строки C — char* с NUL. Переполнения буфера реальны.

### Массивы и строки
C-строка заканчивается `\0`. `sizeof` в функции не даёт длину массива вызывающего. `gets` запрещён; предпочитай `snprintf`.

## Практика

Реализуй safe_strlen и разворот строки in-place.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-05`

```bash
cd /usr/local/xodex/courses/c/level-05
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Навигация

- Предыдущий: уровень 4
- Переходи к следующему номеру.
- Index: `docs/c/ru/README.md`
