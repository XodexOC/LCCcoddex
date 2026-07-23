# [07] Pointers Basics
> **Track:** C Programming · **Level:** 07 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Every variable in your program lives somewhere in the computer's memory. So far, you've worked with variables by name — you say `int x = 5;` and the compiler handles where `x` is stored.

But there are things you cannot do with variable names alone:
- **Modify a variable from inside a function** (pass-by-value copies the argument, so changes don't affect the caller)
- **Work with dynamically allocated memory** (you don't know the name — it was allocated at runtime)
- **Efficiently walk through arrays** (array indexing is convenient, but pointer arithmetic is sometimes faster)
- **Build complex data structures** (linked lists, trees, etc.)

**Pointers** are variables that hold **memory addresses** instead of values. They let you work with memory directly.

## 2. Core concept (absolute zero explanation)

### What is a pointer?

A **pointer** is a variable that stores the **memory address** of another variable (or of a block of memory).

Think of it like a house address:
- Your house (the variable) has an address on a street (memory address)
- You write that address on a piece of paper (the pointer)
- Someone can use that piece of paper to find your house (dereference the pointer)

```
Variable x:
  Name:  x
  Value: 42
  Address: 0x7ffd1234

Pointer p:
  Name:  p
  Value: 0x7ffd1234   ← this is x's address
  Address: 0x7ffd1238  ← p has its own address too!
```

### Two operators you need

**`&` (address-of operator)** — gets the memory address of a variable:

```c
int x = 42;
printf("%p\n", &x);  // prints something like 0x7ffd1234
```

**`*` (dereference operator)** — goes to the address stored in a pointer and accesses the value there:

```c
int x = 42;
int *p = &x;  // p stores the address of x
printf("%d\n", *p);  // prints 42 — goes to p's address and reads the value
```

## 3. Step-by-step breakdown

### Example 1: Declaring pointers and using & and *

```c
#include <stdio.h>

int main() {
    int x = 42;
    
    // Declare a pointer to an int. Read: "pointer to int"
    int *p;
    
    // Store the address of x in p
    p = &x;
    
    printf("Value of x:      %d\n", x);     // 42
    printf("Address of x:    %p\n", &x);    // e.g., 0x7ffd1234
    printf("Value of p:      %p\n", p);     // same address as &x
    printf("Address of p:    %p\n", &p);    // p lives at its own address
    printf("Dereference p:   %d\n", *p);    // 42 — value at the address p holds
    
    // Modify x through the pointer
    *p = 99;
    printf("x after *p = 99: %d\n", x);     // 99
    
    return 0;
}
```

**Declaration syntax:**
```c
int *p;   // p is a pointer to an int
char *c;  // c is a pointer to a char
double *d;// d is a pointer to a double
```

**Key insight:** `*` in a declaration and `*` in an expression mean different things:
- `int *p;` — declares `p` as a pointer (part of the type)
- `*p` — dereference: "get the value at the address stored in p"

### Example 2: NULL pointer

A pointer that doesn't point to anything valid should be set to `NULL`:

```c
#include <stdio.h>

int main() {
    int *p = NULL;  // Points to nothing
    
    // Always check for NULL before dereferencing
    if (p != NULL) {
        printf("%d\n", *p);  // This would crash if p is NULL
    } else {
        printf("Pointer is NULL — cannot dereference\n");
    }
    
    // Dereferencing NULL causes a crash (segmentation fault)
    // *p = 42;  // NEVER do this!
    
    return 0;
}
```

**Why NULL exists:**
- Uninitialized pointers contain garbage addresses
- Using a garbage address causes crashes or corrupts data
- NULL gives a safe default: "points to nothing"
- Always initialize pointers to NULL if you don't have a valid address yet

### Example 3: Pointers and functions — pass by pointer

C uses **pass by value**: functions receive copies of arguments. Pointers let you simulate **pass by reference**:

```c
#include <stdio.h>

// Pass by value — this DOESN'T work for swapping
void swap_bad(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
    // Effect: a and b are swapped locally, but the caller's variables are unchanged
}

// Pass by pointer — this WORKS
void swap_good(int *a, int *b) {
    int temp = *a;  // Read the value at address a
    *a = *b;        // Write to the address a
    *b = temp;      // Write to the address b
}

int main() {
    int x = 10, y = 20;
    
    printf("Before: x = %d, y = %d\n", x, y);
    
    swap_bad(x, y);   // Passes copies — no effect
    printf("After swap_bad: x = %d, y = %d\n", x, y);  // Still 10, 20
    
    swap_good(&x, &y);  // Passes addresses — works!
    printf("After swap_good: x = %d, y = %d\n", x, y); // 20, 10
    
    return 0;
}
```

**Why this works:**
- `swap_good` receives `&x` and `&y` — the addresses of x and y
- `*a = *b` means "take the value at address b and put it at address a"
- This modifies x and y directly, not copies

### Example 4: The "out parameter" pattern

Functions can "return" multiple values through pointer parameters:

```c
#include <stdio.h>

// "Return" both quotient and remainder through pointers
void divide(int dividend, int divisor, int *quotient, int *remainder) {
    *quotient = dividend / divisor;
    *remainder = dividend % divisor;
}

int main() {
    int q, r;
    
    divide(17, 5, &q, &r);
    
    printf("17 / 5 = %d remainder %d\n", q, r);
    
    // Another example: decompose seconds into hours, minutes, seconds
    int total_seconds = 3665;
    int h, m, s;
    
    h = total_seconds / 3600;
    m = (total_seconds % 3600) / 60;
    s = total_seconds % 60;
    
    printf("%d seconds = %d h %d m %d s\n", total_seconds, h, m, s);
    
    return 0;
}
```

### Example 5: Pointers and arrays

The name of an array **decays to** a pointer to its first element:

```c
#include <stdio.h>

int main() {
    int arr[5] = {10, 20, 30, 40, 50};
    
    // arr is the same as &arr[0]
    printf("arr:      %p\n", arr);     // address of first element
    printf("&arr[0]:  %p\n", &arr[0]); // same address
    printf("arr[0]:   %d\n", arr[0]);  // 10
    printf("*arr:     %d\n", *arr);    // 10 — dereferencing the array name
    
    // Access other elements using pointer arithmetic
    printf("*(arr+1): %d\n", *(arr+1)); // 20
    printf("*(arr+2): %d\n", *(arr+2)); // 30
    
    // arr[i] is exactly equivalent to *(arr + i)
    printf("arr[3] == *(arr+3): %d == %d\n", arr[3], *(arr+3));
    
    return 0;
}
```

**Key fact:** `arr[i]` is **defined** as `*(arr + i)` in C. They are identical.

**Important difference:** `sizeof(arr)` gives the full array size, but `sizeof(pointer)` gives just the pointer size:

```c
int arr[10];
int *p = arr;

printf("%zu\n", sizeof(arr));  // 40 (10 ints × 4 bytes)
printf("%zu\n", sizeof(p));    // 8 (pointer size on 64-bit system)
```

### Example 6: Pointer declaration syntax explained

Pointer declaration can be confusing. Here are the rules:

```c
int *p;     // p is a pointer to int
int* p;     // same thing, different style (type is "pointer to int")
int *p, q;  // p is a pointer to int, q is an int (NOT a pointer!)
int *p, *q; // both p and q are pointers to int
```

**Style debate:** Some write `int* p;` (pointer belongs to type), others write `int *p;` (pointer belongs to variable). Both are valid. The second form avoids confusion in declarations with multiple variables.

### Example 7: Pointer to pointer (introduction)

A pointer can point to another pointer:

```c
#include <stdio.h>

int main() {
    int x = 42;
    int *p = &x;     // p points to x
    int **pp = &p;   // pp points to p (which points to x)
    
    printf("x:          %d\n", x);     // 42
    printf("*p:         %d\n", *p);    // 42
    printf("**pp:       %d\n", **pp);  // 42
    
    // Changing x through pp
    **pp = 100;
    printf("x after **pp = 100: %d\n", x);  // 100
    
    return 0;
}
```

Think of it as levels of indirection:
- `x` — value
- `p` — address of `x`
- `pp` — address of `p`

### Example 8: void* pointer (introduction)

A `void*` is a generic pointer that can point to any type. It cannot be dereferenced directly — you must cast it first.

```c
#include <stdio.h>

int main() {
    int x = 42;
    double d = 3.14;
    
    void *ptr;
    
    ptr = &x;      // void* can hold any address
    printf("int value: %d\n", *(int*)ptr);  // Must cast before dereferencing
    
    ptr = &d;      // Now points to a double
    printf("double value: %f\n", *(double*)ptr);
    
    return 0;
}
```

`void*` is used extensively in C for generic functions like `malloc`, `qsort`, etc.

## 4. Common mistakes

### Dereferencing uninitialized pointer
```c
int *p;      // p contains garbage address
*p = 42;     // CRASH! Writing to a random memory location
```
Always initialize pointers: `int *p = NULL;` or `int *p = &some_variable;`.

### Forgetting & when passing to scanf
```c
int x;
scanf("%d", x);   // Wrong! Should be &x
scanf("%d", &x);  // Correct
```
(For strings/arrays, you DON'T need & because the array name is already a pointer.)

### Confusing * in declaration vs expression
```c
int *p = &x;   // Declaration: p is a pointer
*p = 42;       // Expression: dereference p, assign 42 to whatever p points to
```

### Returning a pointer to a local variable
```c
int* bad_function() {
    int x = 42;
    return &x;  // DANGER! x is destroyed when function returns
}
```

### Thinking *p is the pointer itself
When you see `*p`, it's the **dereferenced value**, not the pointer. The pointer is `p`.

## 5. Exercises

### Easy
1. Write a program that declares an `int`, a pointer to it, prints the variable's value using both the variable and the pointer.
2. Write a program that prints the address of an `int`, a `char`, and a `double` variable.
3. Demonstrate NULL by checking if a pointer is NULL before dereferencing.

### Medium
4. Write a function `void increment(int *x)` that increments the value pointed to by `x`.
5. Write a function `void get_min_max(int arr[], int size, int *min, int *max)` that finds both minimum and maximum.
6. Write a program that uses a pointer to iterate through an array and print all elements.

### Hard
7. Write a function `void circular_swap(int *a, int *b, int *c)` that rotates values: a→b, b→c, c→a.
8. Write a function `int* find_max(int arr[], int size)` that returns a pointer to the maximum element.
9. Write a program that demonstrates the equivalence of `arr[i]` and `*(arr + i)` using both forms.

## 6. Self-check questions

1. What is a pointer? What kind of value does it store?
2. What does the `&` operator do? What does the `*` operator do?
3. What is NULL and why is it important?
4. Why can't `swap(int a, int b)` actually swap two variables in the caller?
5. How is `arr[i]` defined in terms of pointers?
6. What does "array decay" mean when passing an array to a function?
7. What is the difference between `int *p` and `int* p`?
8. Why can't you return a pointer to a local variable from a function?
9. What is `void*` and why can't you dereference it directly?
10. What does `**pp` mean if `pp` is a pointer to a pointer?

## 7. What's next

You know what pointers are, how to use `&` and `*`, and how pointers relate to arrays. But pointers can do more: arithmetic, dynamic memory, function pointers, and more.

Next: **Level 08 — Pointers Deep**. You'll learn pointer arithmetic, differences between arrays and pointers, pointers to pointers, function pointers, and building dynamic arrays.
