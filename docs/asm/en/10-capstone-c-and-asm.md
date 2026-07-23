# [10] Capstone — C + Assembly

> **Track:** Assembly · **Level:** 10 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

We've spent 9 lessons writing pure assembly. Assembly is powerful, but for most tasks, C is more productive and portable. The real world uses **both**: C for high-level logic and assembly for low-level optimization, hardware access, or operations that C can't express.

The problems we solve in this lesson:

1. **How do we call C functions (like `printf`) from assembly?**
2. **How do we write assembly functions that C can call?**
3. **How do we compile and link .c and .asm files together?**
4. **What is `extern` and `global` in the context of mixed-language projects?**
5. **When does it actually make sense to use assembly instead of C?**

## 2. Core concept (absolute zero)

### 2.1 `global` — exporting symbols

When we write `global _start`, we tell the linker: "the symbol `_start` is available for other object files to use." The linker needs `_start` as the program entry point.

```assembly
section .text
    global my_function    ; my_function can be called from other .o files

my_function:
    ; ... function body ...
```

Without `global`, `my_function` is only visible within the same assembly file (it's a **local symbol**). With `global`, it becomes an **external symbol** that the linker can resolve across object files.

### 2.2 `extern` — importing symbols

When we want to call a function defined in another object file (like a C function), we declare it as `extern`:

```assembly
extern printf            ; printf is defined elsewhere (in libc)
extern my_c_function     ; defined in a .c file

section .text
    call my_c_function
    call printf
```

`extern` tells the assembler: "this symbol exists, but don't worry about defining it — the linker will find it."

### 2.3 Name mangling

**C** does not mangle names. A function `my_func` in C appears as `my_func` in the object file — exactly the same name.

**C++** does mangle names (adds type information to the symbol). This is why you can't directly call a C++ function from assembly unless you use `extern "C"`:

```cpp
// In C++, this function has the C calling convention (no name mangling):
extern "C" void my_cpp_func(int x);
```

**Assembly** doesn't mangle names either. So assembly and C can freely call each other — as long as you follow the ABI (lesson 08).

### 2.4 `main` vs `_start`

In pure assembly, we use `_start` as the entry point. The OS calls `_start` directly.

When mixing with C, we usually use `main` as our entry point. The C runtime (CRT) provides `_start`, which calls `main`. This way, the C library (libc) is initialized before `main` runs:

```c
// main.c
#include <stdio.h>

int main() {
    printf("Hello from C!\n");
    return 0;
}
```

```bash
gcc main.c -o program   # _start (from CRT) → main (our code)
```

### 2.5 Compiling mixed projects

To compile a project with both .c and .asm files:

```bash
# Step 1: Assemble the .asm file to .o
nasm -f elf64 my_asm.asm -o my_asm.o

# Step 2: Compile the .c file to .o
gcc -c my_c.c -o my_c.o

# Step 3: Link them together
gcc my_c.o my_asm.o -o program

# Or in one command:
gcc -o program my_c.c my_asm.asm -l:my_asm.o
# Actually, gcc can compile .c and link .o together:
nasm -f elf64 my_asm.asm -o my_asm.o
gcc -c my_c.c -o my_c.o
gcc my_c.o my_asm.o -o program
```

Or more simply, using gcc's linker with nasm output:
```bash
nasm -f elf64 func.asm -o func.o
gcc main.c func.o -o program
```

## 3. Step-by-step breakdown

### 3.1 Calling C's `printf` from assembly

```assembly
; hello_printf.asm — call printf from assembly
section .data
    msg db "Hello from assembly! Count: %d", 10, 0
    val dq 42

section .text
    global main
    extern printf          ; printf is in libc

main:
    push rbp
    mov  rbp, rsp

    ; printf(format_string, arg1, arg2, ...)
    ; Uses the System V ABI:
    ;   rdi = format string
    ;   rsi = first argument
    ;   rdx = second argument
    ;   etc.

    mov  rdi, msg          ; format string
    mov  rsi, [val]        ; %d = 42
    xor  eax, eax          ; AL = number of vector registers used (0 for no floats)
    call printf

    ; Return 0
    xor  eax, eax

    pop  rbp
    ret
```

```bash
nasm -f elf64 hello_printf.asm -o hello_printf.o
gcc hello_printf.o -no-pie -o hello_printf
./hello_printf
# Output: Hello from assembly! Count: 42
```

**Important:** Before calling a variadic function like `printf`, you must set `AL` to the number of floating-point arguments passed in vector registers (xmm0-xmm7). For no floats, `xor eax, eax`. This is part of the System V ABI.

### 3.2 Calling assembly function from C

```asm
; fast_math.asm — assembly functions callable from C
section .text
    global multiply        ; visible to C
    global factorial        ; visible to C

; int multiply(int a, int b)
; Arguments: rdi = a, rsi = b (from System V ABI)
; Returns:   rax = a * b
multiply:
    push rbp
    mov  rbp, rsp
    mov  rax, rdi
    imul rax, rsi
    pop  rbp
    ret

; int factorial(int n)
; Arguments: rdi = n
; Returns:   rax = n!
factorial:
    push rbp
    mov  rbp, rsp

    cmp  rdi, 1
    jle  .base

    push rdi
    dec  rdi
    call factorial
    pop  rdi
    imul rax, rdi

    pop  rbp
    ret

.base:
    mov  rax, 1
    pop  rbp
    ret
```

```c
// main.c — calls assembly functions
#include <stdio.h>

// Declare the assembly functions
extern int multiply(int a, int b);
extern int factorial(int n);

int main() {
    int prod = multiply(6, 7);
    printf("6 * 7 = %d\n", prod);  // 42

    int fact = factorial(5);
    printf("5! = %d\n", fact);     // 120

    return 0;
}
```

```bash
nasm -f elf64 fast_math.asm -o fast_math.o
gcc main.c fast_math.o -o program
./program
# Output:
# 6 * 7 = 42
# 5! = 120
```

### 3.3 Calling C function from assembly (with arguments)

```assembly
; call_c.asm — call C functions from assembly
section .data
    fmt db "Sum: %d", 10, 0

section .text
    global main
    extern printf          ; from libc
    extern add_numbers     ; from our C file

main:
    push rbp
    mov  rbp, rsp

    ; Call C function: int add_numbers(int a, int b, int c)
    mov  rdi, 10
    mov  rsi, 20
    mov  rdx, 30
    call add_numbers       ; rax = 60

    ; Print result using printf
    mov  rdi, fmt
    mov  rsi, rax
    xor  eax, eax
    call printf

    xor  eax, eax
    pop  rbp
    ret
```

```c
// helper.c
int add_numbers(int a, int b, int c) {
    return a + b + c;
}
```

```bash
nasm -f elf64 call_c.asm -o call_c.o
gcc -c helper.c -o helper.o
gcc call_c.o helper.o -o program
./program
# Output: Sum: 60
```

### 3.4 Handling floating point

```assembly
; float_mix.asm — assembly with floats, callable from C
section .text
    global compute

; double compute(double x, int n)
; xmm0 = x, rdi = n
; returns: xmm0 = x^n (power by repeated multiplication)
compute:
    push rbp
    mov  rbp, rsp

    movsd xmm1, xmm0      ; xmm1 = x (base)
    mov  rcx, rdi         ; rcx = n
    dec  rcx              ; rcx = n - 1 (first multiplication uses base)
    movsd xmm0, [one]     ; xmm0 = 1.0

.loop:
    test rcx, rcx
    jz   .done
    mulsd xmm0, xmm1      ; result *= base
    dec  rcx
    jmp  .loop

.done:
    pop  rbp
    ret

section .data
one: dq 1.0
```

```c
// main_float.c
#include <stdio.h>

extern double compute(double x, int n);

int main() {
    double result = compute(2.0, 10);
    printf("2^10 = %.0f\n", result);  // 1024
    return 0;
}
```

### 3.5 String function in assembly, called from C

Let's write a fast `strlen` in assembly and call it from C:

```asm
; asm_strlen.asm — optimized strlen in assembly
section .text
    global asm_strlen

; size_t asm_strlen(const char* str)
; Uses SCASB for hardware-accelerated string scanning
asm_strlen:
    push rbp
    mov  rbp, rsp

    cld
    mov  rcx, -1          ; maximum count
    xor  al, al           ; search for null
    ; rdi already has the string pointer
    repne scasb           ; scan until null
    not  rcx              ; rcx = length + 1
    dec  rcx              ; rcx = length

    mov  rax, rcx

    pop  rbp
    ret
```

```c
// strlen_test.c
#include <stdio.h>
#include <string.h>

extern size_t asm_strlen(const char* str);

int main() {
    const char* test = "Hello, Assembly!";

    size_t len_c = strlen(test);
    size_t len_asm = asm_strlen(test);

    printf("C strlen:      %zu\n", len_c);
    printf("Assembly strlen: %zu\n", len_asm);
    printf("Results %s\n", (len_c == len_asm) ? "MATCH ✓" : "MISMATCH ✗");

    return 0;
}
```

### 3.6 Benchmark: assembly vs C strlen

```c
// benchmark.c
#include <stdio.h>
#include <string.h>
#include <time.h>

extern size_t asm_strlen(const char* str);

#define ITERATIONS 100000000

int main() {
    const char* test = "This is a test string to measure strlen performance!";
    size_t result;
    clock_t start, end;

    // Benchmark C strlen
    start = clock();
    for (long i = 0; i < ITERATIONS; i++) {
        result = strlen(test);
    }
    end = clock();
    double time_c = (double)(end - start) / CLOCKS_PER_SEC;

    // Benchmark assembly strlen
    start = clock();
    for (long i = 0; i < ITERATIONS; i++) {
        result = asm_strlen(test);
    }
    end = clock();
    double time_asm = (double)(end - start) / CLOCKS_PER_SEC;

    printf("C strlen:       %.3f seconds\n", time_c);
    printf("Assembly strlen: %.3f seconds\n", time_asm);
    printf("Speedup: %.2fx\n", time_c / time_asm);

    return 0;
}
```

```bash
nasm -f elf64 asm_strlen.asm -o asm_strlen.o
gcc benchmark.c asm_strlen.o -O2 -o benchmark
./benchmark
# Typical output (varies by CPU):
# C strlen:       0.512 seconds
# Assembly strlen: 0.487 seconds
# Speedup: 1.05x
```

**Note:** Modern compilers with `-O2` often inline `strlen` or use very efficient implementations. Your hand-written assembly may not always be faster — that's the reality of modern optimizing compilers!

## 4. Complete project: word counter

Let's build a mixed C+Assembly project that counts words in a string.

### 4.1 Assembly function: `is_space`

```asm
; word_utils.asm
section .text
    global is_space
    global to_upper

; int is_space(char c)
; Returns 1 if c is whitespace, 0 otherwise
; rdi = character (actually only the lower byte matters)
is_space:
    push rbp
    mov  rbp, rsp

    mov  al, dil          ; get the character
    cmp  al, ' '
    je   .yes
    cmp  al, 9            ; tab
    je   .yes
    cmp  al, 10           ; newline
    je   .yes

    xor  eax, eax         ; return 0
    pop  rbp
    ret

.yes:
    mov  eax, 1
    pop  rbp
    ret

; char to_upper(char c)
; Converts lowercase letter to uppercase
to_upper:
    push rbp
    mov  rbp, rsp

    mov  al, dil
    cmp  al, 'a'
    jb   .done
    cmp  al, 'z'
    ja   .done
    ; It's a lowercase letter
    sub  al, 32           ; convert to uppercase

.done:
    ; Upper byte of rax should be clean
    movzx eax, al
    pop  rbp
    ret
```

### 4.2 C main program

```c
// wordcount.c
#include <stdio.h>
#include <string.h>

extern int is_space(char c);
extern char to_upper(char c);

int count_words(const char* str) {
    int count = 0;
    int in_word = 0;

    while (*str) {
        if (is_space(*str)) {
            in_word = 0;
        } else {
            if (!in_word) {
                count++;
                in_word = 1;
            }
        }
        str++;
    }

    return count;
}

void to_upper_string(char* str) {
    while (*str) {
        *str = to_upper(*str);
        str++;
    }
}

int main() {
    char text[] = "hello world, this is assembly language!";

    printf("Original: %s\n", text);

    int words = count_words(text);
    printf("Word count: %d\n", words);

    to_upper_string(text);
    printf("Uppercase: %s\n", text);

    return 0;
}
```

```bash
nasm -f elf64 word_utils.asm -o word_utils.o
gcc wordcount.c word_utils.o -o wordcount
./wordcount
# Output:
# Original: hello world, this is assembly language!
# Word count: 6
# Uppercase: HELLO WORLD, THIS IS ASSEMBLY LANGUAGE!
```

## 5. Advanced: inline assembly (GCC)

GCC allows embedding assembly directly in C code using `asm()`:

```c
#include <stdio.h>

int main() {
    int a = 10, b = 20, result;

    // Inline assembly: add a and b, store in result
    asm (
        "addl %%ebx, %%eax;"   // eax += ebx
        : "=a" (result)        // output: result = eax
        : "a" (a), "b" (b)     // inputs: eax = a, ebx = b
        :                       // clobbered registers: none
    );

    printf("%d + %d = %d\n", a, b, result);  // 30

    return 0;
}
```

Extended inline assembly syntax:
```c
asm ( "instructions"
    : output_operands    // what comes out
    : input_operands     // what goes in
    : clobbered_regs     // what we destroy
);
```

**When to use inline assembly:**
- Single CPU instructions that C can't express (like `rdtsc`, `cpuid`)
- Fine-grained control in performance-critical inner loops
- Accessing special registers

**When NOT to use inline assembly:**
- When a separate .asm file works (it's cleaner)
- When the compiler can do it better (almost always)
- For portability (inline assembly is compiler-specific)

## 6. Complete program: fast memory copy with benchmarking

```asm
; fast_copy.asm — optimized memory copy using MOVSQ
section .text
    global fast_memcpy

; void* fast_memcpy(void* dest, const void* src, size_t n)
; rdi = dest, rsi = src, rdx = n (bytes)
; Returns: rax = dest
fast_memcpy:
    push rbp
    mov  rbp, rsp
    push rdi             ; save dest for return

    cld
    mov  rcx, rdx        ; rcx = byte count
    shr  rcx, 3          ; rcx = number of 8-byte chunks
    rep  movsq           ; copy 8 bytes at a time

    ; Handle remaining bytes
    mov  rcx, rdx
    and  rcx, 7          ; rcx = remaining bytes (0-7)
    rep  movsb           ; copy remaining bytes

    mov  rax, [rbp - 8]  ; return dest

    pop  rdi
    pop  rbp
    ret
```

```c
// memcpy_bench.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

extern void* fast_memcpy(void* dest, const void* src, size_t n);

#define SIZE (1024 * 1024 * 64)  // 64 MB
#define ITERATIONS 10

int main() {
    char* src = malloc(SIZE);
    char* dst1 = malloc(SIZE);
    char* dst2 = malloc(SIZE);

    // Fill source with data
    for (int i = 0; i < SIZE; i++) {
        src[i] = i & 0xFF;
    }

    clock_t start, end;

    // Benchmark libc memcpy
    start = clock();
    for (int i = 0; i < ITERATIONS; i++) {
        memcpy(dst1, src, SIZE);
    }
    end = clock();
    double time_libc = (double)(end - start) / CLOCKS_PER_SEC;

    // Benchmark our fast_memcpy
    start = clock();
    for (int i = 0; i < ITERATIONS; i++) {
        fast_memcpy(dst2, src, SIZE);
    }
    end = clock();
    double time_asm = (double)(end - start) / CLOCKS_PER_SEC;

    // Verify correctness
    int match = memcmp(dst1, dst2, SIZE) == 0;

    printf("Size: %d MB\n", SIZE / (1024 * 1024));
    printf("Iterations: %d\n", ITERATIONS);
    printf("libc memcpy:  %.3f s (%.2f MB/s)\n",
           time_libc, (SIZE * ITERATIONS / 1e6) / time_libc);
    printf("fast_memcpy:  %.3f s (%.2f MB/s)\n",
           time_asm, (SIZE * ITERATIONS / 1e6) / time_asm);
    printf("Correct: %s\n", match ? "YES" : "NO");

    free(src);
    free(dst1);
    free(dst2);

    return 0;
}
```

## 7. When to use assembly today

A realistic perspective on assembly language in 2026:

### Use assembly when:

| Task | Reason |
|------|--------|
| **Bootloaders and kernels** | Need direct control of hardware, no runtime |
| **CPU feature detection** | `cpuid`, `rdtsc` — no C equivalent |
| **Interrupt handlers** | Need precise register state control |
| **SIMD optimization** | Hand-tuned vector code can beat auto-vectorizers |
| **Reverse engineering** | Understanding binaries requires reading assembly |
| **Embedded systems** | Tight memory constraints, no OS |
| **Writing compilers** | You need to generate assembly output |
| **Security research** | Exploit development, malware analysis |

### Don't use assembly when:

| Task | Reason |
|------|--------|
| **Regular application code** | C/Rust compilers optimize better than humans |
| **Portability needed** | Assembly is CPU-specific |
| **Team maintenance** | Assembly is harder to read and maintain |
| **Quick prototyping** | Higher-level languages are faster to develop in |

### The golden rule:

> **Write in C, profile, identify bottlenecks, rewrite only the hottest 1-5% in assembly — and measure to confirm it's actually faster.**

Modern compilers (GCC, Clang) with `-O3` and `-march=native` generate remarkably good code. The era when humans routinely beat compilers ended around the 1990s. Today, assembly is for:
1. **Learning** — understanding how computers work at the lowest level (you've done this!)
2. **Hardware access** — things C can't express
3. **Working on hardware** — without an OS or runtime
4. **Performance** — only after profiling proves it's necessary

## 8. Common mistakes

### Mistake 1: Forgetting to set `AL` before calling `printf`

```assembly
call printf    ; WRONG if printf is variadic — AL has garbage

xor  eax, eax  ; CORRECT: AL = 0 (no floating-point args)
call printf
```

`printf` is a variadic function. The ABI requires AL to indicate the number of vector registers used for floating-point arguments.

### Mistake 2: Forgetting `no-pie` for position-independent code

```bash
gcc asm_file.o -o program
# Error: relocation R_X86_64_32 against `.data' can not be used when...
# Fix:
gcc asm_file.o -no-pie -o program
```

Or write position-independent assembly (use `lea` instead of `mov` with absolute addresses).

### Mistake 3: Mismatched calling convention

```asm
; Wrong: passing args in wrong registers
call my_c_func    ; my_c_func expects args in rdi, rsi, rdx, rcx, r8, r9
; If you put them in rbx, r12, etc., it won't work!

; Correct:
mov  rdi, arg1
mov  rsi, arg2
mov  rdx, arg3
call my_c_func
```

### Mistake 4: Name mismatch in `extern` and actual function name

```asm
extern printF    ; Wrong capitalization!
; ...
call printF      ; Linker error: undefined reference to 'printF'

extern printf    ; Correct
call printf
```

C function names are case-sensitive and unmangled.

### Mistake 5: Corrupting the stack in assembly called from C

If you write an assembly function called from C, you MUST:
- Preserve rbx, rbp, r12, r13, r14, r15 (callee-saved)
- Ensure RSP is 16-byte aligned at the point of any `call`
- Not return with RSP different from entry

```asm
my_func:
    push rbp
    mov  rbp, rsp
    ; ... do work ...
    pop  rbp
    ret               ; RSP must equal entry RSP
```

### Mistake 6: Using `_start` instead of `main` in mixed projects

```asm
; When linking with C runtime, use 'main', not '_start':
global main         ; Correct
; global _start     ; Wrong - conflicts with CRT's _start

main:
    ; ... code that can call C functions ...
    ret              ; return to libc's cleanup
```

## 9. Exercises

1. **Call `puts` from assembly.** Write an assembly program that calls C's `puts` function to print "Hello from assembly!". Use `extern puts` and `global main`.

2. **Call assembly from C.** Write an assembly function `int square(int n)` and call it from C. Print the result of squaring 12 (144).

3. **Two C functions from assembly.** Write an assembly program that calls `atoi("42")` and `atoi("100")` from C's standard library, adds them, then calls `printf` to print the result (142).

4. **Assembly string function.** Write an assembly `strcmp` and call it from C. Compare two strings and print whether they're equal.

5. **Benchmark.** Benchmark your assembly `strlen` against C's `strlen` with a long string (1000+ characters) and 10 million iterations. Report the speedup.

6. **Struct manipulation.** In C, define `struct Point { int x; int y; }`. In assembly, write a function `Point add_points(Point a, Point b)` that returns a+b (component-wise). Remember small structs may be returned in registers.

7. **Uppercase filter.** Write an assembly function `void to_upper_buffer(char* buf, size_t len)` and call it from C. Apply it to "hello world" and print the result.

8. **Array sum in assembly.** Write an assembly function `long sum_array(int* arr, size_t len)`. From C, create an array of 1000 elements, fill with values, call your function, and print the sum.

9. **Inline assembly.** Use GCC's inline assembly to execute `CPUID` instruction and print the CPU vendor string (from ebx:edx:ecx after `cpuid` with eax=0).

10. **Full project.** Build a program that:
    - Reads a file name from the command line using C's `fopen`/`fread`
    - Passes the file content to an assembly function that counts characters
    - Returns the count to C, which prints it
    - Challenge: make it work with files of any size

## 10. Self-check questions

- [ ] What does `global` do in assembly? What does `extern` do?
- [ ] Why do we use `main` instead of `_start` when calling C functions?
- [ ] What must you set in AL before calling `printf`? Why?
- [ ] What does the `-no-pie` flag do when linking assembly with GCC?
- [ ] What happens if you don't preserve callee-saved registers in an assembly function called from C?
- [ ] Does C mangle function names? Does C++?
- [ ] How do you compile a mixed .c + .asm project?
- [ ] What is the purpose of the `asm()` keyword in GCC?
- [ ] In the System V ABI, what registers are used for the first 6 integer arguments?
- [ ] When is it justified to write assembly instead of C?

## 11. Reflection: what you've learned

Congratulations. You've completed the 10-level Assembly track for Xodex.

Let's look back at what you've learned:

| Level | Topic | What you can do now |
|:-----:|-------|-------------------|
| 00 | How computers work | Understand CPU, memory, instructions |
| 01 | First program | Write, assemble, link, and run assembly |
| 02 | Registers and mov | Move data between registers |
| 03 | Arithmetic | Add, subtract, multiply, divide |
| 04 | Memory basics | Load from and store to memory |
| 05 | Addressing modes | Index arrays, structs, LEA |
| 06 | Conditional jumps | If/else, while, for loops |
| 07 | Stack and subroutines | Functions, call/ret, stack frames |
| 08 | Calling convention | System V ABI, arguments, preservation |
| 09 | Strings and REP | String instructions, memory ops |
| 10 | C + Assembly | Mixed-language projects, extern/global |

You now understand computer architecture at a fundamental level. Every `if`, `for`, and function call in C maps to the instructions you've written. When you write code in any language, you understand what the CPU actually does.

**What to do next:**
- Write a small game in assembly (snake, tetris — using syscalls directly)
- Read compiler output: `gcc -S myfile.c` to see how C compiles to assembly
- Explore SIMD (SSE/AVX) instructions for vectorized computation
- Study an open-source OS kernel's assembly startup code (like Linux's `arch/x86/boot/`)

Assembly is not the end — it's the foundation for truly understanding computing.
