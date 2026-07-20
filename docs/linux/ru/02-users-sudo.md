# [2/10] Пользователи и sudo

> **Track:** Системы Linux · **Level:** 2 · **Slug:** `02-users-sudo`

## Цели

- Понять: Пользователи и sudo
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

UID/GID, /etc/passwd, группы, sudo. Почему не жить под root.

### Минимальные привилегии
Работаешь как `student`, `sudo` — точечно. В Xodex Live sudo без пароля для удобства класса.

## Практика

Под student выполни sudo и посмотри /etc/sudoers.d/xodex.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-02`

```bash
cd /usr/local/xodex/courses/linux/level-02
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 7 hier`, `man 1 systemctl`

## Навигация

- Предыдущий: уровень 1
- Переходи к следующему номеру.
- Index: `docs/linux/ru/README.md`
