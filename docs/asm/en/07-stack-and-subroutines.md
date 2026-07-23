# [07] The Stack and subroutines

> **Track:** Assembly · **Level:** 07 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

So far we write all code in one flat `_start` block. As programs grow, this becomes impossible to manage:

```assembly
; Without subroutines — everything duplicated:
_start:
    ; print "Hello"
    mov  rax, 1
    mov  rdi, 1
    mov  rsi, hello_msg
    mov  rdx, 5
    syscall

    ; ... some other code ...

    ; print "World" — same syscall again!
    mov  rax, 1
    mov  rdi, 1
    mov  rsi, world_msg
    mov  rdx, 5
    syscall
```

We need:
1. **Subroutines (functions)** — reusable blocks of code we can "call" from anywhere
2. **The stack** — temporary storage for return addresses, local variables, and saved registers
3. **A calling mechanism** — `call` jumps to a subroutine and remembers where to return; `ret` returns

## 2. Core concept (absolute zero)

### 2.1 What is the stack?

The stack is a **LIFO** (Last In, First Out) data structure in memory — like a stack of plates:
- You **push** a plate onto the top
- You **pop** a plate from the top
- You can't take a plate from the middle without removing everything above it

```
Empty stack     Push 10         Push 20         Push 30          Pop → 30
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      ┌─────────┐
│         │    │         │    │         │    │   30    │ ←TOP  │         │
│         │    │         │    │   20    │    │   20    │      │   20    │
│         │    │   10    │    │   10    │    │   10    │      │   10    │
└─────────┘    └─────────┘    └─────────┘    └─────────┘      └─────────┘
```

In x86-64, the stack:
- Lives in regular RAM (main memory)
- Grows **downward** (toward lower addresses)
- Is tracked by **RSP** (Stack Pointer) — a register that holds the address of the top of the stack

```
High addresses
    ┌──────────────┐
    │   ... data ...  │
    ├──────────────┤
    │   stack grows   │ ← RSP points here (top of stack)
    │   downward      │
    ▼                 │
    │                 │
    └──────────────┘
Low addresses
```

### 2.2 `push` — push onto stack

```assembly
push rax    ; decrements RSP by 8, then stores rax at [RSP]
```

Equivalent to:
```assembly
sub rsp, 8
mov [rsp], rax
```

```
Before: RSP = 0x1000, rax = 42
After:  RSP = 0x0FF8, memory[0x0FF8] = 42
```

You can push:
- 64-bit register: `push rax`
- 64-bit memory: `push [mem]`
- 64-bit immediate: `push 100` (encoded as 32-bit sign-extended)

### 2.3 `pop` — pop from stack

```assembly
pop rax     ; loads 8 bytes from [RSP] into rax, then increments RSP by 8
```

Equivalent to:
```assembly
mov rax, [rsp]
add rsp, 8
```

```
Before: RSP = 0x0FF8, memory[0x0FF8] = 42
After:  RSP = 0x1000, rax = 42
```

### 2.4 `call` — call a subroutine

`call` does two things:
1. **Pushes the return address** (the address of the instruction right after the `call`) onto the stack
2. **Jumps** to the target label

```assembly
call my_func    ; push address of next instruction; jump to my_func
```

Equivalent to:
```assembly
push next_ip    ; (not a real instruction — conceptual)
jmp  my_func
next_ip:
```

### 2.5 `ret` — return from subroutine

`ret` does the reverse of `call`:
1. **Pops** the return address from the stack
2. **Jumps** to that address

```assembly
ret    ; pop rip; jump to [old rsp]
```

Equivalent to:
```assembly
pop rip         ; (not a real instruction — conceptual)
```

### 2.6 The stack frame pattern

When you write a subroutine, the standard prologue and epilogue look like:

```assembly
my_func:
    ; ─── prologue ───
    push rbp          ; save old base pointer on stack
    mov  rbp, rsp    ; set new base pointer = current stack top

    ; ... function body (using rbp-relative addressing for locals) ...

    ; ─── epilogue ───
    pop rbp           ; restore old base pointer
    ret               ; return to caller
```

**Why?** `rbp` (base pointer) gives us a fixed reference point. Inside the function, `rsp` changes as we push/pop, but `rbp` stays constant. Local variables are at `[rbp - N]`, parameters (from the caller) are at `[rbp + N]`.

```
Stack layout during a function call:

High addresses
┌──────────────────────┐
│   ... caller's data ... │
├──────────────────────┤
│   return address      │ ← pushed by call
├──────────────────────┤
│   saved RBP           │ ← pushed by push rbp; RBP points here
├──────────────────────┤ ← RBP = RSP after mov rbp, rsp
│   local variables     │ ← accessed as [rbp - 8], [rbp - 16], etc.
│   (subtract from RSP) │
├──────────────────────┤ ← RSP points here
Low addresses
```

### 2.7 Local variables on the stack

To reserve space for local variables, subtract from RSP:

```assembly
my_func:
    push rbp
    mov  rbp, rsp
    sub  rsp, 32        ; reserve 32 bytes for local vars

    ; [rbp - 8]   = first local (8 bytes)
    ; [rbp - 16]  = second local
    ; [rbp - 24]  = third local
    ; [rbp - 32]  = fourth local

    mov  [rbp - 8], rbx    ; save rbx into local var

    mov  rsp, rbp
    pop  rbp
    ret
```

### 2.8 Preserving registers

When you call a subroutine, you must assume that some registers might be modified. The convention (we'll formalize this in lesson 08) is:

- **Caller-saved:** rax, rcx, rdx, rsi, rdi, r8-r11 — the callee can freely modify these
- **Callee-saved:** rbx, rbp, r12-r15 — if the callee wants to use these, it must save and restore them

Simple rule for now: **if your subroutine uses a register, save it with `push` at the start and `pop` at the end** (in reverse order):

```assembly
my_func:
    push rbx          ; save rbx
    push r12          ; save r12

    ; ... use rbx and r12 freely ...

    pop  r12          ; restore in reverse order
    pop  rbx
    ret
```

### 2.9 The red zone (Linux ABI)

The System V AMD64 ABI (Linux) defines a **red zone** of 128 bytes below RSP. This is memory that:
- Is not used by signal handlers or interrupt handlers
- Is safe for temporary use without adjusting RSP
- Only applies at the leaf level (functions that don't call other functions)

```assembly
leaf_func:
    ; Can use [rsp - 8], [rsp - 16], ... [rsp - 128] safely
    mov  [rsp - 8], rax    ; safe — within red zone
    ; ... do work ...
    ret                    ; no need to restore RSP
```

**Warning:** If your function calls another function, the red zone is NOT safe (the called function's `call` will overwrite it). For now, just use proper stack frames.

## 3. Step-by-step breakdown

### 3.1 First subroutine: a simple function

```assembly
; subroutine.asm — first subroutine
section .text
    global _start

_start:
    mov  rax, 10
    call print_value      ; call subroutine
    ; returns here after ret

    mov  rax, 20
    call print_value      ; call again

    mov  eax, 60
    xor  edi, edi
    syscall

; Subroutine: print_value
; Prints the value in rax using sys_write (for demo)
print_value:
    push rbp
    mov  rbp, rsp

    ; We're just using rax (already set by caller)
    ; This is a simplified example

    pop  rbp
    ret
```

### 3.2 Subroutine with argument passing via registers

```assembly
; calc.asm — subroutines with register arguments
section .text
    global _start

_start:
    mov  rdi, 5          ; first argument
    mov  rsi, 3          ; second argument
    call add_values      ; result in rax
    ; rax = 8

    mov  rdi, 10
    mov  rsi, 4
    call sub_values      ; result in rax
    ; rax = 6

    mov  eax, 60
    xor  edi, edi
    syscall

; int add_values(int a, int b) — returns a + b
; Arguments: rdi = a, rsi = b
; Returns:   rax = a + b
add_values:
    push rbp
    mov  rbp, rsp
    mov  rax, rdi
    add  rax, rsi
    pop  rbp
    ret

; int sub_values(int a, int b) — returns a - b
sub_values:
    push rbp
    mov  rbp, rsp
    mov  rax, rdi
    sub  rax, rsi
    pop  rbp
    ret
```

### 3.3 Subroutine calling another subroutine

```assembly
; nested.asm — subroutines calling subroutines
section .text
    global _start

_start:
    mov  rdi, 6
    mov  rsi, 2
    call divide          ; rax = 6 / 2 = 3

    mov  edi, eax        ; exit code = 3
    mov  eax, 60
    syscall

; int divide(int a, int b)
; Returns a / b using repeated subtraction
divide:
    push rbp
    mov  rbp, rsp
    push rbx             ; save rbx (callee-saved)

    xor  eax, eax        ; quotient = 0
    mov  ebx, edi        ; ebx = a (dividend)
    mov  ecx, esi        ; ecx = b (divisor)

.loop:
    cmp  ebx, ecx
    jl   .done           ; if dividend < divisor, done
    sub  ebx, ecx        ; dividend -= divisor
    inc  eax             ; quotient++
    jmp  .loop

.done:
    ; rax = quotient, ebx = remainder
    pop  rbx
    pop  rbp
    ret
```

### 3.4 Stack frame with local variables

```assembly
; locals.asm — using local variables on the stack
section .text
    global _start

_start:
    mov  rdi, 10
    call square_and_double
    ; rax should be 200

    mov  edi, eax
    mov  eax, 60
    syscall

; int square_and_double(int x)
; Returns (x * x) * 2
square_and_double:
    push rbp
    mov  rbp, rsp
    sub  rsp, 16         ; reserve 2 local variables (8 bytes each)

    ; [rbp - 8] = temp1 (x * x)
    ; [rbp - 16] = temp2 (result)

    mov  [rbp - 8], rdi     ; save input
    mov  rax, rdi
    imul rax, rdi            ; rax = x * x
    mov  [rbp - 8], rax      ; temp1 = x * x

    mov  rax, [rbp - 8]
    shl  rax, 1              ; multiply by 2 (shift left)
    mov  [rbp - 16], rax     ; temp2 = (x*x) * 2

    mov  rax, [rbp - 16]     ; return value

    mov  rsp, rbp
    pop  rbp
    ret
```

### 3.5 Recursive function: factorial

```assembly
; factorial.asm — recursive factorial
section .text
    global _start

_start:
    mov  rdi, 5
    call factorial       ; rax = 5! = 120

    mov  edi, eax        ; exit code = 120
    mov  eax, 60
    syscall

; int factorial(int n)
; Returns n * factorial(n-1), base case n <= 1 returns 1
factorial:
    push rbp
    mov  rbp, rsp

    ; Base case: if n <= 1, return 1
    cmp  rdi, 1
    jle  .base_case

    ; Recursive case: n * factorial(n-1)
    push rdi             ; save n

    dec  rdi             ; n - 1
    call factorial       ; rax = factorial(n-1)

    pop  rdi             ; restore n
    imul rax, rdi        ; rax = n * factorial(n-1)

    pop  rbp
    ret

.base_case:
    mov  rax, 1
    pop  rbp
    ret
```

### 3.6 Preserving multiple registers

```assembly
; preserve.asm — correct register preservation
section .text
    global _start

_start:
    mov  rbx, 100        ; rbx = 100
    mov  r12, 200        ; r12 = 200

    call my_func

    ; rbx and r12 should still be 100 and 200
    ; (because my_func preserves them)

    mov  edi, ebx        ; exit code = 100
    mov  eax, 60
    syscall

my_func:
    push rbp
    mov  rbp, rsp
    push rbx             ; preserve rbx
    push r12             ; preserve r12

    ; Use rbx and r12 for our own purposes
    mov  rbx, 1
    mov  r12, 2
    ; ... do work with rbx and r12 ...

    pop  r12             ; restore r12 (reverse order!)
    pop  rbx             ; restore rbx
    pop  rbp
    ret
```

## 4. Complete program: modular calculator

```assembly
; calculator.asm — modular program with 4 subroutines
section .data
    num1 dq 25
    num2 dq 7

section .text
    global _start

_start:
    mov  rdi, [num1]
    mov  rsi, [num2]

    call add_sub         ; rax = num1 + num2
    call sub_sub         ; rax = num1 - num2
    call mul_sub         ; rax = num1 * num2
    call div_sub         ; rax = num1 / num2

    ; exit with code = division result
    mov  edi, eax
    mov  eax, 60
    syscall

; All subroutines follow the same pattern:
; Arguments: rdi = a, rsi = b
; Returns:   rax = result

add_sub:
    push rbp
    mov  rbp, rsp
    mov  rax, rdi
    add  rax, rsi
    pop  rbp
    ret

sub_sub:
    push rbp
    mov  rbp, rsp
    mov  rax, rdi
    sub  rax, rsi
    pop  rbp
    ret

mul_sub:
    push rbp
    mov  rbp, rsp
    mov  rax, rdi
    imul rax, rsi
    pop  rbp
    ret

div_sub:
    push rbp
    mov  rbp, rsp
    push rbx

    xor  edx, edx       ; clear rdx (high 64 bits of dividend)
    mov  rax, rdi        ; dividend
    mov  rbx, rsi        ; divisor
    div  rbx             ; rax = quotient

    pop  rbx
    pop  rbp
    ret
```

## 5. Complete program: array sum with subroutine

```assembly
; array_sum.asm — modular array processing
section .data
    arr     dd 10, 20, 30, 40, 50
    arr_len equ 5

section .text
    global _start

_start:
    lea  rdi, [arr]      ; arg1: array pointer
    mov  rsi, arr_len    ; arg2: array length
    call sum_array       ; rax = sum

    mov  edi, eax        ; exit code = 150
    mov  eax, 60
    syscall

; int sum_array(int* arr, int len)
; Returns sum of all elements
sum_array:
    push rbp
    mov  rbp, rsp
    push rbx             ; preserve rbx
    push rcx             ; preserve rcx

    xor  eax, eax        ; sum = 0
    xor  ecx, ecx        ; i = 0

.loop:
    cmp  ecx, esi        ; i < len?
    jge  .done

    mov  ebx, [rdi + rcx*4]  ; ebx = arr[i]
    add  eax, ebx             ; sum += arr[i]
    inc  ecx                  ; i++
    jmp  .loop

.done:
    pop  rcx             ; restore
    pop  rbx             ; restore
    pop  rbp
    ret
```

## 6. Common mistakes

### Mistake 1: Forgetting to save/restore callee-saved registers

```assembly
my_func:
    push rbp
    mov  rbp, rsp
    mov  rbx, 100        ; rbx is callee-saved!
    ; ... but we didn't push rbx first!
    pop  rbp
    ret
```

When the caller checks `rbx` after calling `my_func`, it'll find 100 instead of the original value.

### Mistake 2: Stack imbalance (more pushes than pops)

```assembly
my_func:
    push rbp
    mov  rbp, rsp
    push rbx
    push r12
    ; ... do work ...
    pop  r12
    ; MISSING: pop rbx
    pop  rbp
    ret
```

This corrupts the stack. The `ret` will pop the wrong address and crash.

### Mistake 3: Stack imbalance (mismatched call/ret)

```assembly
my_func:
    push rbp
    mov  rbp, rsp
    ; ... work ...
    pop  rbp
    ret

; Somewhere else:
    call my_func
    ; but if we also do:
    jmp  my_func        ; this doesn't push a return address!
                        ; the ret will pop garbage and crash
```

### Mistake 4: Using RSP after adjusting it, then not resetting

```assembly
my_func:
    push rbp
    mov  rbp, rsp
    sub  rsp, 16        ; allocate 16 bytes for locals
    ; ... use [rbp-8], [rbp-16] ...
    ; BUG: forgot to restore RSP before pop rbp
    pop  rbp            ; pops the wrong value!
    ret

; CORRECT:
my_func:
    push rbp
    mov  rbp, rsp
    sub  rsp, 16
    ; ... use locals ...
    mov  rsp, rbp       ; restore RSP
    pop  rbp
    ret
```

### Mistake 5: Using red zone when calling other functions

```assembly
leaf_func:
    mov  [rsp - 8], rax     ; safe — we don't call anything
    ; ... work ...
    ret

non_leaf:
    mov  [rsp - 8], rax     ; UNSAFE! If we call something, the call
    call leaf_func          ; instruction pushes return address here!
    ret
```

### Mistake 6: Returning a value in the wrong register

The return value convention (we'll formalize in the next lesson) is **rax**. Don't return in rbx, rcx, or any other register.

### Mistake 7: Forgetting that `call` changes RSP

```assembly
my_func:
    push rbp
    mov  rbp, rsp
    sub  rsp, 32
    ; ... push some values ...
    ; ... do work ...
    ; Now trying to pop rbp, but RSP isn't where we left it!
    pop  rbp            ; pops wrong value!
    ret
```

Always ensure RSP is exactly where it was after `mov rbp, rsp` before the epilogue.

## 7. Exercises

1. **Simple subroutine.** Write a subroutine `double_value` that takes an integer in `rdi` and returns `rdi * 2` in `rax`. Call it, exit with the result.

2. **Two subroutines.** Write `square` (returns rdi*rdi) and `cube` (returns square * rdi). `cube` should call `square`. Test with input 4, exit with 64.

3. **Local variables.** Write a subroutine that takes 3 numbers in rdi, rsi, rdx, computes `(a+b) * (b+c)`, stores intermediates on the stack, and returns the result.

4. **Array max subroutine.** Write a subroutine `array_max` that takes (array pointer in rdi, length in rsi) and returns the maximum element in rax.

5. **Fibonacci recursive.** Write a recursive `fibonacci(n)` subroutine. fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2). Test with n=10, result should be 55.

6. **String length.** Write a subroutine `strlen` that takes a pointer to a null-terminated string in rdi and returns its length (not counting the null terminator) in rax. Use the stack to save any registers you modify.

7. **Push/pop order.** Write a subroutine that swaps the values of rbx and r12 using only push/pop on the stack (no mov or xchg between the registers directly). Verify by calling it and checking both registers afterward.

8. **Preserve all.** Write a subroutine that adds 10 to rdi, 20 to rsi, 30 to rdx, and returns the sum in rax — but preserves rdi, rsi, rdx (they should be unchanged after the call).

9. **Nested calls.** Write `sum_of_squares(n)` that calls `square(n)` and adds it recursively: `sum_of_squares(3)` = 3² + 2² + 1² = 14.

10. **Red zone test.** Write a leaf subroutine that uses only the red zone (no `sub rsp`) to store a temporary value, compute something, and return. Verify it works.

## 8. Self-check questions

- [ ] What does RSP point to? Does the stack grow up or down?
- [ ] What do `push rax` and `pop rax` do? Write the equivalent using `sub`/`add`/`mov`.
- [ ] What does `call` push onto the stack? What does `ret` pop from the stack?
- [ ] Why do we do `push rbp; mov rbp, rsp` at the start of a subroutine?
- [ ] How do you allocate space for 4 local 8-byte variables on the stack?
- [ ] What is the red zone? When can you safely use it?
- [ ] Why must callee-saved registers be preserved by the subroutine?
- [ ] What happens if `ret` is executed when RSP points to the wrong address?
- [ ] Ordering: if you push rbx, push r12, what order must you pop them in?
- [ ] What register does the return value go into?

## 9. What's next

You now understand the stack, subroutines, and how to build modular programs. You've seen a simple pattern for passing arguments (in registers) and returning values (in rax).

In the next lesson — **calling conventions (System V AMD64 ABI)**: the exact rules for how functions should pass arguments, which registers must be preserved, stack alignment requirements, and how to write functions that can be called from C or other languages.
