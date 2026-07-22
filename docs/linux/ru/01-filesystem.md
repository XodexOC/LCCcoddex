# [1/10] Иерархия ФС

> **Track:** Системы Linux · **Level:** 1 · **Slug:** `01-filesystem`

## Цели

- Понять: Иерархия ФС
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

FHS: /, /etc, /var, /home, /usr, /tmp, /proc, /sys. Права rwx.

### FHS
`/etc` конфиги, `/var` переменные данные, `/home` люди, `/proc` и `/sys` — интерфейсы ядра.

## Практика

Объясни права /etc/passwd и своего home.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-01`

```bash
cd /usr/local/xodex/courses/linux/level-01
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 7 hier`, `man 1 systemctl`

## Навигация

- Предыдущий: уровень 0
- Переходи к следующему номеру.
- Index: `docs/linux/ru/README.md`
