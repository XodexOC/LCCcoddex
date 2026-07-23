# [03] Арифметика

> **Трек:** Assembly · **Уровень:** 03 · **Сложность:** ★★☆☆☆

## 1. Какую проблему решаем?

Компьютеры созданы для счёта. У процессора есть инструкции для сложения, вычитания, умножения и деления.

## 2. Сложение и вычитание

### add
```assembly
add rax, 5        ; rax = rax + 5
add rbx, rcx      ; rbx = rbx + rcx
```

### sub
```assembly
sub rax, 5        ; rax = rax - 5
sub rbx, rcx      ; rbx = rbx - rcx
```

### inc и dec
```assembly
inc rax           ; rax = rax + 1
dec rbx           ; rbx = rbx - 1
```

### Флаги

После add/sub меняются флаги:
- **ZF** = 1, если результат 0
- **CF** = 1, если был перенос (результат не влез)
- **SF** = 1, если результат отрицательный
- **OF** = 1, если знаковое переполнение

```assembly
mov rax, 10
sub rax, 10        ; rax = 0 → ZF = 1

mov rax, 0xFFFFFFFFFFFFFFFF
add rax, 1         ; rax = 0, CF = 1 (перенос)
```

## 3. Умножение

### mul — беззнаковое

```assembly
mov rax, 5
mov rbx, 3
mul rbx            ; RAX = 5 * 3 = 15, RDX = 0
```

Операнд всегда в RAX. Результат в RAX (младшие 64 бита) и RDX (старшие).

### imul — знаковое

```assembly
mov rax, -5
mov rbx, 3
imul rbx           ; RAX = -15

imul rax, rbx      ; RAX = RAX * RBX
imul rax, rbx, 5   ; RAX = RBX * 5
```

## 4. Деление

### div — беззнаковое

```assembly
mov rax, 15        ; делимое
xor rdx, rdx       ; RDX = 0
mov rbx, 4         ; делитель
div rbx            ; RAX = 3 (частное), RDX = 3 (остаток)
```

**Важно:** всегда обнуляй RDX перед div!

### idiv — знаковое

```assembly
mov rax, -15
cqo                ; расширить знак RAX в RDX
mov rbx, 4
idiv rbx           ; RAX = -3, RDX = -3
```

**cqo** — Convert Quadword to Octaword: если RAX >= 0 → RDX = 0, если RAX < 0 → RDX = -1.

### Деление на ноль = SIGFPE

```assembly
mov rbx, 0
div rbx            ; FATAL: программа упадёт
```

## 5. Пример: вычисление выражения

```assembly
section .data
    expr db "((5 + 3) * 2) - (4 / 2) = ??", 10
    len_expr equ $ - expr

section .text
    global _start

_start:
    mov rax, 5
    add rax, 3          ; rax = 8
    mov rbx, 2
    mul rbx             ; rax = 16
    mov rcx, rax        ; сохранили

    mov rax, 4
    xor rdx, rdx
    mov rbx, 2
    div rbx             ; rax = 2

    sub rcx, rax        ; rcx = 14

    ; вывести строку
    mov rax, 1
    mov rdi, 1
    mov rsi, expr
    mov rdx, len_expr
    syscall

    ; exit(14)
    mov rax, 60
    mov rdi, 14
    syscall
```

## 6. Частые ошибки

- **Забыть xor rdx, rdx перед div** — результат будет неверным
- **Деление на 0** — программа упадёт
- **mul vs imul** — для отрицательных чисел используй imul
- **После syscall RAX меняется** — в нём возвращается количество записанных байт

## 7. Упражнения

1. 100 + 200, результат как код возврата. `echo $?` ?
2. 1000 - 333 - 111. Код возврата?
3. 7 * 8 * 9. Код возврата? (должно быть 504)
4. 100 / 7. Частное как код возврата.
5. (10 + 5) * 2 - (100 / 10). Код возврата?

## 8. Вопросы для самопроверки

- [ ] Как записывается сложение?
- [ ] Зачем перед div обнуляют RDX?
- [ ] Что такое ZF?
- [ ] Чем mul отличается от imul?
- [ ] Что делает cqo?

## 9. Что дальше?

Следующий урок — **сравнение и переходы**: if/else и циклы на ассемблере.
