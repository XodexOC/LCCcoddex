# [10] Capstone — C + Assembly

> **Трек:** Assembly · **Уровень:** 10 · **Сложность:** ★★★☆☆

## 1. Суть

Реальный мир использует C для логики и Assembly для низкоуровневой оптимизации. Нужно уметь вызывать C из asm и asm из C.

## 2. global и extern

```assembly
global my_func      ; my_func видна другим .o файлам
extern printf       ; printf определена в libc (линкер найдёт)
```

C не искажает имена функций (no name mangling). C++ — искажает, если не указан `extern "C"`.

## 3. main vs _start

Чистый asm: `_start` (точка входа от OC).
Смешанный проект: `main` (CRT инициализирует libc, вызывает main).

## 4. Компиляция смешанного проекта

```bash
nasm -f elf64 func.asm -o func.o
gcc -c main.c -o main.o
gcc main.o func.o -o program
```

## 5. Вызов printf из asm

```assembly
section .data
    msg db "Count: %d", 10, 0
    val dq 42

section .text
    global main
    extern printf

main:
    push rbp
    mov  rbp, rsp
    mov  rdi, msg
    mov  rsi, [val]
    xor  eax, eax      ; 0 float-аргументов
    call printf
    xor  eax, eax
    pop  rbp
    ret
```

## 6. Вызов asm функции из C

```asm
; multiply.asm
global multiply
multiply:
    push rbp
    mov  rbp, rsp
    mov  rax, rdi
    imul rax, rsi
    pop  rbp
    ret
```

```c
// main.c
extern int multiply(int a, int b);
int main() {
    int r = multiply(6, 7);  // 42
    return 0;
}
```

## 7. Inline assembly (GCC)

```c
asm ("addl %%ebx, %%eax;"
    : "=a" (result)
    : "a" (a), "b" (b));
```

## 8. Когда использовать asm сегодня

**Использовать:**
- Загрузчики и ядра ОС
- Детектирование CPU (`cpuid`, `rdtsc`)
- Обработчики прерываний
- SIMD-оптимизация (AVX/SSE)

**Не использовать:**
- Обычный прикладной код (компиляторы оптимизируют лучше)
- Когда нужна переносимость
- Быстрое прототипирование

**Золотое правило:** пиши на C, профилируй, переписывай горячие 1-5% на asm — и измеряй ускорение.

## 9. Частые ошибки

- Забыть `xor eax, eax` перед variadic функциями (printf)
- Не сохранять callee-saved регистры в asm-функции для C
- Использовать `_start` вместо `main` в смешанном проекте
- Забыть флаг `-no-pie` при линковке с GCC

## 10. Что ты выучил за 10 уровней

| Ур. | Тема |
|:---:|------|
| 00 | Как работает компьютер |
| 01 | Первая программа, syscall |
| 02 | Регистры и mov |
| 03 | Арифметика |
| 04 | Память и .data |
| 05 | Режимы адресации |
| 06 | Сравнение и переходы |
| 07 | Стек и подпрограммы |
| 08 | Соглашение о вызовах |
| 09 | Строки и REP |
| 10 | C + Assembly |

Ты понимаешь архитектуру компьютера на фундаментальном уровне. Каждый `if`, `for` и вызов функции в C теперь отображается на инструкции, которые ты писал.