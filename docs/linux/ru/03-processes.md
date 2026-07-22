# [3/10] Процессы

> **Track:** Системы Linux · **Level:** 3 · **Slug:** `03-processes`

## Цели

- Понять: Процессы
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

PID, parent, состояния. ps, top/htop, kill, jobs, fg/bg.

### Процессы
PID, дерево, сигналы. `SIGTERM` вежливый, `SIGKILL` — нет.

## Практика

sleep в фоне, найди PID, пошли SIGTERM.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-03`

```bash
cd /usr/local/xodex/courses/linux/level-03
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 7 hier`, `man 1 systemctl`

## Навигация

- Предыдущий: уровень 2
- Переходи к следующему номеру.
- Index: `docs/linux/ru/README.md`
