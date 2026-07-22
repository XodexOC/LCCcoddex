# [8/10] Файлы и ввод-вывод

> **Track:** Программирование на C · **Level:** 8 · **Slug:** `08-files-io`

## Цели

- Понять: Файлы и ввод-вывод
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

fopen/fread/fwrite/fclose. Текст vs бинарный. errno. Дескрипторы vs FILE*.

### Потоки ввода-вывода
Проверяй коды возврата. Позже сравнишь `FILE*` с дескрипторами (`open`/`read`).

## Практика

Скопируй файл побайтно. Ошибки через perror.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/c/level-08`

```bash
cd /usr/local/xodex/courses/c/level-08
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 1 gcc`, `man 3 printf`, https://en.cppreference.com/w/c/language

## Навигация

- Предыдущий: уровень 7
- Переходи к следующему номеру.
- Index: `docs/c/ru/README.md`
