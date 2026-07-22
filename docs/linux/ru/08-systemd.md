# [8/10] systemd и сервисы

> **Track:** Системы Linux · **Level:** 8 · **Slug:** `08-systemd`

## Цели

- Понять: systemd и сервисы
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

units, systemctl status/start/enable. journalctl.

### systemd
Unit-файлы и drop-in’ы. Автологин Xodex — drop-in к getty.

## Практика

Изучи getty@tty1 и drop-in автологина Xodex.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-08`

```bash
cd /usr/local/xodex/courses/linux/level-08
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 7 hier`, `man 1 systemctl`

## Навигация

- Предыдущий: уровень 7
- Переходи к следующему номеру.
- Index: `docs/linux/ru/README.md`
