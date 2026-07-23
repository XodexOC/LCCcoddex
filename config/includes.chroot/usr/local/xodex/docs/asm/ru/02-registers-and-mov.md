# [02] Регистры и mov

> **Трек:** Assembly · **Уровень:** 02 · **Сложность:** ★☆☆☆☆

## 1. Какую проблему решаем?

В прошлом уроке строка была жёстко задана. Чтобы манипулировать данными, нужно понимать **регистры** — ячейки внутри процессора, где живут данные. И инструкцию **mov** — главный способ перемещать данные.

## 2. Все регистры 64-битного процессора

```
64-битный     32-битный     16-битный   8-бит (ст.) 8-бит (мл.)
──────────    ──────────    ──────────   ──────────  ──────────
RAX           EAX           AX           AH          AL
RBX           EBX           BX           BH          BL
RCX           ECX           CX           CH          CL
RDX           EDX           DX           DH          DL
RSI           ESI           SI           ─           SIL
RDI           EDI           DI           ─           DIL
RBP           EBP           BP           ─           BPL
RSP           ESP           SP           ─           SPL
R8-R15        R8D-R15D      R8W-R15W     ─           R8B-R15B
```

**Важное правило:** при записи в EAX старшие 32 бита RAX **обнуляются**. При записи в AX или AL — не трогаются.

## 3. Инструкция mov

```
mov назначение, источник
mov rax, 5        ; imm → reg
mov rbx, rax      ; reg → reg
mov rcx, [addr]   ; mem → reg
mov [addr], rdx   ; reg → mem
mov [addr], 42    ; imm → mem
mov [x], [y]      ; ❌ НЕЛЬЗЯ (mem→mem)
```

### mov imm → reg
```assembly
mov rax, 42       ; rax = 42
mov al, 10        ; al = 10
```

### mov reg → reg
```assembly
mov rax, rbx      ; скопировать rbx в rax
```
После копирования в обоих регистрах одно и то же. Исходный не меняется.

### Части регистров
```assembly
mov rax, 0xFFFFFFFFFFFFFFFF   ; RAX = все 64 бита = 1
mov eax, 0                   ; RAX = 0 (старшие 32 бита обнулились!)
mov ax, 42                   ; RAX = 42 (младшие 16 бит)
```

### Квадратные скобки: память
```assembly
section .data
    my_var dq 42

section .text
    mov rax, my_var      ; rax = АДРЕС (например, 0x601000)
    mov rbx, [my_var]    ; rbx = ЗНАЧЕНИЕ (42)
```

**Без скобок** — адрес. **Со скобками** — значение по адресу.

### Соответствие размеров

```assembly
mov al, [b]    ; 1 байт → 8-битный регистр
mov ax, [w]    ; 2 байта → 16-битный
mov eax, [d]   ; 4 байта → 32-битный
mov rax, [q]   ; 8 байт → 64-битный
```

## 4. Программа

```assembly
section .data
    msg db "RAX = ", 0
    newline db 10

section .text
    global _start

_start:
    mov rax, 42
    mov rbx, 100
    mov rcx, 0xFF

    mov rdx, rax        ; rdx = 42

    mov rax, 1          ; write
    mov rdi, 1          ; stdout
    mov rsi, msg
    mov rdx, 6
    syscall

    mov rax, 1          ; write newline
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall

    mov rax, 60         ; exit(0)
    xor rdi, rdi
    syscall
```

## 5. Частые ошибки

- `mov rax, var` vs `mov rax, [var]` — адрес vs значение
- `mov [x], [y]` — нельзя, через регистр: `mov rax, [y]; mov [x], rax`
- Писать 8 байт в 1-байтовую переменную — порча соседней памяти

## 6. Упражнения

1. Положи в RAX=10, RBX=20, RCX=30. Скопируй RAX в RDX. Выведи строку.
2. Напиши: RAX = 0xFFFFFFFFFFFFFFFF, обнули через EAX. Чему равен RAX?
3. RAX=0, AL=10, AH=20. Чему равен AX? (подсказка: AH — второй байт, AL — первый)

## 7. Вопросы для самопроверки

- [ ] Сколько бит в RAX? EAX? AX? AL?
- [ ] Что происходит со старшими 32 битами при записи в EAX?
- [ ] Чем отличается `mov rax, addr` от `mov rax, [addr]`?
- [ ] Как скопировать значение из одной переменной в другую?
- [ ] Почему нельзя `mov [x], [y]`?

## 8. Что дальше?

Следующий урок — арифметика: add, sub, mul, div, флаги ZF/CF.
