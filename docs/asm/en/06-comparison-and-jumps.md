# [06] Comparison and conditional jumps

> **Track:** Assembly · **Level:** 06 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

So far every program we wrote runs in a straight line — instruction after instruction, top to bottom:

```assembly
mov rax, 10
add rax, 5
mov rbx, rax
; ... always executes every line
```

But real programs need **decisions**:
- If a number is zero, do one thing; otherwise do another
- Loop while a condition is true
- Loop a fixed number of times (for loop)
- Check if one value is greater than another

In C:
```c
if (x > 0) {
    // do something
} else {
    // do something else
}

while (i < 10) {
    // repeat
}

for (int i = 0; i < n; i++) {
    // repeat
}
```

Assembly has no `if`, `while`, or `for` keywords. We need to build these constructs from scratch using:
1. **`cmp`** — compare two values (sets flags)
2. **Conditional jumps** — jump (or don't) based on flags
3. **`jmp`** — unconditional jump

## 2. Core concept (absolute zero)

### 2.1 The flags register (RFLAGS)

The CPU has a special register called **RFLAGS** (64 bits). We never access it directly by name like `rax`. Instead, instructions **set** individual bits inside it, and other instructions **read** those bits.

The most important flags for comparisons:

| Flag | Full name | Meaning when set (= 1) |
|------|-----------|----------------------|
| ZF | Zero Flag | Last result was zero |
| CF | Carry Flag | Last operation caused a carry/borrow (unsigned overflow) |
| SF | Sign Flag | Last result was negative (highest bit = 1) |
| OF | Overflow Flag | Last result caused signed overflow |
| PF | Parity Flag | Last result had even number of 1 bits (rarely used) |
| AF | Auxiliary Flag | BCD carry (rarely used) |

**Analogy:** Think of flags as tiny sticky notes the CPU sticks on its desk after each calculation. A later instruction can check: "was the zero flag set?" and act accordingly.

### 2.2 `cmp` — compare

`cmp` works like `sub` (subtraction) but **discards the result** — it only sets the flags:

```assembly
sub rax, rbx    ; rax = rax - rbx, sets flags, AND changes rax
cmp rax, rbx    ; computes rax - rbx, sets flags, but does NOT change rax
```

```
Before: rax = 10, rbx = 5

cmp rax, rbx    ; internally computes 10 - 5 = 5
                ; ZF = 0 (result is not zero)
                ; CF = 0 (no borrow)
                ; SF = 0 (result is positive)
                ; rax is still 10, rbx is still 5

Compare this to:

sub rax, rbx    ; rax = 10 - 5 = 5
                ; same flags, but rax changed!
```

**What flags does cmp set?**

| Comparison | ZF | CF | SF | OF |
|------------|:--:|:--:|:--:|:--:|
| `cmp a, b` where a == b | 1 | 0 | 0 | 0 |
| `cmp a, b` where a < b (signed) | 0 | depends | 1 | depends |
| `cmp a, b` where a > b (signed) | 0 | depends | 0 | depends |
| `cmp a, b` where a < b (unsigned) | 0 | 1 | — | — |
| `cmp a, b` where a > b (unsigned) | 0 | 0 | — | — |

### 2.3 How flags work (the full picture)

When `cmp a, b` computes `a - b`:

- **ZF = 1** if `a == b` (because `a - b = 0`)
- **CF = 1** if `a < b` when treating both as **unsigned** (because `a - b` would need a borrow)
- **SF = 1** if the result is negative (i.e., `a < b` when treating both as **signed**)
- **OF = 1** if signed overflow occurred (when `a` and `b` have opposite signs and the result has the wrong sign)

### 2.4 Conditional jumps

A conditional jump checks one or more flags and jumps (or doesn't) to a label.

Every conditional jump has **multiple mnemonics** for the same instruction — they're aliases.

#### Equality / zero checks

| Instruction | Checks | Jumps when |
|-------------|--------|------------|
| `je label` | ZF == 1 | a == b |
| `jz label` | ZF == 1 | result was zero (same as je) |
| `jne label` | ZF == 0 | a != b |
| `jnz label` | ZF == 0 | result was nonzero (same as jne) |

`je` and `jz` are the **same opcode** (0x74). They exist so your code reads naturally:
- `je` → "jump if equal" (after `cmp`)
- `jz` → "jump if zero" (after `test` or `sub`)

#### Signed comparisons

Treat values as signed (two's complement). Uses SF and OF.

| Instruction | Condition | Jumps when |
|-------------|-----------|------------|
| `jg` | SF == OF AND ZF == 0 | a > b (signed) |
| `jge` | SF == OF | a >= b (signed) |
| `jl` | SF != OF | a < b (signed) |
| `jle` | SF != OF OR ZF == 1 | a <= b (signed) |
| `jnle` | same as `jg` | a > b (signed, not less or equal) |
| `jnge` | same as `jl` | a < b (signed, not greater or equal) |

#### Unsigned comparisons

Treat values as unsigned (0 to 2^N-1). Uses CF.

| Instruction | Condition | Jumps when |
|-------------|-----------|------------|
| `ja` | CF == 0 AND ZF == 0 | a > b (unsigned) |
| `jae` | CF == 0 | a >= b (unsigned) |
| `jb` | CF == 1 | a < b (unsigned) |
| `jbe` | CF == 1 OR ZF == 1 | a <= b (unsigned) |

The mnemonics form a pattern:
- `j` + `g`/`l` = **signed** (greater/less) — uses SF, OF
- `j` + `a`/`b` = **unsigned** (above/below) — uses CF

#### Flag-specific checks

| Instruction | Checks | Jumps when |
|-------------|--------|------------|
| `js label` | SF == 1 | result was negative |
| `jns label` | SF == 0 | result was non-negative |
| `jc label` | CF == 1 | carry occurred |
| `jnc label` | CF == 0 | no carry |
| `jo label` | OF == 1 | signed overflow occurred |
| `jno label` | OF == 0 | no signed overflow |
| `jp label` | PF == 1 | even parity |
| `jnp label` | PF == 0 | odd parity |

### 2.5 `jmp` — unconditional jump

Jumps **always**, no flags checked:

```assembly
jmp label    ; go to label, no questions asked
```

This is the assembly equivalent of `goto`.

### 2.6 `test` — compare without subtraction

Sometimes you just want to check if a value is zero, negative, or has certain bits set, without comparing two values.

`test` does a **bitwise AND** of two operands, sets flags, discards result:

```assembly
test rax, rax    ; computes rax & rax = rax (AND with itself)
                 ; sets ZF if rax == 0
                 ; sets SF if rax < 0 (bit 63 = 1)
                 ; does NOT change rax!
```

This is the idiomatic way to check if a register is zero:
```assembly
test rax, rax
jz   .is_zero       ; jump if rax == 0
js   .is_negative   ; jump if rax < 0
```

Why `test rax, rax` instead of `cmp rax, 0`? Both work, but `test` is slightly faster on some CPUs and is the conventional idiom.

### 2.7 Jump range and labels

A jump instruction has a **target label**. The assembler computes the distance from the jump to the label and encodes it in the instruction:

```assembly
cmp rax, 10
je .done       ; if rax == 10, jump to .done
; ... more code ...
.done:
    ; execution continues here after jump
```

Labels that start with `.` are **local labels** — they're scoped to the nearest non-local label. This lets you reuse `.loop`, `.done`, `.skip` in different functions.

## 3. Step-by-step breakdown

### 3.1 The if pattern

```asm
; if (rax == 0) { rbx = 1; }
    cmp  rax, 0
    jne  .after_if     ; skip if NOT equal (rax != 0)
    mov  rbx, 1
.after_if:
```

```asm
; if (rax > rbx) { rcx = 100; }
    cmp  rax, rbx
    jle  .after_if     ; skip if rax <= rbx
    mov  rcx, 100
.after_if:
```

**Key insight:** You write the **opposite** condition for the jump. To execute code when `rax == 0`, you jump when `rax != 0` (`jne`). The body follows the jump; if the condition is true, the jump is NOT taken and the body runs.

### 3.2 The if/else pattern

```asm
; if (rax == 0) { rbx = 1; } else { rbx = 2; }
    cmp  rax, 0
    jne  .else          ; jump to else if NOT equal
    mov  rbx, 1         ; if body
    jmp  .after_if      ; skip else after if body
.else:
    mov  rbx, 2         ; else body
.after_if:
```

The `jmp` after the if-body is **critical** — without it, execution would "fall through" into the else body.

```
Execution flow:
                ┌─────────────────────┐
                │ cmp rax, 0          │
                │ jne .else    ───────┼──→ false (rax != 0)
                │ mov rbx, 1         │ │
                │ jmp .after_if ───┐  │ │
                └──────────────────│──│─┘
                  ┌──────────────┐ │  │
                  │ .else:       │ ←──┘
                  │ mov rbx, 2   │ │
                  │ jmp .after   │ │
                  └──────────────┘ │
                  ┌────────────────┘
                  │
                  ▼
                .after_if:
```

### 3.3 The while loop pattern

```asm
; while (rax < 10) {
;     rax++;
; }
    mov  rax, 0          ; initialize counter
.loop:
    cmp  rax, 10         ; check condition
    jge  .end_loop       ; exit if rax >= 10
    inc  rax             ; body
    jmp  .loop           ; repeat
.end_loop:
```

Better structure (more common):
```asm
    mov  rax, 0
    jmp  .check          ; jump to check first
.loop:
    inc  rax             ; body
.check:
    cmp  rax, 10
    jl   .loop           ; if rax < 10, repeat
```

### 3.4 The for loop pattern

```asm
; for (rcx = 0; rcx < 5; rcx++) {
;     [arr + rcx*4] = rcx * 10;
; }
    mov  rcx, 0          ; i = 0
.loop:
    cmp  rcx, 5          ; i < 5?
    jge  .end_loop       ; if i >= 5, exit
    mov  [arr + rcx*4], ecx  ; body
    inc  rcx             ; i++
    jmp  .loop
.end_loop:
```

Counting **down** is often simpler:
```asm
; for (rcx = 4; rcx >= 0; rcx--)
    mov  rcx, 5          ; count = 5
.loop:
    dec  rcx             ; count-- (also sets ZF!)
    js   .end_loop       ; if negative, exit
    ; ... body ...
    jmp  .loop
.end_loop:
```

Or with a counter approach:
```asm
    mov  rcx, 5          ; count = 5
.loop:
    test rcx, rcx        ; check if zero
    jz   .end_loop       ; if zero, done
    dec  rcx             ; count--
    ; ... body ...
    jmp  .loop
.end_loop:
```

### 3.5 Checking multiple conditions

You can chain comparisons:

```asm
; if (rax > 0 && rax < 10) { rbx = 1; }
    cmp  rax, 0
    jle  .after_if       ; if rax <= 0, skip
    cmp  rax, 10
    jge  .after_if       ; if rax >= 10, skip
    mov  rbx, 1
.after_if:
```

```asm
; if (rax == 0 || rax == 5) { rbx = 1; }
    cmp  rax, 0
    je   .do_body        ; if rax == 0, do it
    cmp  rax, 5
    jne  .after_if       ; if rax != 5, skip
.do_body:
    mov  rbx, 1
.after_if:
```

## 4. Complete program: finding maximum in array

```assembly
; max.asm — find the maximum value in an array
section .data
    arr     dd 17, 42, 8, 99, 23, 56, 3, 71
    arr_len equ 8

section .text
    global _start

_start:
    ; Find maximum value in arr (signed)
    lea  rbx, [arr]          ; rbx = address of arr
    mov  ecx, arr_len        ; ecx = number of elements
    mov  eax, [rbx]          ; eax = first element (current max)
    dec  ecx                 ; already read first element
    add  rbx, 4              ; move to next element

.loop:
    test ecx, ecx            ; check if counter is zero
    jz   .done               ; if zero, done

    mov  edx, [rbx]          ; edx = current element
    cmp  edx, eax            ; compare current with max
    jle  .skip               ; if current <= max, skip
    mov  eax, edx            ; new max

.skip:
    add  rbx, 4              ; advance to next element
    dec  ecx                 ; counter--
    jmp  .loop

.done:
    ; eax = 99 (the maximum)
    mov  edi, eax            ; exit code = max value
    mov  eax, 60             ; sys_exit
    xor  edi, edi
    syscall
```

## 5. Complete program: signed vs unsigned comparison

```assembly
; signed_unsigned.asm — demonstrates the difference between jg and ja
section .data
    ; Treat 0xFF as 255 (unsigned) or -1 (signed)
    val_a dq 0xFF            ; = 255 unsigned, = -1 signed
    val_b dq 0x01            ; = 1 both ways

section .text
    global _start

_start:
    ; ─── Signed comparison (jg/jl) ───
    mov  rax, [val_a]        ; rax = 0xFF = -1 (signed)
    mov  rbx, [val_b]        ; rbx = 1
    cmp  rax, rbx
    jg   .signed_greater     ; Is -1 > 1? NO (jg uses signed comparison)
    ; Falls through: -1 < 1, so jg not taken
    mov  r8, 0               ; r8 = 0 (signed says: -1 is NOT greater than 1)
    jmp  .check_unsigned

.signed_greater:
    mov  r8, 1

.check_unsigned:
    ; ─── Unsigned comparison (ja/jb) ───
    mov  rax, [val_a]        ; rax = 0xFF = 255 (unsigned)
    mov  rbx, [val_b]        ; rbx = 1
    cmp  rax, rbx
    ja   .unsigned_above     ; Is 255 > 1? YES (ja uses unsigned comparison)
    mov  r9, 0
    jmp  .done

.unsigned_above:
    mov  r9, 1               ; r9 = 1 (unsigned says: 255 is above 1)

.done:
    ; r8 = 0, r9 = 1
    ; Same bytes, different interpretations!
    mov  edi, 0
    mov  eax, 60
    syscall
```

## 6. Complete program: for loop summing array

```assembly
; sum.asm — sum all elements of an array (for loop pattern)
section .data
    arr     dd 10, 20, 30, 40, 50
    arr_len equ 5

section .text
    global _start

_start:
    ; Sum all elements: sum = arr[0] + arr[1] + ... + arr[4]
    xor  eax, eax            ; sum = 0
    mov  ecx, 0              ; i = 0

.loop:
    cmp  ecx, arr_len        ; i < arr_len?
    jge  .done               ; if i >= arr_len, exit

    add  eax, [arr + ecx*4]  ; sum += arr[i]
    inc  ecx                 ; i++
    jmp  .loop

.done:
    ; eax = 10+20+30+40+50 = 150
    mov  edi, eax            ; exit code = 150
    mov  eax, 60
    syscall
```

## 7. Common mistakes

### Mistake 1: Wrong comparison direction in `cmp`

```assembly
cmp rax, rbx    ; computes rax - rbx
je  .equal      ; jumps if rax == rbx (correct)
```

The result of `cmp a, b` is `a - b`. `je` checks ZF which is set when `a - b = 0`, i.e., `a == b`. This is intuitive.

But for `jg`/`jl`: `cmp a, b; jg` means "jump if `a > b`", not "jump if `b > a`".

```assembly
cmp rax, 10
jg  .target    ; jumps if rax > 10, NOT if 10 > rax
```

### Mistake 2: Using `jg` when you should use `ja` (and vice versa)

```assembly
mov rax, -1    ; 0xFFFFFFFFFFFFFFFF
mov rbx, 1
cmp rax, rbx
jg  .target    ; signed: -1 > 1? NO (not taken)
ja  .target    ; unsigned: 0xFFFF... > 1? YES (taken)
```

Same bytes, completely different result.

### Mistake 3: Forgetting `jmp` after if-body in if/else

```assembly
    cmp  rax, 0
    jne  .else
    mov  rbx, 1
    ; MISSING: jmp .after_if   ← fall-through bug!
.else:
    mov  rbx, 2
.after_if:
```

Without `jmp .after_if`, execution falls through to the else body no matter what.

### Mistake 4: Using `cmp` when `test` is more idiomatic

```assembly
; Both work, but test is idiomatic for zero-check:
cmp  rax, 0     ; OK
jz   .zero

test rax, rax   ; preferred idiom
jz   .zero
```

### Mistake 5: Off-by-one in loops

```assembly
; WRONG — exits one iteration too early
    mov  ecx, 0
.loop:
    cmp  ecx, 5
    jge  .done     ; when ecx = 5, jge is taken → last iteration is ecx = 4
    ; ... body ...
    inc  ecx
    jmp  .loop

; CORRECT
    mov  ecx, 0
.loop:
    cmp  ecx, 5
    jnl  .done     ; wait, jnl is wrong too
    ; ...
```

Wait, let me be precise:
- `cmp ecx, 5; jge .done` — jumps when ecx >= 5. So loop body runs for ecx = 0,1,2,3,4. That's 5 iterations. Correct!

The actual off-by-one:
```assembly
; WRONG — 6 iterations instead of 5
    mov  ecx, 0
.loop:
    ; ... body ...
    inc  ecx
    cmp  ecx, 5
    jle  .loop     ; when ecx = 5, jle says 5 <= 5 is TRUE → does another iteration
; ecx becomes 6 before exit
```

### Mistake 6: Confusing `jl`/`jle` with `jb`/`jbe`

| Mnemonic | Meaning | For | Condition |
|----------|---------|-----|-----------|
| `jl` | Jump if Less | signed | SF != OF |
| `jb` | Jump if Below | unsigned | CF == 1 |

If you're comparing signed numbers (like -3 vs 5), use `jl`/`jg`. If you're comparing addresses or unsigned numbers, use `jb`/`ja`.

### Mistake 7: Not preserving the value being compared

```assembly
cmp rax, rbx
; ... some code that changes rax or rbx ...
je  .equal     ; BUG! rax or rbx may have changed
```

Always do the check immediately after the comparison, or save the flags (you can't — there's no "pushf" that's commonly used inline).

## 8. Exercises

1. **Simple if.** Write a program: if `rax == 5`, set `rbx = 1`. Otherwise set `rbx = 0`. Start with `rax = 5`. Exit with code = rbx (should be 1).

2. **If/else.** Write: if `rax > 10`, set `rbx = 100`; else set `rbx = 200`. Start with `rax = 7`. Exit with code 200.

3. **Find negative.** Given array `arr dd -5, 3, -1, 8, -9`, count how many elements are negative. Exit with the count.

4. **While loop (sum until zero).** Given `arr dd 7, 2, 9, 0, 5`, sum elements until you hit a zero (stop at zero, don't include it). Exit with sum = 18.

5. **Signed vs unsigned.** Let `rax = 0xFFFFFFFFFFFFFFF8` (-8 signed, huge unsigned), `rbx = 3`. Use `jg` and `ja` to compare — note the different results. Exit with 0 if jg was wrong, 1 if ja was right.

6. **For loop: factorial.** Compute factorial of 5 (5! = 120) using a for loop counting down. Exit with code 120.

7. **Array reverse.** Given `arr dd 1, 2, 3, 4, 5`, reverse the array in place to get `5, 4, 3, 2, 1`. Exit with code = first element after reversal (5).

8. **Linear search.** Search arr for value 42. If found, exit with index; if not found, exit with -1 (bitwise: exit code 255).

9. **Bubble sort.** Implement one pass of bubble sort on `arr dd 5, 3, 8, 1, 9`. The largest element should "bubble" to the end. Exit with code = last element (9, but verify the array is `3, 5, 1, 8, 9` after one pass).

10. **FizzBuzz.** Count from 1 to 30. For each number: if divisible by 3, add 1 to r8; if by 5, add 1 to r9; if by both (15), add 1 to r10. Uses `div` and `cmp` with `je`. Exit with code = r10 (should be 2, for 15 and 30).

## 9. Self-check questions

- [ ] What flags does `cmp` set? How are they different from `sub`?
- [ ] What is the difference between `jg` and `ja`? Between `jl` and `jb`?
- [ ] When do you use `test rax, rax` instead of `cmp rax, 0`?
- [ ] In an if/else pattern, why do you need `jmp` after the if-body?
- [ ] How does `cmp a, b; jl target` decide whether to jump? (What relationship between flags?)
- [ ] If `rax = 0x80` (128 unsigned, -128 signed) and `rbx = 0x7F` (127), what does `jg` say? What does `ja` say?
- [ ] Can you check "a >= b" with a single jump instruction? If so, which one for signed? For unsigned?
- [ ] What does `js` check? When would a `cmp` result be negative?
- [ ] What is the difference between `jz` and `je`?
- [ ] How do you implement a for loop with a variable number of iterations?

## 10. What's next

You now have branching and looping in your assembly toolkit. You can write programs that make decisions, repeat operations, and work with arrays.

In the next lesson — **the stack and subroutines**: how to organize code into reusable functions (`call`/`ret`), pass data through the stack, and build modular programs.
