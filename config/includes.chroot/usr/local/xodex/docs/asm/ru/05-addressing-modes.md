# [05] Режимы адресации

> **Трек:** Assembly · **Уровень:** 05 · **Сложность:** ★★★☆☆

## 1. Режимы адресации

Способы указать процессору адрес памяти:

| Режим | Пример | Адрес |
|-------|--------|-------|
| Direct | `[val]` | val |
| Register indirect | `[rax]` | RAX |
| Base + disp | `[rax + 10]` | RAX + 10 |
| Indexed | `[arr + rsi*4]` | arr + RSI×4 |
| Full | `[rbx + rsi*4 + 10]` | RBX + RSI×4 + 10 |

**Формула:** `Адрес = База + Индекс × Масштаб + Смещение`

Масштаб: только 1, 2, 4, 8.

## 2. Register indirect

```assembly
mov rbx, val          ; rbx = адрес val (0x601000)
mov rax, [rbx]        ; rax = значение по адресу rbx = 42
```

`[rbx]` — зайди по адресу, который в RBX, возьми значение.

## 3. Base + displacement

```assembly
mov rbx, arr
mov eax, [rbx]        ; arr[0]
mov eax, [rbx + 4]    ; arr[1]
mov eax, [rbx + 8]    ; arr[2]
```

## 4. Indexed

```assembly
mov rsi, 2
mov eax, [arr + rsi*4]  ; arr[2]
```

Индекс в регистре, масштаб = размер элемента.

## 5. LEA — Load Effective Address

`lea` вычисляет адрес, **не читая память**:

```assembly
lea rax, [rbx + rsi*4 + 10]   ; rax = rbx + rsi*4 + 10
lea rax, [rcx + rcx*2]         ; rax = rcx * 3
lea rax, [rcx*8]               ; rax = rcx * 8
```

`lea rax, [rbx]` — просто скопировать адрес (аналог `mov rax, rbx`).
`mov rax, [rbx]` — **прочитать** память по адресу rbx.

## 6. Частые ошибки

- Путать `mov rax, [rbx]` (чтение) и `mov rax, rbx` (копия адреса)
- Забыть масштаб: `[arr + rsi]` вместо `[arr + rsi*4]`
- RSP нельзя использовать как индекс
- LEA никогда не читает память

## 7. Упражнения

1. Объяви `val dq 99`, прочитай через `[rbx]` с register indirect.
2. Объяви `arr dd 5, 10, 15, 20, 25`. Прочитай arr[4] через base+disp.
3. Используя `[arr + rsi*4]` с rsi = 2, прочитай arr[2].
4. Вычисли `rax = rcx*4 + rdx + 10` через одну LEA.