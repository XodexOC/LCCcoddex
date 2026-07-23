# [09] Строки и REP-инструкции

> **Трек:** Assembly · **Уровень:** 09 · **Сложность:** ★★★☆☆

## 1. Суть

x86-64 имеет специальные строковые инструкции для работы с памятью. Они используют `RSI` (source), `RDI` (destination), `RCX` (счётчик).

## 2. Регистры

- `RSI` — Source Index (откуда читаем)
- `RDI` — Destination Index (куда пишем)
- `RCX` — счётчик для `rep`
- `AL`/`AX`/`EAX`/`RAX` — аккумулятор для lods/stos/scas

## 3. Флаг направления (DF)

| Инструкция | Действие |
|:----------:|:--------:|
| `cld` | DF=0, RSI/RDI увеличиваются (вперёд) |
| `std` | DF=1, RSI/RDI уменьшаются (назад) |

Всегда ставьте `cld` перед строковыми операциями.

## 4. Основные инструкции

| Инстр | Что делает | RSI/RDI |
|:-----:|:-----------|:-------:|
| `lodsb` | `al = [rsi]` | RSI++ |
| `stosb` | `[rdi] = al` | RDI++ |
| `movsb` | `[rdi] = [rsi]` | RSI++, RDI++ |
| `scasb` | сравнить `al` с `[rdi]` | RDI++ |
| `cmpsb` | сравнить `[rsi]` с `[rdi]` | RSI++, RDI++ |

Варианты: `b`=1, `w`=2, `d`=4, `q`=8 байт.

## 5. REP-префиксы

| Префикс | Условие повторения |
|:-------:|:------------------|
| `rep` | пока RCX > 0 |
| `repe` / `repz` | пока RCX > 0 **и** ZF = 1 |
| `repne` / `repnz` | пока RCX > 0 **и** ZF = 0 |

## 6. strlen

```assembly
strlen:
    push rbp
    mov  rbp, rsp
    cld
    mov  rcx, -1
    xor  al, al
    repne scasb        ; ищем нуль-байт
    not  rcx
    dec  rcx           ; rcx = длина
    mov  rax, rcx
    pop  rbp
    ret
```

## 7. Примеры

### rep stosb — заполнить буфер

```assembly
lea  rdi, [buffer]
mov  al, 'A'
mov  rcx, 256
rep  stosb
```

### rep movsb — копировать

```assembly
lea  rsi, [src]
lea  rdi, [dst]
mov  rcx, 64
rep  movsb
```

### repne scasb — поиск символа

```assembly
lea  rdi, [msg]
mov  al, 'l'
mov  rcx, -1
repne scasb           ; ZF=1 если найден
```

## 8. Частые ошибки

- Забыть `cld` — DF может быть 1 (обратное направление)
- Перепутать RSI (source) и RDI (destination)
- `repe scasb` ищет НЕСОВПАДЕНИЕ; `repne scasb` ищет СОВПАДЕНИЕ
- Не включить нуль-терминатор в длину для strcpy