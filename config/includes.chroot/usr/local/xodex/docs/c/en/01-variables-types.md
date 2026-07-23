# [01] Variables & Types
> **Track:** C Programming · **Level:** 01 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

In Level 00, we printed a fixed message. But programs need to work with changing data — a user's name, a bank balance, a temperature reading. We need a way to store information in the computer's memory and give it a name so we can use it later.

We also need to tell the computer what *kind* of data we're storing — is it a whole number? A letter? A number with decimals? Different kinds of data take up different amounts of memory and behave differently.

## 2. Core concept (absolute zero explanation)

### What is a variable?

A **variable** is a named box in the computer's memory that holds a value.

Imagine a row of mailbox slots. Each slot has a label (a number or name) and can hold one piece of mail. In programming, each variable has:
- A **name** — how you refer to it (like `age` or `temperature`)
- A **type** — what kind of data it holds (a number? a letter?)
- A **value** — the actual data stored in the box

```
Variable: age
Type: int
Memory: [  25  ]
         ^^^^^^
         4 bytes reserved
```

The name is `age`, the type is `int` (integer/whole number), and the value is `25`.

### What is a type?

A **type** tells the computer:
1. How much memory to set aside for this variable
2. What kind of operations you can do on it
3. How to interpret the bits in memory

### Why types matter

```c
int x = 65;      // stored as 00000000 01000001
char c = 'A';    // stored as 01000001
```

The bit pattern `01000001` can mean `65` (as an int) or `'A'` (as a character). The type tells the compiler which interpretation to use.

## 3. Step-by-step breakdown

### Example 1: Integer variables (int)

An `int` stores a whole number (positive, negative, or zero). On most modern systems, an `int` takes **4 bytes** (32 bits) of memory.

```c
#include <stdio.h>

int main() {
    int age;           // Declaration: create a box called "age"
    age = 25;          // Assignment: put 25 in the box
    
    int score = 100;   // Initialization: declare and assign in one step
    
    printf("Age: %d\n", age);
    printf("Score: %d\n", score);
    
    return 0;
}
```

Output:
```
Age: 25
Score: 100
```

**Declaration vs Initialization:**
- `int age;` — **Declaration**. Creates the variable but doesn't give it a value. The box contains whatever garbage was in that memory location — using it before assignment is dangerous.
- `int score = 100;` — **Initialization**. Creates the variable AND puts a value in it at the same time. Always prefer initialization over separate declaration+assignment.

**Memory size of int:**

```c
#include <stdio.h>

int main() {
    printf("int uses %zu bytes\n", sizeof(int));
    return 0;
}
```

On most systems, this prints `int uses 4 bytes`. A byte is 8 bits. Each bit is a 0 or 1. With 4 bytes = 32 bits, you can represent 2^32 different values.

**Range of int:**
- An `int` can hold values from approximately -2,147,483,648 to 2,147,483,647 (negative 2 billion to positive 2 billion).
- This is because 32 bits = 4,294,967,296 combinations, split roughly in half for positive and negative.

### Example 2: Character type (char)

A `char` stores a single character and takes **1 byte** (8 bits) of memory.

```c
#include <stdio.h>

int main() {
    char letter = 'A';     // Single quotes for characters
    char digit = '7';      // Character '7', NOT the number 7
    char symbol = '$';
    
    printf("letter: %c\n", letter);
    printf("digit: %c\n", digit);
    printf("symbol: %c\n", symbol);
    
    // A char is also a small integer
    printf("'A' as a number: %d\n", letter);   // prints 65
    printf("'a' as a number: %d\n", 'a');       // prints 97
    
    return 0;
}
```

Output:
```
letter: A
digit: 7
symbol: $
'A' as a number: 65
'a' as a number: 97
```

A `char` is technically a very small integer (0–255 for unsigned, -128 to 127 for signed). The mapping from numbers to characters follows the **ASCII** standard. 'A' is 65, 'B' is 66, 'a' is 97, '0' is 48.

### Example 3: Floating-point types (float and double)

Use these for numbers with decimal points (real numbers).

```c
#include <stdio.h>

int main() {
    float  price = 19.99f;       // 4 bytes, ~6-7 decimal digits precision
    double pi   = 3.1415926535; // 8 bytes, ~15-16 decimal digits precision
    
    printf("price: %f\n", price);    // %f for float
    printf("pi:    %lf\n", pi);      // %lf for double
    
    // Control decimal places
    printf("price: %.2f\n", price);  // 2 decimal places
    printf("pi:    %.10lf\n", pi);   // 10 decimal places
    
    // Size check
    printf("float size:  %zu bytes\n", sizeof(float));
    printf("double size: %zu bytes\n", sizeof(double));
    
    return 0;
}
```

Output:
```
price: 19.990000
pi:    3.141593
price: 19.99
pi:    3.1415926535
float size:  4 bytes
double size: 8 bytes
```

**Key differences:**
- `float` — 4 bytes, less precision, append `f` to the number literal
- `double` — 8 bytes, more precision, the default for decimal numbers in C
- Always prefer `double` unless memory is extremely tight

### Example 4: signed vs unsigned

By default, `int` and `char` are **signed** — they can hold negative and positive values. You can explicitly ask for **unsigned**, which only holds non-negative values but doubles the positive range.

```c
#include <stdio.h>

int main() {
    signed int   normal = -100;    // can be negative
    unsigned int positive = 100;   // cannot be negative
    
    // signed int range: -2 billion to +2 billion
    // unsigned int range: 0 to 4 billion
    
    // WARNING: mixing signed and unsigned can cause bugs
    unsigned int u = 5;
    int s = -10;
    
    if (u + s > 0) {
        printf("This might print unexpectedly!\n");
        // u + s wraps around to a huge positive number
    }
    
    return 0;
}
```

**When to use unsigned:**
- When negative values don't make sense (array indices, sizes, counts)
- When you need the extra positive range

### Example 5: The sizeof() operator

`sizeof` tells you how many bytes a type or variable uses. It's not a function — it's an **operator** built into the language.

```c
#include <stdio.h>

int main() {
    int x = 10;
    char c = 'A';
    double d = 3.14;
    
    printf("sizeof(int):    %zu bytes\n", sizeof(int));
    printf("sizeof(x):      %zu bytes\n", sizeof(x));     // variable name, no ()
    printf("sizeof(char):   %zu bytes\n", sizeof(char));
    printf("sizeof(double): %zu bytes\n", sizeof(double));
    printf("sizeof(float):  %zu bytes\n", sizeof(float));
    
    // Arrays
    int arr[20];
    printf("sizeof(arr):    %zu bytes\n", sizeof(arr));    // 20 * 4 = 80
    
    return 0;
}
```

`%zu` is the format specifier for `size_t` (the type returned by `sizeof`).

### Variable naming rules

C variable names must follow these rules:

1. **Allowed characters:** letters (`a-z`, `A-Z`), digits (`0-9`), and underscore (`_`)
2. **Cannot start with a digit:** `1name` is invalid, `name1` is valid
3. **Case-sensitive:** `age`, `Age`, and `AGE` are three different variables
4. **No keywords:** Can't use reserved words like `int`, `return`, `if`, `while`
5. **Underscore prefix usually reserved:** Names starting with `_` are often used by system libraries

**Conventions (not rules, but good practice):**
- Use descriptive names: `student_count` not `sc`
- Use `snake_case` (lowercase with underscores) — the C convention
- Avoid single-letter names except for loop counters (`i`, `j`, `k`)

Valid: `age`, `_count`, `total_score`, `studentName`, `var1`
Invalid: `1st`, `int`, `my-var`, `first name`

## 4. Common mistakes

### Using uninitialized variables
```c
int x;
printf("%d\n", x);  // Prints garbage value!
```
Always initialize variables before reading them.

### Using %d for a float
```c
float pi = 3.14;
printf("%d\n", pi);  // Wrong! Use %f
```
Using the wrong format specifier causes undefined behavior — it might print garbage or crash.

### Single vs double quotes confusion
```c
char c = "A";      // Wrong: double quotes make a string, not a char
char c = 'A';      // Correct: single quotes make a char
```

### Integer overflow
```c
unsigned char x = 255;
x = x + 1;         // Wraps around to 0, not 256!
```
Be aware of type ranges. Use larger types if you need bigger numbers.

### Assuming int size is always 4 bytes
On older or embedded systems, `int` might be 2 bytes (16 bits). Use `sizeof()` to check, or use fixed-width types from `<stdint.h>` (like `int32_t`) when you need exact sizes.

### Assigning float to int truncates
```c
int x = 3.99;      // x becomes 3, the .99 is truncated
```

## 5. Exercises

### Easy
1. Declare an `int` variable called `year`, initialize it to the current year, and print it.
2. Declare a `char` variable holding your favorite letter, print it as a character and as a number.
3. Print the `sizeof` of `short`, `long`, and `long long` on your system.

### Medium
4. Create a program with variables for your name (as a single char initial), age (int), height (double), and grade (char). Print them all with proper format specifiers.
5. Write a program that demonstrates what happens when you add 1 to the maximum value of an `unsigned char` (255). Print the result.
6. Declare an `int` without initializing it. Print it three times. Is the output consistent? Why or why not?

### Hard
7. Research the ASCII table. Print characters for the values 65–90 (uppercase alphabet) using `%c` in a loop.
8. Write a program that checks the size of `int` on your system WITHOUT using `sizeof` (hint: use pointer arithmetic or `limits.h`).

## 6. Self-check questions

1. What is the difference between declaration and initialization?
2. How many bytes does an `int` use on most modern systems? What range does that give?
3. What is the difference between `float` and `double`?
4. Why does `sizeof` use `%zu` to print?
5. What is ASCII and how does it relate to `char`?
6. What happens when you assign 3.99 to an `int` variable?
7. What happens if you print a `float` with `%d`?
8. What is the difference between `char c = 'A'` and `char c = "A"`?
9. What are the variable naming rules in C?
10. What is the difference between `signed int` and `unsigned int`?

## 7. What's next

You now know how to store and print different kinds of data. But storing data is only useful if you can manipulate it.

Next: **Level 02 — Math & Operators**. You'll learn how to perform arithmetic, use compound assignments, understand precedence, and call math functions like `sqrt` and `pow`.
