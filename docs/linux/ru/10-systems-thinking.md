# [10/10] Системное мышление (итог)

> **Track:** Системы Linux · **Level:** 10 · **Slug:** `10-systems-thinking`

## Цели

- Понять: Системное мышление (итог)
- Выполнить лабораторную
- Знать, какие man/docs открыть дальше

## Теория

Live boot (kernel, initrd, squashfs). Наблюдаемость. Дальше: контейнеры, серверы.

### Итог
Пойми Live: kernel + initrd + squashfs. Эксперименты могут исчезнуть после reboot — это нормально для обучения.

## Практика

Кратко опиши путь загрузки Xodex от ISO до login.

**Live paths:**
- Examples: `/usr/local/xodex/examples/c`
- Lab: `/usr/local/xodex/courses/linux/level-10`

```bash
cd /usr/local/xodex/courses/linux/level-10
./test.sh
```

## Самопроверка

- [ ] Объяснить тему без конспекта
- [ ] Упражнение выполнено
- [ ] Назвать один сбой без проверок

## Дальше

- `man 7 hier`, `man 1 systemctl`

## Навигация

- Предыдущий: уровень 9
- Итог пройден — вернись к ранним лабам с gdb/valgrind/strace.
- Index: `docs/linux/ru/README.md`
