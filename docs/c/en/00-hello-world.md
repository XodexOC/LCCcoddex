# [00] Hello World & Toolchain
> **Track:** C Programming · **Level:** 00 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

You have an idea. You want to tell the computer to do something — print text to the screen, add two numbers, or control a robot. The computer only understands machine code (billions of 1s and 0s). Nobody writes machine code by hand. We need a way to write instructions in a language humans can read, then translate those instructions into something the computer can run.

C is that human-readable language. This lesson teaches you how to write your first C program, understand every piece of it, and turn it into a running program.

## 2. Core concept (absolute zero explanation)

### What is a program?

A **program** is a list of instructions that tells the computer what to do. Think of it like a recipe:

```
Recipe for pancakes:
1. Mix flour and eggs
2. Add milk
3. Cook on pan
4. Serve
```

A computer program is the same idea but written in a language the computer can eventually understand.

### What is an algorithm?

An **algorithm** is the step-by-step plan for solving a problem — before you write any code. The recipe above is an algorithm. In programming, you first figure out the algorithm, then you write it in a programming language.

Example algorithm: "Count from 1 to 10 and print each number"
```
1. Start with number 1
2. Print the number
3. Add 1 to the number
4. If number <= 10, go back to step 2
5. Stop
```

### What is a compiler?

A **compiler** is a program that translates human-readable source code (C) into machine code (1s and 0s). You feed it a `.c` file, and it produces an executable file the computer can run.

Think of it like a translator: you speak English, the computer speaks machine code. The compiler translates between them.

### What is gcc?

**GCC** stands for GNU Compiler Collection. It is the most popular C compiler on Linux. When you run `gcc hello.c`, it reads your C source file and produces an executable program.

### What is a source file?

A **source file** is a plain text file containing C code. By convention, C source files end with `.c` (like `hello.c`). This tells the compiler, "This file contains C code."

## 3. Step-by-step breakdown

### Example 1: Your first program

Type this into a file called `hello.c`:

```c
#include <stdio.h>

int main() {
    printf("Hello, world!\n");
    return 0;
}
```

Every single character matters. Let's explain each piece.

### Breaking down every character

**Line 1: `#include <stdio.h>`**

- `#` — This tells the preprocessor (the first stage of compilation) to do something *before* compiling. Anything starting with `#` is a preprocessor directive.
- `include` — Means "insert the contents of another file here."
- `stdio.h` — A **header file** that comes with C. The name stands for **ST**an**D**ard **I**nput **O**utput. It contains information about functions like `printf`.
- `< >` — Angle brackets tell the compiler to look for this file in the system's standard location (usually `/usr/include`).
- Together, `#include <stdio.h>` means: "Before compiling, grab the standard input/output header file so we can use functions like `printf`."

**Line 3: `int main() {`**

- `int` — Short for **integer**. This is the type of value the function will return to the operating system when it finishes.
- `main` — The **entry point** of every C program. When you run your program, the operating system looks for a function called `main` and starts executing there. Every C program *must* have a `main` function.
- `()` — These parentheses mean `main` is a **function**. The empty space inside means it takes no arguments (no inputs).
- `{` — Opens the **body** of the function. All the instructions that `main` should execute go between `{` and `}`.

**Line 4: `    printf("Hello, world!\n");`**

- `printf` — A **function** (defined in `stdio.h`) that prints text to the screen.
- `("Hello, world!\n")` — The **argument** we pass to `printf`. This is what gets printed.
- `"Hello, world!"` — A **string literal** (text enclosed in double quotes).
- `\n` — A special **escape sequence** that means **newline**. It moves the cursor to the next line after printing.
- `;` — The **semicolon** ends a statement in C. Think of it like a period at the end of a sentence. Almost every line of C code ends with `;`.

**Line 5: `    return 0;`**

- `return` — Exit the function and send a value back to whoever called it (here, the operating system).
- `0` — A **return code** of 0 means "success." The operating system checks this value to know if your program ran correctly. Any non-zero value usually means something went wrong.
- `;` — Ends the statement.

**Line 6: `}`**

- Closes the body of `main`.

### Why return 0?

When your program finishes, the operating system checks the return value. By convention:
- `return 0;` means "everything worked fine."
- `return 1;` or any non-zero value means "something went wrong."

You can check the return code in the shell:
```bash
./hello
echo $?    # prints the return code of the last program
```

### Example 2: Compiling and running

Open a terminal and navigate to the folder containing `hello.c`:

```bash
gcc hello.c -o hello
```

- `gcc` — Invoke the C compiler.
- `hello.c` — The source file to compile.
- `-o hello` — Short for "output." Name the executable `hello` instead of the default `a.out`.

Now run it:

```bash
./hello
```

The `./` means "look in the current directory." You should see:

```
Hello, world!
```

### Example 3: The four stages of compilation

When you run `gcc hello.c`, four separate stages happen:

**Stage 1: Preprocessing**

The preprocessor handles `#include`, `#define`, and other `#` directives. It literally inserts the contents of `stdio.h` into your file. You can see the preprocessed output:

```bash
gcc -E hello.c
```

This prints the expanded source to the screen. You'll see hundreds of lines — that's `stdio.h` being inserted.

**Stage 2: Compilation**

The compiler translates the preprocessed C code into **assembly language** — a low-level human-readable representation specific to your CPU. Assembly looks like this:

```asm
movl    $0, %eax
```

You can see the assembly output:

```bash
gcc -S hello.c
```

This creates `hello.s` containing assembly code.

**Stage 3: Assembly**

The **assembler** (`as`) converts assembly code into **machine code** (1s and 0s) and stores it in an **object file** (`.o`):

```bash
gcc -c hello.c
```

This creates `hello.o` — a binary file but not yet a complete executable.

**Stage 4: Linking**

The **linker** (`ld`) combines your object file with necessary system files (like the code for `printf`) to produce a final executable. This is why you need `#include <stdio.h>` — the header tells the compiler about `printf`, and the linker provides the actual code for it.

All four stages in one command:

```bash
gcc hello.c -o hello
```

### Example 4: Using the default output name

If you don't use `-o`, gcc creates a file called `a.out`:

```bash
gcc hello.c
./a.out
```

The name `a.out` is historical — it originally stood for "assembler output." Always use `-o` to give meaningful names.

### Example 5: A program with comments

Comments are notes for humans that the compiler ignores:

```c
#include <stdio.h>

/* This is a multi-line comment.
   The compiler ignores everything inside. */

int main() {
    // This is a single-line comment (C99 style)
    printf("Hello, world!\n");  // Comments can go after code
    return 0;
}
```

- `/* ... */` — Multi-line comment.
- `// ...` — Single-line comment (added in C99).

## 4. Common mistakes

### Missing semicolon
```c
printf("Hello")
return 0;
```
Error: `expected ';' before 'return'`. Always end statements with `;`.

### Wrong case
```c
Printf("Hello");   // Wrong - C is case-sensitive
printf("Hello");   // Correct
```

### Missing #include
```c
int main() {
    printf("Hello");  // Warning: implicit declaration
    return 0;
}
```
Without `#include <stdio.h>`, the compiler doesn't know what `printf` is. It may still work with a warning, but always include the proper header.

### Misspelling main
```c
int mian() { ... }   // Wrong
int main() { ... }   // Correct
```
The linker will complain it cannot find `main` — the entry point.

### Forgetting \n
```c
printf("Hello");
printf("World");
```
Output: `HelloWorld` (all on one line). Add `\n` for newlines.

## 5. Exercises

### Easy
1. Write a program that prints your name.
2. Write a program that prints your name on one line and your age on the next.
3. Write a program that prints a smiley face using characters like `:)`.

### Medium
4. Modify the `printf` line to print multiple lines using only one `printf` statement and `\n`.
5. Write a program that prints a simple ASCII art picture (like a house or a tree) using multiple `printf` calls.

### Hard
6. Write a program that prints "Hello" on the first line, "World" on the second, and "!" on the third using a single `printf`.
7. Find out what happens if you omit `return 0;` — does the program still compile? What does `echo $?` show?

## 6. Self-check questions

1. What does `#include <stdio.h>` do?
2. What is the purpose of `main` in a C program?
3. What does `\n` mean?
4. Why does every statement end with `;`?
5. Why do we use `return 0;`?
6. What are the four stages of compilation?
7. What is the difference between a source file (`.c`) and an executable?
8. What happens if you forget `#include <stdio.h>`?
9. What does `-o` do in the `gcc` command?
10. What does `./` mean when running a program?

## 7. What's next

You can now write, compile, and run a C program. You understand every character in the "Hello, world!" program and the toolchain that turns source code into a running executable.

Next up: **Level 01 — Variables & Types**. You'll learn how to store and work with data: numbers, characters, and the boxes that hold them.
