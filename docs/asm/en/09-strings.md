# [09] Strings and REP instructions

> **Track:** Assembly · **Level:** 09 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

Strings are everywhere in programming — text output, file names, user input, configuration data. In C, a string is an array of bytes ending with a null byte (`\0`):

```c
char* msg = "Hello";  // 'H' 'e' 'l' 'l' 'o' '\0'
```

Working with strings in assembly means:
- **Finding length** — counting bytes until null
- **Copying** — moving bytes from one place to another
- **Comparing** — checking if two strings are equal
- **Concatenating** — appending one string to another

We could do all of this with loops (like we did in level 06), but x86-64 has **dedicated string instructions** that process bytes (or words/doublewords/quadwords) in a single operation, often with a **repeat prefix** (`rep`) that makes them run in hardware loops.

These instructions are:
- **`lodsb`/`lodsw`/`lodsd`/`lodsq`** — Load String: read from memory into AL/AX/EAX/RAX
- **`stosb`/`stosw`/`stosd`/`stosq`** — Store String: write from AL/AX/EAX/RAX to memory
- **`movsb`/`movsw`/`movsd`/`movsq`** — Move String: copy from one memory to another
- **`scasb`/`scasw`/`scasd`/`scasq`** — Scan String: compare AL/AX/EAX/RAX with memory
- **`cmpsb`/`cmpsw`/`cmpsd`/`cmpsq`** — Compare String: compare two memory locations

And the repeat prefixes:
- **`rep`** — repeat while RCX > 0 (decrementing RCX each iteration)
- **`repe`/`repz`** — repeat while RCX > 0 AND ZF == 1
- **`repne`/`repnz`** — repeat while RCX > 0 AND ZF == 0

## 2. Core concept (absolute zero)

### 2.1 The source and destination registers

String instructions use:
- **`RSI`** (R/SI) — **S**ource Index: points to source memory
- **`RDI`** (R/DI) — **D**estination Index: points to destination memory
- **`RCX`** — repeat counter (for `rep`)
- **`AL`/`AX`/`EAX`/`RAX`** — the accumulator used by lods/stos/scas

### 2.2 The direction flag (DF)

The **direction flag** in RFLAGS determines whether string instructions **increment** or **decrement** RSI/RDI after each operation:

| DF | RSI/RDI after operation | Mnemonic |
|:--:|:----------------------:|:--------:|
| 0 | Increment (forward) | `cld` (CLear Direction) |
| 1 | Decrement (backward) | `std` (SeT Direction) |

Always use `cld` to set forward direction before string operations (the OS may leave DF in an unknown state).

### 2.3 `lodsb` — Load String Byte

```assembly
lodsb    ; al = [rsi]; rsi += 1 (if DF=0) or rsi -= 1 (if DF=1)
```

Variants:
| Instruction | Size loaded | Register | RSI change |
|:-----------:|:----------:|:--------:|:----------:|
| `lodsb` | 1 byte | AL | ±1 |
| `lodsw` | 2 bytes | AX | ±2 |
| `lodsd` | 4 bytes | EAX | ±4 |
| `lodsq` | 8 bytes | RAX | ±8 |

**Usage:** Reading a string character by character:

```assembly
cld                  ; forward direction
lea  rsi, [my_str]   ; rsi = address of string
lodsb                ; al = 'H', rsi now points to 'e'
lodsb                ; al = 'e', rsi now points to 'l'
```

### 2.4 `stosb` — Store String Byte

```assembly
stosb    ; [rdi] = al; rdi += 1 (if DF=0) or rdi -= 1 (if DF=1)
```

Variants: `stosb`, `stosw`, `stosd`, `stosq`

**Usage:** Writing a string to a buffer:

```assembly
cld
lea  rdi, [buffer]   ; rdi = destination
mov  al, 'A'
stosb                ; buffer[0] = 'A'
mov  al, 'B'
stosb                ; buffer[1] = 'B'
mov  al, 0           ; null terminator
stosb                ; buffer[2] = 0
```

### 2.5 `movsb` — Move String Byte

```assembly
movsb    ; [rdi] = [rsi]; rsi++, rdi++ (if DF=0)
```

Variants: `movsb`, `movsw`, `movsd`, `movsq`

**Usage:** Copying memory:

```assembly
cld
lea  rsi, [source]   ; source address
lea  rdi, [dest]     ; destination address
movsb                ; copies 1 byte from [rsi] to [rdi], advances both
```

### 2.6 `scasb` — Scan String Byte

```assembly
scasb    ; compare al with [rdi]; rdi += 1 (if DF=0)
         ; sets flags (ZF, SF, etc.) like cmp
```

Variants: `scasb`, `scasw`, `scasd`, `scasq`

**Usage:** Searching for a character in a string:

```assembly
cld
lea  rdi, [my_str]   ; string to search
mov  al, 'e'         ; character to find
scasb                ; compare 'e' with first char; rdi++
; if ZF == 1, we found 'e'
```

### 2.7 `cmpsb` — Compare String Byte

```assembly
cmpsb    ; compare [rsi] with [rdi]; rsi++, rdi++
         ; sets flags like cmp
```

Variants: `cmpsb`, `cmpsw`, `cmpsd`, `cmpsq`

**Usage:** Comparing two strings:

```assembly
cld
lea  rsi, [str1]
lea  rdi, [str2]
cmpsb                ; compare str1[0] with str2[0]; advance both
; ZF = 1 if they're equal
```

### 2.8 The `rep` prefix

`rep` repeats an instruction RCX times, decrementing RCX each time:

```assembly
mov  rcx, 10         ; repeat 10 times
rep  movsb           ; copy 10 bytes from [rsi] to [rdi]
```

Equivalent to:
```assembly
.loop:
    movsb
    dec  rcx
    jnz  .loop
```

**But `rep` is faster** — it's a single instruction that loops internally in the CPU microarchitecture.

### 2.9 `repe`/`repne` — conditional repeat

- **`repe`** (repeat while equal): repeat while RCX > 0 AND ZF == 1
- **`repne`** (repeat while not equal): repeat while RCX > 0 AND ZF == 0

These are primarily used with `scas` and `cmps`:

```assembly
; Find first non-'A' character in a string
mov  al, 'A'
lea  rdi, [str]
mov  rcx, 100         ; max 100 chars
repe scasb            ; scan while equal to 'A' and rcx > 0
; rdi points to the first non-'A' (or end of buffer)
```

## 3. Step-by-step breakdown

### 3.1 `strlen` — string length

```assembly
; strlen.asm — compute string length using scasb
section .data
    msg db "Hello, World!", 0

section .text
    global _start

_start:
    lea  rdi, [msg]
    call strlen

    ; rax = length (13)
    mov  edi, eax
    mov  eax, 60
    syscall

; int strlen(const char* str)
; Returns length of null-terminated string (not counting null)
strlen:
    push rbp
    mov  rbp, rsp
    push rcx             ; save rcx

    cld                  ; forward direction
    mov  rcx, -1         ; maximum possible count
    xor  al, al          ; al = 0 (null terminator to search for)
    lea  rdi, [rdi]      ; rdi already points to string
    repne scasb          ; scan until null byte or rcx = 0
    ; At this point: rdi points past the null byte
    ; rcx = -1 - length - 1 (we decremented from -1)
    ; Actually: rcx starts at -1 (0xFFFFFFFFFFFFFFFF)
    ; After repne scasb finds the null, rcx = -1 - length - 1

    ; Length = (-1 - rcx) - 1 = -rcx - 2
    ; We can compute: not rcx (bitwise NOT) gives us: -rcx - 1
    ; Then subtract 1 more
    mov  rax, rcx
    not  rax              ; rax = -rcx - 1
    dec  rax              ; rax = -rcx - 2 = length

    pop  rcx
    pop  rbp
    ret
```

Let me explain the `strlen` trick more clearly:

- `rcx` starts at -1 (0xFFFFFFFFFFFFFFFF)
- `repne scasb` decrements rcx each iteration
- When null is found, we've scanned `length + 1` bytes (including null)
- `rcx = -1 - (length + 1)`
- We want `length`
- `NOT rcx → (-rcx - 1) = length + 1`
- `DEC rax → length`

### 3.2 `strcpy` — string copy

```assembly
; strcpy.asm — copy string using movsb
section .data
    src db "Hello, World!", 0

section .bss
    dst resb 32           ; 32 bytes for destination

section .text
    global _start

_start:
    lea  rdi, [src]
    lea  rsi, [dst]
    call strcpy

    mov  eax, 60
    xor  edi, edi
    syscall

; void strcpy(char* dest, const char* src)
; Arguments: rdi = dest, rsi = src
strcpy:
    push rbp
    mov  rbp, rsp
    push rcx
    push rdi             ; save dest (need it to find length)

    cld

    ; First, find length of src
    mov  rcx, -1
    xor  al, al
    ; rsi is src, but scasb uses rdi, so we need to swap
    ; Actually, let's use a different approach:
    ; Save src pointer and scan from it
    xchg rsi, rdi        ; swap: rdi = src, rsi = dest (we'll fix later)
    push rsi             ; save dest (now in rsi)
    repne scasb          ; find null in src
    ; rcx = -(len + 2) approximately

    ; Compute len + 1 (include null byte)
    mov  rax, rcx
    not  rax             ; len + 2
    dec  rax             ; len + 1

    ; Now copy movsb with rep
    ; rsi is still the original src? No, we swapped...
    ; Let me redo this more carefully:

    pop  rsi             ; rsi = dest (was pushed earlier)
    ; Actually this got confusing. Let's write a cleaner version.

    ; Let's restart the approach properly:
    pop  rdi             ; restore original rdi (dest)
    pop  rcx
    pop  rbp
    ret

; Cleaner version:
; strcpy_clean(char* dest, const char* src)
strcpy_clean:
    push rbp
    mov  rbp, rsp
    push rcx
    push rsi
    push rdi

    cld
    ; Find length of src
    mov  rdi, rsi        ; rdi = src (for scasb)
    mov  rcx, -1
    xor  al, al
    repne scasb
    ; rcx = -(len + 2)
    not  rcx             ; rcx = len + 1 (including null)

    ; Restore source into rsi, dest into rdi
    mov  rsi, rsi        ; rsi = src (already in rsi from argument)
    ; Actually rsi was overwritten by scasb? No, scasb uses rdi, not rsi.
    ; rsi still = src. Good.
    ; But rdi now = &src[len+1] (past the null)
    ; We need dest back in rdi. We saved it in push rdi.
    pop  rdi             ; rdi = dest (original argument)
    push rdi             ; save it again for later

    ; Now rsi = src, rdi = dest, rcx = bytes to copy (including null)
    rep  movsb           ; copy entire string including null

    pop  rdi
    pop  rsi
    pop  rcx
    pop  rbp
    ret
```

Actually, the above is messy because I'm writing it inline. Let me provide a clean, simple implementation:

### 3.3 `strcpy` — clean implementation

```assembly
; Simple strcpy using rep movsb
; First find length, then copy
strcpy:
    push rbp
    mov  rbp, rsp
    push rcx
    push rdi
    push rsi

    cld
    ; --- Step 1: find length of src (in rsi) ---
    mov  rdi, rsi        ; rdi = src (for scasb)
    mov  rcx, -1
    xor  al, al
    repne scasb          ; scan until null
    ; After: rcx = -(length + 2) — we scanned len+1 bytes
    not  rcx             ; rcx = length + 1 + 1 = len + 2?? 
    ; NOT of -(len+2) = (len+2)-1 = len+1... let's be precise:
    ; rcx starts at -1 (0xFFFFFFFFFFFFFFFF)
    ; After scanning len+1 bytes: rcx = -(len+1) - 1 = -(len+2)
    ; NOT rcx = (len+2) - 1 = len + 1 ← this is what we want

    ; Wait: -1 in two's complement is 0xFFFFFFFFFFFFFFFF
    ; After repne scasb: rcx = -1 - (len+1) = -(len+2)
    ; NOT: ~(-(len+2)) = (len+2)-1 = len+1 ✓
    ; Actually: ~(-x) = x-1, so ~(-(len+2)) = (len+2)-1 = len+1 ✓

    ; --- Step 2: copy ---
    ; Restore rdi to dest (popped from stack saved earlier)
    ; But we need to pop in reverse order... 
    ; This is getting confusing. Let me use a different approach.

    ; Actually let me just pop the saved values and restore them,
    ; then use a simple byte-by-byte or rep movsb approach.

    pop  rsi             ; rsi = original src
    pop  rdi             ; rdi = original dest

    ; Now rcx = length + 1 (including null)
    rep  movsb           ; copy all bytes

    pop  rcx
    pop  rbp
    ret
```

Hmm, the saved register management is getting tangled. Let me provide a much cleaner version that doesn't have bugs:

### 3.4 `strlen` — simple

```assembly
; strlen using repne scasb
strlen:
    push rbp
    mov  rbp, rsp

    cld
    mov  rcx, -1         ; maximum count
    xor  al, al          ; search for null
    ; rdi already has the string address
    repne scasb          ; scan
    ; rcx = -(length + 2)
    not  rcx             ; rcx = length + 1
    dec  rcx             ; rcx = length

    mov  rax, rcx        ; return length

    pop  rbp
    ret
```

Wait, `not` on unsigned: if rcx = -(len+2), then `not rcx` = `~(-(len+2))` = `(len+2)-1` = `len+1`. Then `dec rcx` = len. That's correct for `not`. But NOT is bitwise complement. The complement of -x is x-1 (for x > 0). So `~(-(len+2))` = `(len+2)-1` = `len+1`. Then `dec` gives `len`. ✓

OK, let me just write the whole thing cleanly without all the commentary-in-code:

### 3.5 `strcat` and `strcmp`

For `strcat`, find the end of dest, then copy src to that point.

For `strcmp`, use `repe cmpsb` to compare byte by byte while equal.

## 4. Complete examples

### 4.1 `rep stosb` — fill memory with a value

```assembly
; memset equivalent — fill buffer with 'A'
section .bss
    buffer resb 256

section .text
    global _start

_start:
    cld
    lea  rdi, [buffer]
    mov  al, 'A'         ; value to fill
    mov  rcx, 256        ; count
    rep  stosb           ; fill 256 bytes with 'A'

    mov  eax, 60
    xor  edi, edi
    syscall
```

### 4.2 `rep movsb` — block copy

```assembly
; memcpy equivalent — copy 64 bytes
section .data
    src_data times 64 db 0x42    ; 64 bytes of 0x42

section .bss
    dst_data resb 64

section .text
    global _start

_start:
    cld
    lea  rsi, [src_data]
    lea  rdi, [dst_data]
    mov  rcx, 64
    rep  movsb           ; copy 64 bytes

    mov  eax, 60
    xor  edi, edi
    syscall
```

### 4.3 `repne scasb` — search for a character

```assembly
; Find first occurrence of 'l' in "Hello"
section .data
    msg db "Hello, World!", 0

section .text
    global _start

_start:
    cld
    lea  rdi, [msg]
    mov  al, 'l'         ; character to find
    mov  rcx, -1         ; max count
    repne scasb          ; search
    ; If found: ZF = 1, rdi points to byte AFTER 'l'
    ; If not found: ZF = 0, rcx = 0

    ; Compute position: position = rdi - msg - 1
    ; (because rdi advanced past the found char)
    sub  rdi, msg
    dec  rdi             ; rdi = index of 'l' (first occurrence = 2)

    mov  eax, 60
    mov  edi, edi        ; exit with position
    syscall
```

## 5. Complete string library

```assembly
; string_lib.asm — complete string functions library
section .text

; ─── strlen: compute string length ───
; Input:  rdi = pointer to null-terminated string
; Output: rax = length (not counting null)
; Uses:   al, rcx, rdi
global strlen
strlen:
    push rbp
    mov  rbp, rsp

    cld
    mov  rcx, -1
    xor  al, al
    repne scasb          ; scan for null
    not  rcx
    dec  rcx
    mov  rax, rcx

    pop  rbp
    ret

; ─── strcpy: copy string ───
; Input:  rdi = dest, rsi = src
; Output: rax = dest (pointer to destination)
; Uses:   al, rcx, rdi, rsi
global strcpy
strcpy:
    push rbp
    mov  rbp, rsp
    push rdi             ; save dest

    cld
    ; Find length of src
    mov  rdi, rsi        ; rdi = src
    mov  rcx, -1
    xor  al, al
    repne scasb
    not  rcx             ; rcx = length + 1 (including null)

    ; Copy
    mov  rdi, [rbp - 8]  ; rdi = dest (popped conceptually)
    ; Actually we pushed rdi, so it's at [rbp - 8] + ...
    ; Let me just restore from the stack:
    mov  rdi, [rsp + 8]  ; rdi = saved dest (above push rdi)
    ; No wait, rsp changed after push rbp. Let me rethink.
    ; Stack: [rsp] = saved rdi, [rsp+8] = saved rbp, [rsp+16] = ret addr
    ; But rbp = old rsp after push rbp; mov rbp, rsp
    ; So: [rbp - 8] = saved rdi, [rbp] = saved rbp, [rbp+8] = ret addr
    mov  rdi, [rbp - 8]  ; rdi = dest

    rep  movsb           ; copy

    mov  rax, [rbp - 8]  ; return dest pointer

    pop  rdi
    pop  rbp
    ret

; ─── strcat: concatenate strings ───
; Input:  rdi = dest, rsi = src
; Output: rax = dest
; Uses:   al, rcx, rdi, rsi
global strcat
strcat:
    push rbp
    mov  rbp, rsp
    push rdi             ; save dest

    cld
    ; Find end of dest
    mov  rcx, -1
    xor  al, al
    repne scasb          ; rdi now points past null byte of dest
    dec  rdi             ; rdi = position of null byte

    ; Now copy src to this position
    ; rdi was modified by scasb; rsi is still src
    push rdi             ; save copy destination
    mov  rdi, rsi        ; rdi = src (to find length)
    mov  rcx, -1
    xor  al, al
    repne scasb
    not  rcx             ; rcx = length of src + 1

    pop  rdi             ; rdi = insertion point in dest
    ; rsi = src (from argument) — but was unchanged? No, we changed rdi = rsi
    ; rsi still = original src? Let me trace: rsi was argument, never changed in scasb
    ; scasb only modifies rdi (and flags, al, rcx). rsi is untouched.
    ; So rsi is still the original src. ✓

    rep  movsb           ; append src (including null)

    mov  rax, [rbp - 8]  ; return dest

    pop  rdi
    pop  rbp
    ret

; ─── strcmp: compare strings ───
; Input:  rdi = str1, rsi = str2
; Output: rax = 0 if equal, nonzero if different
; Uses:   al, cx, rdi, rsi
global strcmp
strcmp:
    push rbp
    mov  rbp, rsp

    cld
.loop:
    cmpsb                ; compare one byte
    jne  .not_equal      ; if different, done
    ; Check if we just compared the null terminator
    cmp  byte [rdi - 1], 0   ; was the byte we just read null?
    ; Actually cmpsb already advanced both. We need to check the byte
    ; that was just compared. [rdi-1] is the byte from str2.
    cmp  byte [rdi - 1], 0
    je   .equal           ; if null, strings are equal (both reached end)

    jmp  .loop

.equal:
    xor  eax, eax        ; return 0 (equal)
    pop  rbp
    ret

.not_equal:
    ; Return difference of the differing bytes
    mov  al, [rdi - 1]   ; byte from str1
    sub  al, [rsi - 1]   ; subtract byte from str2
    movsx rax, al        ; sign-extend to 64-bit
    pop  rbp
    ret
```

## 6. Common mistakes

### Mistake 1: Forgetting to set DF with `cld`

```assembly
; BUG: DF might be 1 (backward direction)
rep  movsb    ; copies in wrong direction!

; CORRECT:
cld
rep  movsb
```

### Mistake 2: Wrong argument order for `movsb`

```assembly
; movsb moves FROM [rsi] TO [rdi]
lea  rsi, [source]     ; SOURCE in RSI
lea  rdi, [dest]       ; DEST in RDI
rep  movsb             ; copies source → dest
```

This is easy to get backwards — RSI is the source, RDI is the destination.

### Mistake 3: Not counting the null terminator

```assembly
; Overwriting scasb's register usage
strlen:
    lea  rdi, [msg]
    mov  rcx, -1
    xor  al, al
    repne scasb
    not  rcx
    dec  rcx
    ; rcx = length (not including null) ✓

; But for strcpy:
    mov  rcx, length    ; BUG: copies only the string, no null terminator!
    rep  movsb
    ; dest has the string but no null — it's not a valid C string

; CORRECT:
    mov  rcx, length + 1  ; include null terminator
    rep  movsb
```

### Mistake 4: Using `lodsb`/`stosb` without setting up RSI/RDI

```assembly
lodsb    ; reads from [rsi] — but rsi hasn't been set!
stosb    ; writes to [rdi] — but rdi hasn't been set!
```

Always set RSI (source) and RDI (destination) before using string instructions.

### Mistake 5: Confusing `lodsb` vs. `stosb`

- `lodsb` → **Load** from memory into **AL** (RSI is source)
- `stosb` → **Store** from **AL** into memory (RDI is destination)

Think: "Load String into AL" and "Store String from AL".

### Mistake 6: Using `repe scasb` when you need `repne scasb`

```assembly
; Search for character 'x':
mov  al, 'x'
repe scasb    ; BUG: stops when character DOESN'T match OR when ZF=0
              ; This stops at the first NON-matching character

repne scasb   ; CORRECT: stops when character matches (ZF=1) or rcx=0
```

- `repne` = repeat while **not equal** → stops when EQUAL (found it)
- `repe` = repeat while **equal** → stops when NOT EQUAL (found mismatch)

### Mistake 7: Using `cmpsb` with RSI/RDI pointing to different sized elements

```assembly
; Comparing strings byte by byte:
cld
repe cmpsb    ; correct — compares bytes

; But if you use cmpsd (4 bytes at a time):
repe cmpsd    ; compares 4 bytes at once — may read past string!
```

## 7. Exercises

1. **strlen.** Write a program that computes the length of "Assembly" and exits with that value (8).

2. **strcpy.** Write a program that copies "Hello" from src to dst and exits with code = dst[0] ('H' = 72).

3. **strcat.** Write `strcat` that appends " World" to "Hello" to form "Hello World". Exit with the length of the result (11).

4. **strcmp.** Write `strcmp` that compares "abc" and "abc" — exit with 0. Then compare "abc" and "abd" — should return nonzero.

5. **rep stosb.** Fill a 100-byte buffer with the value 0xFF using `rep stosb`. Exit with code = buffer[50] (should be 255).

6. **rep movsb.** Copy a 50-byte array from src to dst using `rep movsq` (8 bytes at a time). How many iterations? Exit with code = dst[49].

7. **Character count.** Count how many times the letter 'o' appears in "Hello World, this is assembly!". Use `repne scasb` in a loop. Exit with the count.

8. **Uppercase conversion.** Convert a lowercase string "hello" to uppercase "HELLO" in place (subtract 32 from each byte). Use `lodsb` and `stosb`. Exit with code = first byte after conversion ('H' = 72).

9. **strstr implementation.** Write a function that finds the first occurrence of substring "world" in "hello world". Return the position (index) in rax.

10. **String reverse.** Reverse a string in place: "hello" → "olleh". Use RSI pointing to start and RDI pointing to end (use `std` for backward direction). Swap characters. Exit with code = first byte of reversed string ('o' = 111).

## 8. Self-check questions

- [ ] What do RSI and RDI stand for? Which is source and which is destination?
- [ ] What does `cld` do? What happens if you forget it?
- [ ] What is the difference between `lodsb` and `stosb`?
- [ ] What does `rep` do? What register does it use as counter?
- [ ] What does `repne scasb` do? When does it stop?
- [ ] How do you compute string length using `repne scasb`?
- [ ] What's the difference between `repe cmpsb` and `repne cmpsb`?
- [ ] How many bytes does `movsq` move? What about `movsb`?
- [ ] After a `lodsb`, what happens to RSI?
- [ ] How do you fill a buffer with a constant value using string instructions?

## 9. What's next

You now have a complete toolkit for string and memory operations. The string instructions (`lodsb`/`stosb`/`movsb`/`scasb`/`cmpsb`) with `rep` prefixes are among the most efficient ways to process memory on x86-64.

In the next and final lesson — **Capstone: C + Assembly**: how to combine C and assembly in one project, call C functions from assembly, call assembly functions from C, compile them together with gcc, and understand when to use assembly today.
