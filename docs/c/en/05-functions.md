# [05] Functions
> **Track:** C Programming · **Level:** 05 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

As programs grow, putting all code in `main` becomes unmanageable. If you need to calculate an average in ten different places, you'd copy the same code ten times. If you find a bug in that calculation, you'd need to fix it in all ten places.

We need a way to:
- **Reuse** code without copying it
- **Organize** code into named, logical blocks
- **Isolate** complex logic into separate, testable pieces
- **Abstract** away details so the caller doesn't need to know how something works

## 2. Core concept (absolute zero explanation)

### What is a function?

A **function** is a named block of code that performs a specific task. You've already been using one: `main`.

Think of a function like a blender:
- You put ingredients in (the **inputs/arguments**)
- You press a button (the **call/invocation**)
- You get a smoothie out (the **return value**)

```
Inputs → [ FUNCTION ] → Output
```

A function **takes inputs**, **does something**, and **returns a result**.

### Why use functions?

```c
// WITHOUT functions — repeated code everywhere
int a = 5, b = 10;
int sum1 = a + b;
printf("Sum 1: %d\n", sum1);

int c = 20, d = 30;
int sum2 = c + d;
printf("Sum 2: %d\n", sum2);

// WITH functions — write once, use many times
int add(int x, int y) {
    return x + y;
}

printf("Sum 1: %d\n", add(5, 10));
printf("Sum 2: %d\n", add(20, 30));
```

## 3. Step-by-step breakdown

### Example 1: Your first function

```c
#include <stdio.h>

// Function DEFINITION
void greet() {
    printf("Hello! Welcome to the program.\n");
}

int main() {
    // Function CALL
    greet();
    greet();  // Can call multiple times
    return 0;
}
```

Output:
```
Hello! Welcome to the program.
Hello! Welcome to the program.
```

**Breaking it down:**
- `void` — the **return type**. `void` means this function doesn't return a value.
- `greet` — the **name** of the function.
- `()` — the **parameter list**. Empty means it takes no arguments.
- `{ ... }` — the **body** of the function (what it does).
- `greet();` — the **function call**. This tells the computer to execute `greet`'s code.

### Example 2: Using parameters (inputs)

Parameters let you pass data into a function:

```c
#include <stdio.h>

// Function with one parameter
void print_square(int x) {
    printf("%d squared is %d\n", x, x * x);
}

// Function with multiple parameters
void print_rectangle(int width, int height) {
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            printf("*");
        }
        printf("\n");
    }
}

int main() {
    print_square(7);            // 7 is the argument
    print_square(12);
    
    printf("\n");
    print_rectangle(5, 3);      // width=5, height=3
    
    return 0;
}
```

Output:
```
7 squared is 49
12 squared is 144

*****
*****
*****
```

**Terminology:**
- **Parameter** — the variable listed in the function definition (`int x`)
- **Argument** — the actual value passed when calling (`7`)

### Example 3: Return values

Functions can send a value back to the caller using `return`:

```c
#include <stdio.h>

int add(int a, int b) {
    int sum = a + b;
    return sum;       // send the result back
}

int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

int main() {
    int result = add(10, 20);
    printf("10 + 20 = %d\n", result);
    
    printf("Max of 15 and 8 is %d\n", max(15, 8));
    
    // Functions can be used in expressions
    int triple = add(add(1, 2), 3);  // (1+2)+3 = 6
    printf("Triple: %d\n", triple);
    
    return 0;
}
```

**Key points about `return`:**
1. `return` immediately exits the function.
2. The value after `return` is sent back to the caller.
3. The return type in the function signature must match the returned value.
4. A `void` function can use `return;` (with no value) to exit early, or omit it entirely.

### Example 4: Function declaration vs definition

C requires functions to be **declared** before they are called. A **declaration** (also called a **prototype**) tells the compiler: "This function exists, here's its signature — the full definition comes later."

```c
#include <stdio.h>

// DECLARATION (prototype)
int multiply(int a, int b);
// Or: int multiply(int, int);  — parameter names optional in declaration

int main() {
    int product = multiply(6, 7);  // Works because of the declaration
    printf("6 * 7 = %d\n", product);
    return 0;
}

// DEFINITION
int multiply(int a, int b) {
    return a * b;
}
```

Without the declaration, the compiler would complain: "implicit declaration of function 'multiply'" (or an error in C99+).

**Why this matters:**
The compiler reads your file top-to-bottom. When it reaches the call to `multiply` in `main`, it needs to know:
1. That `multiply` exists
2. What parameters it takes
3. What it returns

The declaration provides this info. The definition (body) can be anywhere — even in another file.

### Example 5: Local variables and scope

Variables declared inside a function are **local** to that function:

```c
#include <stdio.h>

void func_a() {
    int x = 10;  // x is local to func_a
    printf("func_a: x = %d\n", x);
}

void func_b() {
    int x = 20;  // This is a DIFFERENT x, local to func_b
    printf("func_b: x = %d\n", x);
}

int main() {
    func_a();  // prints: func_a: x = 10
    func_b();  // prints: func_b: x = 20
    
    // printf("%d\n", x);  // ERROR: x is not defined here
    
    return 0;
}
```

**Scope rules:**
1. Variables defined inside `{ }` are local to that block.
2. A variable is only accessible from its point of declaration to the closing `}`.
3. Each function call creates **new copies** of its local variables.

```c
int global = 100;  // Global variable — accessible everywhere (avoid when possible)

void demo() {
    int local = 5;  // Local to demo
    {
        int inner = 10;  // Local to this block
        printf("inner: %d\n", inner);
    }
    // printf("%d\n", inner);  // ERROR: inner no longer exists
    printf("global: %d\n", global);  // OK
}

int main() {
    int local = 99;  // Different from demo's local
    demo();
    // printf("%d\n", local);  // This is main's local = 99
    return 0;
}
```

### Example 6: The call stack (conceptual)

The **call stack** is the mechanism that keeps track of function calls:

```c
#include <stdio.h>

void func_c() {
    printf("Inside C\n");
}

void func_b() {
    printf("Inside B, calling C...\n");
    func_c();
    printf("Back in B\n");
}

void func_a() {
    printf("Inside A, calling B...\n");
    func_b();
    printf("Back in A\n");
}

int main() {
    printf("Starting...\n");
    func_a();
    printf("Done!\n");
    return 0;
}
```

Output:
```
Starting...
Inside A, calling B...
Inside B, calling C...
Inside C
Back in B
Back in A
Done!
```

**What happens in memory:**
```
    main()                 main()                 main()                 main()
                           func_a()               func_a()               func_a()
                                                  func_b()               func_b()
                                                                         func_c()
Time → calling...         A starts...            B starts...            C starts...
                            
    main()                 main()                 main()
    func_a()               func_a()
    func_b()               func_b()
    func_c()    →          func_b()    →          func_a()    →          main()
C returns...    B continues...    B returns...    A continues...    A returns...
```

Each function call gets a **stack frame** — a region of memory holding its local variables and where to return to. When a function returns, its frame is reclaimed.

### Example 7: Recursion (simple example)

**Recursion** is when a function calls itself.

```c
#include <stdio.h>

// Factorial: n! = n * (n-1) * (n-2) * ... * 1
// 5! = 5 * 4 * 3 * 2 * 1 = 120

int factorial(int n) {
    // Base case: stop recursing
    if (n <= 1) {
        return 1;
    }
    
    // Recursive case: call ourselves with a smaller value
    return n * factorial(n - 1);
}

int main() {
    printf("5! = %d\n", factorial(5));   // 120
    printf("0! = %d\n", factorial(0));   // 1 (by definition)
    printf("10! = %d\n", factorial(10)); // 3628800
    
    return 0;
}
```

**How recursion works for factorial(5):**
```
factorial(5) = 5 * factorial(4)
                    = 5 * (4 * factorial(3))
                        = 5 * (4 * (3 * factorial(2)))
                            = 5 * (4 * (3 * (2 * factorial(1))))
                                = 5 * (4 * (3 * (2 * 1)))
                            = 5 * (4 * (3 * 2))
                        = 5 * (4 * 6)
                    = 5 * 24
                = 120
```

Every recursive function needs:
1. **Base case** — when to stop recursing (`n <= 1`)
2. **Recursive case** — calling itself with a simpler problem (`n-1`)

### Example 8: Forward declaration

You can use forward declarations to organize functions in any order:

```c
#include <stdio.h>

// Forward declarations
void print_welcome(void);
int get_number(void);
void print_result(int n);

int main() {
    print_welcome();
    int num = get_number();
    print_result(num);
    return 0;
}

// Definitions can be in any order now
void print_welcome(void) {
    printf("Welcome to the number program!\n");
}

int get_number(void) {
    int n;
    printf("Enter a number: ");
    scanf("%d", &n);
    return n;
}

void print_result(int n) {
    printf("You entered: %d\n", n);
}
```

**Using `void` in parameter list:**
- `int get_number(void)` — explicitly says "no parameters"
- `int get_number()` — in C (not C++), an empty parameter list means "parameters unknown" — avoid this

## 4. Common mistakes

### Missing function declaration
```c
int main() {
    greet();  // Error: implicit declaration
    return 0;
}
void greet() { printf("Hi"); }
```
Fix: put `greet` above `main`, or add a prototype.

### Forgetting return value
```c
int add(int a, int b) {
    // No return! Undefined behavior — returns garbage
}
```

### Returning pointer to local variable
```c
int* get_number() {
    int x = 42;
    return &x;  // DANGER: x is destroyed when function returns!
}
```

### Too many parameters (code smell)
Try to keep parameters to 4 or fewer. Use a struct for many related values.

### Confusing parameters and arguments
```c
void func(int x) { ... }  // x is a PARAMETER
func(5);                   // 5 is an ARGUMENT
```

### Recursion without base case (stack overflow)
```c
void infinite() {
    infinite();  // No base case → runs until stack memory runs out
}
```

## 5. Exercises

### Easy
1. Write a function `void print_stars(int n)` that prints `n` stars.
2. Write a function `int square(int x)` that returns the square of its input.
3. Write a function `int is_even(int n)` that returns 1 if even, 0 if odd.

### Medium
4. Write a function `int max_of_three(int a, int b, int c)` that returns the largest of three numbers.
5. Write a function `double celsius_to_fahrenheit(double c)` and test it.
6. Write a function `int count_digits(int n)` that returns the number of digits in a positive integer.
7. Write a program with a function `int power(int base, int exp)` that computes base^exp (without using `pow`).

### Hard
8. Write a recursive function `int fibonacci(int n)` that returns the nth Fibonacci number.
9. Write a function `int is_prime(int n)` that returns 1 if prime, 0 otherwise.
10. Write a recursive function `void print_binary(int n)` that prints the binary representation of a number.

## 6. Self-check questions

1. What is the difference between a function declaration and a function definition?
2. What does `void` mean in a function signature?
3. What is the difference between a parameter and an argument?
4. What happens on the call stack when a function calls another function?
5. What is variable scope? When does a local variable stop existing?
6. What is recursion? What two parts must every recursive function have?
7. Why do you need to declare a function before calling it?
8. What happens if you forget `return` in a non-void function?
9. What is a forward declaration, and why is it useful?
10. Can a function call itself? Is that always allowed?

## 7. What's next

Functions let you organize and reuse code. But so far, each function works with single values. What if you need to work with many values at once — a list of test scores, a string of text, or a grid of pixels?

Next: **Level 06 — Arrays & Strings**. You'll learn how to store and manipulate collections of data, and how C handles text.
