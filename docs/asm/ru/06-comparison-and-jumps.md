# [06] Сравнение и условные переходы

> **Трек:** Assembly · **Уровень:** 06 · **Сложность:** ★★★☆☆

## 1. Суть

Программы должны принимать решения: if/else, while, for. В ассемблере нет этих ключевых слов — строим из `cmp` + условных jump'ов.

## 2. cmp

`cmp a, b` вычисляет `a - b`, меняет флаги, **не меняет** регистры.

```assembly
cmp rax, rbx    ; rax - rbx, флаги обновлены, rax не изменён
```

### Флаги после cmp

| Ситуация | ZF | CF | SF | OF |
|----------|:--:|:--:|:--:|:--:|
| a == b | 1 | 0 | 0 | 0 |
| a < b (signed) | 0 | — | 1 | — |
| a < b (unsigned) | 0 | 1 | — | — |

## 3. Условные jump'ы

### Равенство
| Инструкция | Прыгает когда |
|------------|--------------|
| `je` / `jz` | ZF = 1 (равно / ноль) |
| `jne` / `jnz` | ZF = 0 (не равно) |

### Знаковые (signed)
| Инстр | Когда |
|-------|-------|
| `jg` | a > b (signed) |
| `jge` | a >= b |
| `jl` | a < b |
| `jle` | a <= b |

### Беззнаковые (unsigned)
| Инстр | Когда |
|-------|-------|
| `ja` | a > b (above) |
| `jae` | a >= b |
| `jb` | a < b (below) |
| `jbe` | a <= b |

### Безусловный: `jmp label`

## 4. test

`test rax, rax` — побитовое AND, меняет флаги, не меняет rax.
Идиоматическая проверка на ноль:

```assembly
test rax, rax
jz   .is_zero
```

## 5. Паттерны

### if
```assembly
cmp  rax, 0
jne  .after
mov  rbx, 1          ; выполняется если rax == 0
.after:
```

### if/else
```assembly
cmp  rax, 0
jne  .else
mov  rbx, 1
jmp  .after
.else:
mov  rbx, 2
.after:
```

### while
```assembly
.loop:
cmp  rax, 10
jge  .end
inc  rax
jmp  .loop
.end:
```

## 6. Пример: максимум в массиве

```assembly
section .data
    arr dd 17, 42, 8, 99, 23
    len equ 5

section .text
    global _start
_start:
    lea  rbx, [arr]
    mov  ecx, len
    mov  eax, [rbx]       ; текущий максимум
    dec  ecx
    add  rbx, 4
.loop:
    test ecx, ecx
    jz   .done
    mov  edx, [rbx]
    cmp  edx, eax
    jle  .skip
    mov  eax, edx
.skip:
    add  rbx, 4
    dec  ecx
    jmp  .loop
.done:
    mov  edi, eax
    mov  eax, 60
    syscall
```

## 7. Частые ошибки

- Использовать `jg` когда нужно `ja` (signed vs unsigned)
- Забыть `jmp` после if-body в if/else — fall-through в else
- Off-by-one в циклах
- `cmp rax, rbx; jg` — прыгает если `rax > rbx`, не наоборот