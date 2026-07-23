# [08] Calling convention (System V AMD64 ABI)

> **Track:** Assembly · **Level:** 08 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

In the last lesson we wrote subroutines and passed arguments in registers. But which registers? We used `rdi` and `rsi` for arguments, but we never agreed on a **standard**.

If two people write assembly functions and one passes arguments in `rdi, rsi` while the other expects them in `rbx, rcx`, the functions can't work together:

```assembly
; Alice writes:
my_func_a:
    ; expects arg in rdi
    ; ... work with rdi ...

; Bob writes:
my_func_b:
    ; expects arg in rbx
    ; ... work with rbx ...

; These can't call each other without translation!
```

Now imagine this at the scale of an entire operating system (Linux). Every C function, every library function, every system call uses a **calling convention** — a contract that says:

- **Where are arguments passed?** (which registers, or stack)
- **Where is the return value?**
- **Which registers can the callee freely modify?**
- **Which registers must the callee preserve?**
- **What are the stack alignment rules?**

On Linux x86-64, the standard is the **System V AMD64 ABI** (Application Binary Interface). This is what the C compiler uses, what libc uses, and what we must follow to interoperate.

## 2. Core concept (absolute zero)

### 2.1 What is an ABI?

An **Application Binary Interface** is a set of rules that ensures object files (`.o`) compiled by different compilers (or written in different languages) can link together and work.

It covers:
- **Calling convention** — how functions call each other
- **Data layout** — sizes and alignments of types (int is 4 bytes, long is 8 bytes, etc.)
- **Name mangling** — how symbol names appear in object files (C: no mangling, C++: complex mangling)
- **Exception handling** — how stack unwinding works

For this lesson, we focus on the **calling convention** part.

### 2.2 System V AMD64 ABI — the rules

#### Argument passing (integer/pointer)

| Argument # | Register |
|:----------:|:--------:|
| 1st | `rdi` |
| 2nd | `rsi` |
| 3rd | `rdx` |
| 4th | `rcx` |
| 5th | `r8` |
| 6th | `r9` |
| 7th+ | on the stack (right to left) |

```assembly
; func(a, b, c, d, e, f, g, h)
; rdi  rsi rdx rcx r8  r9  [rsp] [rsp+8]
```

#### Return value

| Type | Register |
|:----:|:--------:|
| Integer/pointer (≤64 bits) | `rax` |
| 128-bit integer | `rax` (low), `rdx` (high) |

#### Caller-saved registers (volatile)

The callee may freely modify these. If the caller needs them after the call, it must save them.

| Register | Note |
|:--------:|:----:|
| `rax` | return value, also scratch |
| `rcx` | 4th argument, also scratch |
| `rdx` | 3rd argument, also scratch |
| `rsi` | 2nd argument, also scratch |
| `rdi` | 1st argument, also scratch |
| `r8` | 5th argument, also scratch |
| `r9` | 6th argument, also scratch |
| `r10` | scratch |
| `r11` | scratch |

#### Callee-saved registers (non-volatile)

If the callee wants to use these registers, it must save them (usually with `push` at entry and `pop` at exit) and restore them before `ret`.

| Register | Note |
|:--------:|:----:|
| `rbx` | preserved |
| `rbp` | preserved (also used as frame pointer) |
| `r12` | preserved |
| `r13` | preserved |
| `r14` | preserved |
| `r15` | preserved |
| `rsp` | preserved (must be restored to original value) |

#### Stack alignment

**This is one of the most important and most confusing rules.**

At the point of a `call` instruction, **RSP must be 16-byte aligned** (i.e., RSP % 16 == 0).

Why? The `call` pushes an 8-byte return address, making RSP = RSP - 8, which is now **misaligned** (RSP % 16 == 8). Inside the function, if we do `push rbp` (another 8 bytes), RSP becomes aligned again.

```
Alignment before call:    RSP % 16 == 0
After call (push ret addr): RSP % 16 == 8
After push rbp:           RSP % 16 == 0   ← aligned again
```

The callee can expect that after its prologue (`push rbp; mov rbp, rsp`), RSP is 16-byte aligned.

### 2.3 The shadow space (Windows vs Linux)

On **Windows x64** (not Linux), the caller must reserve 32 bytes of "shadow space" on the stack before every call, even for functions with ≤4 arguments. This is for registers the callee may want to save.

On **Linux** (System V): **no shadow space**. Arguments ≤ 6 go in registers only. This is simpler and more efficient.

### 2.4 `cqo` — sign extension for division

The `cqo` instruction (Convert Quadword to Octword) sign-extends RAX into RDX:RAX.

```assembly
mov  rax, -5     ; rax = -5 (0xFFFFFFFFFFFFFFFB)
cqo              ; rdx = 0xFFFFFFFFFFFFFFFF (all 1s, because sign bit is 1)
                 ; rax unchanged: 0xFFFFFFFFFFFFFFFB
                 ; Now RDX:RAX = -5 as a 128-bit signed value

; This is needed before signed division (idiv):
mov  rax, -100
cqo              ; sign-extend into RDX
mov  rbx, 3
idiv rbx         ; rax = -33, rdx = -1 (remainder)
```

For unsigned division, just zero RDX:
```assembly
mov  rax, 100
xor  edx, edx   ; zero RDX (unsigned extension)
mov  rbx, 3
div  rbx        ; rax = 33, rdx = 1
```

### 2.5 Floating-point arguments

The System V ABI also defines passing for floating-point values:
- **xmm0–xmm7** — first 8 float/double arguments
- **xmm0** — return value for float/double
- Mixing integer and float args: integer args go in the integer registers, float args go in the SSE registers, preserving order

```c
// C function:
double func(int a, double b, int c, double d);
// a -> rdi, b -> xmm0, c -> rsi, d -> xmm1
// return -> xmm0
```

### 2.6 The function prologue and epilogue

Standard pattern following the ABI:

```assembly
my_func:
    ; ─── Prologue ───
    push rbp           ; save old frame pointer
    mov  rbp, rsp      ; set new frame pointer

    ; (optional) allocate locals
    sub  rsp, 32       ; reserve 32 bytes

    ; ─── Body ───
    ; rdi, rsi, rdx, rcx, r8, r9 have arguments
    ; rax, rcx, rdx, rsi, rdi, r8-r11 may be freely modified
    ; rbx, rbp, r12-r15 must be preserved

    ; ─── Epilogue ───
    mov  rsp, rbp      ; restore stack pointer
    pop  rbp           ; restore old frame pointer
    ret                ; return (rax has result)
```

## 3. Step-by-step breakdown

### 3.1 Writing an ABI-compliant function

```assembly
; abi_func.asm — ABI-compliant function
section .text
    global add_three

; int add_three(int a, int b, int c)
; Arguments: rdi = a, rsi = b, rdx = c
; Returns:   rax = a + b + c
add_three:
    push rbp
    mov  rbp, rsp

    mov  rax, rdi
    add  rax, rsi
    add  rax, rdx

    pop  rbp
    ret
```

### 3.2 Calling a function from another function

```assembly
; caller.asm — one ABI function calling another
section .text
    global compute

; int compute(int x)
; Returns (x * x) + (x * 2) + 1
compute:
    push rbp
    mov  rbp, rsp

    ; Save x (rdi) — we need it after the first call
    ; But rdi is caller-saved, so WE must save it
    push rdi

    ; Call square(x)
    call square           ; rax = square(x)

    ; Restore x
    pop  rdi

    ; Now compute x*2
    mov  rcx, rdi
    shl  rcx, 1           ; rcx = x*2

    ; Add square + x*2
    add  rax, rcx

    ; Add 1
    add  rax, 1

    pop  rbp
    ret

; int square(int n)
square:
    push rbp
    mov  rbp, rsp
    mov  rax, rdi
    imul rax, rdi
    pop  rbp
    ret
```

### 3.3 Using callee-saved registers

```assembly
; callee_saved.asm — demonstrates callee-saved register use
section .text
    global process_array

; int process_array(int* arr, int len)
; Sums all elements, returns sum + len
process_array:
    push rbp
    mov  rbp, rsp
    push rbx             ; save rbx (callee-saved)
    push r12             ; save r12 (callee-saved)

    ; rdi = arr, rsi = len
    mov  rbx, rdi        ; rbx = arr (preserved, so we MUST save it)
    mov  r12, rsi        ; r12 = len (preserved, so we MUST save it)

    xor  eax, eax        ; sum = 0
    xor  ecx, ecx        ; i = 0

.loop:
    cmp  ecx, r12d       ; i < len?
    jge  .done

    mov  edx, [rbx + rcx*4]  ; edx = arr[i]
    add  eax, edx             ; sum += arr[i]
    inc  ecx                  ; i++
    jmp  .loop

.done:
    add  eax, r12d       ; sum += len

    pop  r12             ; restore r12
    pop  rbx             ; restore rbx
    pop  rbp
    ret
```

### 3.4 Stack alignment in action

```assembly
; alignment.asm — demonstrating stack alignment
section .text
    global _start
    extern some_c_func   ; imagine a C function

_start:
    ; At program entry, RSP is 16-byte aligned (OS guarantees this)

    ; If we call a function directly:
    call my_func         ; call pushes 8 bytes → RSP % 16 == 8 at entry

    ; But _start is not a function! No one called us (the OS started us).
    ; So RSP is aligned, and after call it's misaligned.

    mov  eax, 60
    xor  edi, edi
    syscall

my_func:
    ; Entry: RSP % 16 == 8 (because call pushed 8 bytes)
    push rbp             ; RSP -= 8, now RSP % 16 == 0 (aligned!)
    mov  rbp, rsp

    ; Now we can safely call other functions:
    call other_func      ; RSP % 16 == 0 before call → all good

    pop  rbp
    ret

other_func:
    push rbp
    mov  rbp, rsp
    ; RSP is correctly aligned here
    pop  rbp
    ret
```

### 3.5 Function with extra arguments on the stack

When a function has more than 6 arguments, the extra ones are passed on the stack:

```assembly
; lots_of_args.asm — function with 8 arguments
section .text
    global sum_8

; int sum_8(int a, int b, int c, int d, int e, int f, int g, int h)
; Registers: rdi, rsi, rdx, rcx, r8, r9
; Stack:     [rsp] = g, [rsp+8] = h (pushed by caller right-to-left)
sum_8:
    push rbp
    mov  rbp, rsp

    ; sum = a + b + c + d + e + f + g + h
    mov  rax, rdi
    add  rax, rsi
    add  rax, rdx
    add  rax, rcx
    add  rax, r8
    add  rax, r9

    ; g is at [rbp + 16]
    ; Stack layout (from rbp):
    ; [rbp + 24] = h
    ; [rbp + 16] = g
    ; [rbp + 8]  = return address (pushed by call)
    ; [rbp + 0]  = saved rbp

    add  rax, [rbp + 16]    ; add g
    add  rax, [rbp + 24]    ; add h

    pop  rbp
    ret

; Calling sum_8 from _start:
_start:
    mov  rdi, 1
    mov  rsi, 2
    mov  rdx, 3
    mov  rcx, 4
    mov  r8,  5
    mov  r9,  6
    push 8                  ; push h (pushed LAST, highest address)
    push 7                  ; push g (pushed FIRST, lower address)
    call sum_8
    ; rax = 1+2+3+4+5+6+7+8 = 36
    add  rsp, 16            ; clean up stack arguments

    mov  edi, eax
    mov  eax, 60
    syscall
```

### 3.6 Complete program: assembly calling C-style functions

```assembly
; complete.asm — all ABI rules demonstrated
section .data
    arr     dd 3, 7, 2, 9, 5
    arr_len equ 5

section .text
    global _start

_start:
    lea  rdi, [arr]
    mov  rsi, arr_len
    call array_stats

    mov  edi, eax        ; exit with sum
    mov  eax, 60
    syscall

; struct Stats { int sum; int max; int min; };
; void array_stats(int* arr, int len, struct Stats* out)
; Arguments: rdi = arr, rsi = len
; Returns:   rax = sum, rdx = max
; We'll demonstrate returning two values (in rax and rdx)
array_stats:
    push rbp
    mov  rbp, rsp
    push rbx             ; save callee-saved
    push r12             ; save callee-saved
    push r13             ; save callee-saved

    ; Use callee-saved registers for our loop vars
    mov  rbx, rdi        ; rbx = arr
    mov  r12, rsi        ; r12 = len
    xor  r13d, r13d      ; r13 = i = 0

    ; Initialize
    xor  eax, eax        ; sum = 0
    mov  ecx, [rbx]      ; max = arr[0]
    mov  edx, [rbx]      ; min = arr[0]

.loop:
    cmp  r13d, r12d      ; i < len?
    jge  .done

    mov  esi, [rbx + r13*4]  ; esi = arr[i]

    add  eax, esi        ; sum += arr[i]

    cmp  esi, ecx
    jle  .check_min      ; if arr[i] <= max, skip max update
    mov  ecx, esi        ; new max
    jmp  .next

.check_min:
    cmp  esi, edx
    jge  .next           ; if arr[i] >= min, skip
    mov  edx, esi        ; new min

.next:
    inc  r13d
    jmp  .loop

.done:
    ; rax = sum, rcx = max, edx = min
    ; Return sum in rax, max in rdx (2 return values demo)
    mov  rdx, rcx        ; rdx = max

    pop  r13
    pop  r12
    pop  rbx
    pop  rbp
    ret
```

### 3.7 Floating-point example

```assembly
; float_func.asm — ABI with floating point
section .text
    global quadratic

; double quadratic(double x, double a, double b, double c)
; Returns a*x*x + b*x + c
; Arguments: xmm0 = x, xmm1 = a, xmm2 = b, xmm3 = c
; Return:    xmm0
quadratic:
    push rbp
    mov  rbp, rsp

    ; Compute a*x*x
    movsd xmm4, xmm1       ; xmm4 = a
    mulsd xmm4, xmm0       ; xmm4 = a * x
    mulsd xmm4, xmm0       ; xmm4 = a * x * x

    ; Compute b*x
    movsd xmm5, xmm2       ; xmm5 = b
    mulsd xmm5, xmm0       ; xmm5 = b * x

    ; Add them all
    addsd xmm4, xmm5       ; xmm4 = a*x*x + b*x
    addsd xmm4, xmm3       ; xmm4 = a*x*x + b*x + c

    movsd xmm0, xmm4       ; return value

    pop  rbp
    ret
```

## 4. Common mistakes

### Mistake 1: Assuming arguments stay in registers after a call

```assembly
my_func:
    push rbp
    mov  rbp, rsp
    ; rdi has the first argument
    call other_func
    ; rdi may have been modified by other_func!
    ; rdi is caller-saved! Save it before call if you need it.
    pop  rbp
    ret
```

### Mistake 2: Not preserving callee-saved registers

```assembly
my_func:
    push rbp
    mov  rbp, rsp
    ; BUG: using rbx without saving it
    mov  rbx, 42
    ; ... work ...
    pop  rbp
    ret
```

If the caller had something in rbx, it's now lost.

### Mistake 3: Stack misalignment

```assembly
my_func:
    push rbp
    mov  rbp, rsp
    ; At this point RSP % 16 == 0 (if alignment was correct)

    ; But if we only push 1 register (8 bytes):
    push rbx             ; RSP -= 8, now RSP % 16 == 8
    call other_func      ; BAD! RSP % 16 == 8 before call (should be 0)
    pop  rbx

    pop  rbp
    ret
```

**Fix:** always ensure the total stack adjustment (pushes + sub rsp) is a multiple of 16 bytes after the prologue. Or push an even number of callee-saved registers.

### Mistake 4: Forgetting to clean up stack after extra arguments

```assembly
    push 8              ; extra arg
    push 7              ; extra arg
    call lots_of_args
    ; BUG: RSP was changed by the two pushes, but we didn't restore it!
    add  rsp, 16        ; CORRECT: clean up the stack
```

### Mistake 5: Using `div` without zeroing RDX (unsigned) or using `cqo` (signed)

```assembly
    mov  rax, 100
    ; BUG: forgot xor edx, edx
    mov  rbx, 3
    div  rbx             ; uses RDX:RAX as dividend! RDX has garbage!
    ; Result is garbage

    ; CORRECT:
    xor  edx, edx
    div  rbx
```

### Mistake 6: Passing a 32-bit value in a 64-bit register without clearing upper bits

When a C function expects an `int` (32-bit), the upper 32 bits of the register are undefined. To be safe, always zero-extend:

```assembly
    mov  edi, 42        ; implicitly zeros upper 32 bits of rdi
    ; This is correct — writing to edi zeros rdi[63:32]
    ; But:
    mov  rdi, 42        ; also correct for small values
    ; However:
    mov  rdi, rax       ; If rax has garbage in bits 63:32, rdi will too
```

In practice, writing to a 32-bit register (like `edi`) always zero-extends to 64 bits. Writing to a 16-bit or 8-bit register does NOT.

## 5. Exercises

1. **ABI function.** Write an ABI-compliant function `int multiply(int a, int b, int c)` that returns a*b*c. Call it from `_start` with values 2, 3, 4. Exit with result 24.

2. **Callee-saved registers.** Write a function that uses rbx, r12, r13, and r14 — but correctly preserves all of them. The function should add all four arguments and return the sum.

3. **Caller-saved registers.** Write a function `compute(x, y)` that calls `square(x)` and `square(y)` (from earlier) and returns `square(x) + square(y)`. Since `square` may modify rax, rcx, rdx, rsi, rdi, save x and y before the calls.

4. **Stack arguments.** Write a function `sum_10` that sums 10 integer arguments (args 7-10 on the stack). Call it and verify the result.

5. **Stack alignment.** Write a function that calls another function 3 levels deep. Ensure stack alignment is correct at every level.

6. **cqo for division.** Write a function `int divide(int a, int b)` that uses `cqo` and `idiv` for proper signed division. Test with -100 / 3, result should be -33.

7. **Two return values.** Write a function `int divmod(int a, int b)` that returns quotient in rax and remainder in rdx. Call it from `_start` and verify both.

8. **Floating-point ABI.** Write a function `double average(double a, double b, double c)` that returns the average. Pass 1.0, 2.0, 3.0. Since you can't easily print floats from assembly without libc, just verify with a debugger or by storing to memory.

9. **Function pointer.** Store the address of a function in a register (e.g., `mov rbx, my_func`) and call it via `call rbx`. This is how function pointers work.

10. **Mixed args.** Write a function `double mixed(int a, double b, int c, double d)` that returns `a*b + c*d`. Pass 2, 3.0, 4, 5.0 → result = 2*3 + 4*5 = 26.0.

## 6. Self-check questions

- [ ] What registers are used for the first 6 integer arguments?
- [ ] What register holds the return value?
- [ ] List the caller-saved registers. List the callee-saved registers.
- [ ] Why must RSP be 16-byte aligned before a `call`?
- [ ] What is the shadow space? Does Linux use it?
- [ ] What does `cqo` do and when is it needed?
- [ ] What if a function has more than 6 arguments? Where do the extras go?
- [ ] Can a function modify rbx without saving it first? Why or why not?
- [ ] What registers are used for floating-point arguments?
- [ ] After `call`, does the callee know whether RSP is aligned or misaligned? (Hint: think about the return address)

## 7. What's next

You now know the System V AMD64 ABI calling convention. You can write assembly functions that are fully interoperable with C code and with other assembly code. This is the foundation for:

- Calling libc functions (printf, malloc, etc.) from assembly
- Writing assembly functions that C can call
- Understanding how compilers generate function calls
- The next level: strings and REP instructions for efficient memory operations
