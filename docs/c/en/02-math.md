# [02] Math & Operators
> **Track:** C Programming · **Level:** 02 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Variables store data, but the real power comes from manipulating that data. We need to add numbers, calculate percentages, compute square roots, and control how expressions are evaluated. Every program — from a calculator to a physics simulation — relies on mathematical operations.

## 2. Core concept (absolute zero explanation)

### What is an operator?

An **operator** is a symbol that tells the computer to perform a specific mathematical or logical operation. Just like the `+` sign on a calculator tells it to add, operators in C tell the computer to add, subtract, multiply, divide, and more.

```
Operand1 + Operand2  →  Result
   10    +    5      →    15
```

- **Operators** are the action symbols (`+`, `-`, `*`, `/`)
- **Operands** are the values being acted upon (like `10` and `5`)

### What is an expression?

An **expression** is any combination of variables, values, and operators that produces a value:

```c
10 + 5           // expression, evaluates to 15
x * 2            // expression, evaluates to twice x
(a + b) / c      // expression with multiple operators
```

## 3. Step-by-step breakdown

### Example 1: Basic arithmetic

```c
#include <stdio.h>

int main() {
    int a = 10;
    int b = 3;
    
    int sum  = a + b;   // addition:       10 + 3 = 13
    int diff = a - b;   // subtraction:     10 - 3 = 7
    int prod = a * b;   // multiplication:  10 * 3 = 30
    int quot = a / b;   // division:        10 / 3 = 3  (NOT 3.333!)
    int rem  = a % b;   // modulus:         10 % 3 = 1  (remainder)
    
    printf("a + b = %d\n", sum);
    printf("a - b = %d\n", diff);
    printf("a * b = %d\n", prod);
    printf("a / b = %d  (integer division truncates)\n", quot);
    printf("a %% b = %d  (remainder)\n", rem);
    
    return 0;
}
```

Output:
```
a + b = 13
a - b = 7
a * b = 30
a / b = 3  (integer division truncates)
a % b = 1  (remainder)
```

### Understanding integer division truncation

When you divide two integers, the result is an integer. The fractional part is **truncated** (cut off, not rounded):

```c
printf("%d\n", 5 / 2);   // 2  (not 2.5)
printf("%d\n", 10 / 3);  // 3  (not 3.333...)
printf("%d\n", 1 / 3);   // 0  (not 0.333...)
```

If you want a fractional result, at least one operand must be a floating-point type:

```c
printf("%f\n", 5 / 2);      // 2.000000  — still integer division!
printf("%f\n", 5 / 2.0);    // 2.500000  — 2.0 is a double
printf("%f\n", (double)5 / 2); // 2.500000 — typecast
```

### The modulus operator (%)

`%` gives the remainder after division:

```c
printf("%d\n", 10 % 3);   // 1  (10 / 3 = 3, remainder 1)
printf("%d\n", 15 % 5);   // 0  (15 / 5 = 3, remainder 0 — divisible)
printf("%d\n", 7 % 2);    // 1  (odd number check)
```

**Common uses for %:**
- Check if a number is even/odd: `n % 2 == 0` means even
- Keep a value within a range: `index % array_size` wraps around
- Extract digits: `123 % 10` gives 3 (last digit)

### Example 2: Operator precedence

Operators have a **precedence** (priority) order, just like in math class:

```c
#include <stdio.h>

int main() {
    int result;
    
    result = 5 + 3 * 2;       // multiplication first: 5 + 6 = 11
    printf("5 + 3 * 2 = %d\n", result);
    
    result = (5 + 3) * 2;     // parentheses override: 8 * 2 = 16
    printf("(5 + 3) * 2 = %d\n", result);
    
    result = 10 - 3 + 2;      // same precedence, left to right: 9
    printf("10 - 3 + 2 = %d\n", result);
    
    result = 10 - (3 + 2);    // parentheses: 10 - 5 = 5
    printf("10 - (3 + 2) = %d\n", result);
    
    return 0;
}
```

**C precedence rules (simplified, highest to lowest):**
1. `()` — parentheses
2. `++` `--` — increment/decrement (postfix)
3. `++` `--` `+` `-` `!` — unary operators
4. `*` `/` `%` — multiplicative
5. `+` `-` — additive
6. `=` `+=` `-=` etc. — assignment (lowest)

**Rule of thumb:** When in doubt, add parentheses. It makes your intention clear.

### Example 3: Compound assignment operators

These combine an operation with assignment:

```c
#include <stdio.h>

int main() {
    int x = 10;
    
    x += 5;     // same as: x = x + 5;   → x is now 15
    printf("x += 5:  %d\n", x);
    
    x -= 3;     // same as: x = x - 3;   → x is now 12
    printf("x -= 3:  %d\n", x);
    
    x *= 2;     // same as: x = x * 2;   → x is now 24
    printf("x *= 2:  %d\n", x);
    
    x /= 4;     // same as: x = x / 4;   → x is now 6
    printf("x /= 4:  %d\n", x);
    
    x %= 5;     // same as: x = x % 5;   → x is now 1
    printf("x %%= 5:  %d\n", x);
    
    return 0;
}
```

Every arithmetic operator has a compound form: `+=`, `-=`, `*=`, `/=`, `%=`.

### Example 4: Increment and decrement (++ and --)

These operators add 1 or subtract 1 from a variable. They come in two flavors.

```c
#include <stdio.h>

int main() {
    int x = 5;
    int y;
    
    // POSTFIX: use current value, THEN increment
    y = x++;
    printf("postfix: y = %d, x = %d\n", y, x);  // y = 5, x = 6
    
    x = 5;  // reset
    
    // PREFIX: increment FIRST, then use new value
    y = ++x;
    printf("prefix:  y = %d, x = %d\n", y, x);  // y = 6, x = 6
    
    // Same for decrement
    x = 5;
    y = x--;
    printf("postfix decrement: y = %d, x = %d\n", y, x);  // y = 5, x = 4
    
    x = 5;
    y = --x;
    printf("prefix decrement:  y = %d, x = %d\n", y, x);  // y = 4, x = 4
    
    return 0;
}
```

**Key difference:**
- `x++` — Use `x`, then add 1 to `x`
- `++x` — Add 1 to `x`, then use `x`

### Example 5: Type conversion (implicit and explicit)

**Implicit conversion (automatic):**

C automatically converts between types when mixing them in an expression:

```c
#include <stdio.h>

int main() {
    int i = 5;
    double d = 3.14;
    
    double result = i + d;  // i is promoted to double: 5.0 + 3.14 = 8.14
    printf("%f\n", result);
    
    // Integer division truncated to double
    double bad = 5 / 2;     // 5/2 = 2 (integer), then 2 → 2.0
    printf("5/2 = %f\n", bad);  // 2.000000 — probably not what you want!
    
    // Fix with explicit cast
    double good = (double)5 / 2;  // 5 → 5.0, then 5.0 / 2 = 2.5
    printf("(double)5/2 = %f\n", good);
    
    return 0;
}
```

**Explicit conversion (casting):**

You force a conversion with the cast operator: `(type)`:

```c
int a = 10, b = 3;
double result1 = (double)a / b;      // 10.0 / 3 = 3.333...
double result2 = a / (double)b;      // 10 / 3.0 = 3.333...
double result3 = (double)(a / b);    // (double)(3) = 3.0 — wrong place!
```

**Conversion rules when types differ:**
1. `int` + `double` → `int` promoted to `double`
2. `char` + `int` → `char` promoted to `int`
3. Smaller type + larger type → smaller promoted to larger

### Example 6: Math functions (sqrt, pow)

C provides mathematical functions in the **math library**.

```c
#include <stdio.h>
#include <math.h>     // Required for math functions

int main() {
    double x = 9.0;
    double y = 2.0;
    
    double root = sqrt(x);           // square root: √9 = 3.0
    double power = pow(x, y);        // x^y: 9^2 = 81.0
    double ceil_val = ceil(3.14);    // round up: 4.0
    double floor_val = floor(3.14);  // round down: 3.0
    double abs_val = fabs(-5.7);     // absolute value: 5.7
    
    printf("sqrt(9.0)       = %f\n", root);
    printf("pow(9.0, 2.0)   = %f\n", power);
    printf("ceil(3.14)      = %f\n", ceil_val);
    printf("floor(3.14)     = %f\n", floor_val);
    printf("fabs(-5.7)      = %f\n", abs_val);
    
    return 0;
}
```

**IMPORTANT:** You must link the math library explicitly when compiling:

```bash
gcc program.c -o program -lm
```

The `-lm` flag tells the linker to include the math library (`libm.so`). Without it, you get "undefined reference to `sqrt`" errors.

## 4. Common mistakes

### Integer division when you meant float
```c
double avg = (a + b + c) / 3;  // Integer division if a,b,c are ints!
double avg = (a + b + c) / 3.0;  // Correct
```

### Using % with floats
```c
float x = 5.5;
printf("%d", x % 2);   // Error: % doesn't work on floats!
```
`%` only works with integer types. Use `fmod()` from `math.h` for floats.

### Forgetting -lm with math functions
```c
gcc program.c             // Linker error: undefined reference to sqrt
gcc program.c -lm         // Correct
```

### postfix vs prefix confusion
```c
int x = 5;
printf("%d %d", x++, ++x);  // Undefined behavior! Don't modify and use twice
```
Never use `++` or `--` on the same variable more than once in a single expression.

### Precedence mistakes with assignment
```c
int x = 5;
if (x = 10) { ... }  // Assignment, not comparison! Always true (10 is truthy)
if (x == 10) { ... } // Correct comparison
```

## 5. Exercises

### Easy
1. Write a program that converts Celsius to Fahrenheit: `F = C * 9/5 + 32`
2. Write a program that calculates the area of a circle: `A = π * r²` (use `3.14159` or `M_PI`)
3. Test integer division: print the results of `7/3`, `7/3.0`, and `(double)7/3`.

### Medium
4. Write a program that takes an integer and prints its last digit (use `%`).
5. Write a program that swaps two integers using only `+` and `-` (no third variable).
6. Calculate the roots of a quadratic equation `ax² + bx + c = 0` using `sqrt`.

### Hard
7. Write a program that checks if a number is even or odd using the `%` operator.
8. Write a program that extracts and prints each digit of a 3-digit number (hint: `% 10` and `/ 10`).
9. Research and write a program demonstrating integer overflow — what happens when you add 1 to the maximum `int` value?

## 6. Self-check questions

1. What is `5 / 2` in C? Why?
2. What does the `%` operator do? Give two example uses.
3. What does `sizeof(5 / 2.0)` return? Why?
4. What is the difference between `x++` and `++x`?
5. What does `x += 5` mean?
6. What is operator precedence? What happens if you write `3 + 4 * 2`?
7. How do you force a division to produce a fractional result?
8. Why do you need `-lm` when compiling programs that use `sqrt` or `pow`?
9. What is the difference between implicit and explicit type conversion?
10. What happens when you use `%` on a `float`?

## 7. What's next

You can now perform calculations and manipulate numeric data. But programs need to make decisions based on conditions.

Next: **Level 03 — Control Flow**. You'll learn how to make decisions in your program using `if`, `else`, `switch`, and logical operators.
