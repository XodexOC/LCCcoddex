# [08] Соглашение о вызовах (System V AMD64 ABI)

> **Трек:** Assembly · **Уровень:** 08 · **Сложность:** ★★★☆☆

## 1. Суть

ABI — контракт: как функции вызывают друг друга, где аргументы, кто сохраняет регистры, выравнивание стека. Linux x86-64 использует **System V AMD64 ABI**.

## 2. Правила

### Аргументы (целые/указатели)

| № | Регистр |
|:-:|:-------:|
| 1 | `rdi` |
| 2 | `rsi` |
| 3 | `rdx` |
| 4 | `rcx` |
| 5 | `r8` |
| 6 | `r9` |
| 7+ | на стеке (справа налево) |

### Возврат

`rax` — целое/указатель (≤64 бит).
`rax:rdx` — 128-битное целое.

### Caller-saved (менять можно)

`rax`, `rcx`, `rdx`, `rsi`, `rdi`, `r8`, `r9`, `r10`, `r11`

### Callee-saved (сохранять обязательно)

`rbx`, `rbp`, `r12`, `r13`, `r14`, `r15`, `rsp`

### Выравнивание стека

Перед `call` RSP должен быть **16-байтно выровнен** (RSP % 16 == 0).

```
До call:           RSP % 16 == 0
После call (ret):  RSP % 16 == 8
После push rbp:    RSP % 16 == 0 (снова выровнен)
```

## 3. Пример: ABI-функция

```assembly
; int add_three(int a, int b, int c)
; rdi = a, rsi = b, rdx = c
add_three:
    push rbp
    mov  rbp, rsp
    mov  rax, rdi
    add  rax, rsi
    add  rax, rdx
    pop  rbp
    ret
```

## 4. Вызов функции из функции

```assembly
compute:
    push rbp
    mov  rbp, rsp
    push rdi              ; сохраняем x (caller-saved)
    call square           ; rax = square(x)
    pop  rdi
    mov  rcx, rdi
    shl  rcx, 1           ; rcx = x*2
    add  rax, rcx
    add  rax, 1
    pop  rbp
    ret
```

## 5. Аргументы с плавающей точкой

| № | Регистр |
|:-:|:-------:|
| 1-8 | `xmm0`–`xmm7` |

Возврат float/double: `xmm0`.

Перед `printf` (variadic) нужно `xor eax, eax` — указать 0 векторных аргументов.

## 6. Дополнительные аргументы на стеке

При 7+ аргументах остальные кладутся на стек справа налево перед `call`. После вызова caller должен восстановить RSP (`add rsp, N`).

## 7. cqo — знаковое расширение

```assembly
mov rax, -100
cqo               ; RDX = 0xFFFF... (знак RAX)
mov rbx, 3
idiv rbx          ; rax = -33, rdx = -1
```

Для `div` (беззнаковое): `xor edx, edx` перед делением.

## 8. Частые ошибки

- Не сохранять rbx/r12-r15 в функциях, вызываемых из C
- Нарушение выравнивания стека перед call
- Забыть `xor eax, eax` перед printf
- Использовать `_start` вместо `main` в смешанных проектах