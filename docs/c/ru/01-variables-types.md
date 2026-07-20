# [1/10] Переменные и типы

> **Track:** Программирование на C · **Level:** 1 · **Slug:** `01-variables-types`

## Цели

- Понять: Переменные и типы
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

Целые, float, char. Важен размер: sizeof, signed/unsigned, integer promotion.

### Ширина типов
`int` обычно 32 бита. Для бинарных форматов бери `<stdint.h>`.

Знаковое переполнение — UB. На unsigned переполнение определено (по модулю).

## Практика

Выведи sizeof для int, long, size_t, char. Предскажи переполнение unsigned char.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-01`

```bash
cd /usr/local/xodex/courses/c/level-01
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Навигация

- Предыдущий: уровень 0
- Переходи к следующему номеру.
- Index: `docs/c/ru/README.md`
