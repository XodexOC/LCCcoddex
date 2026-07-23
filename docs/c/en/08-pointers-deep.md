# [08] Pointers Deep
> **Track:** C Programming · **Level:** 08 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

Basic pointers let you store addresses and pass them to functions. But pointers are much more powerful. You can:
- Do arithmetic on pointers to navigate memory efficiently
- Build and traverse dynamic data structures (linked lists, trees)
- Store and call functions through pointers (callbacks)
- Work with generic (type-agnostic) memory using `void*`
- Create arrays whose size is determined at runtime

This level removes the training wheels and shows you the full power of pointers.

## 2. Core concept (absolute zero explanation)

### Pointer arithmetic

When you add 1 to a pointer, you don't add 1 byte — you add the **size of the pointed-to type**:

```c
int *p;      // int is 4 bytes
p + 1;       // Advances by 4 bytes in memory

char *q;     // char is 1 byte
q + 1;       // Advances by 1 byte
```

```
Memory: | byte | byte | byte | byte | byte | byte | byte | byte |
         ^-- int *p points here
                  ^-- p + 1 points here (4 bytes forward)
```

This is why arrays work the way they do: `arr[i]` is `*(arr + i)`, and adding `i` to the pointer automatically skips `i * sizeof(element)` bytes.

### Arrays vs pointers — the difference

Arrays and pointers are **not the same**, though they're often confused:

```c
int arr[5];   // arr is an array: 5 ints of memory
int *p;       // p is a pointer: 8 bytes holding an address

// Array: memory is allocated HERE
// Pointer: memory is allocated elsewhere; p just stores an address

sizeof(arr);  // 20 (5 * 4 bytes)
sizeof(p);    // 8 (the pointer itself)

arr = p;      // ERROR! Cannot reassign an array name
p = arr;      // OK! p now points to arr's first element
```

**Summary:** An array name is a fixed address (not a variable). A pointer is a variable that can point to different addresses.

## 3. Step-by-step breakdown

### Example 1: Pointer arithmetic in detail

```c
#include <stdio.h>

int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int *p = arr;  // p points to arr[0]
    
    printf("p        = %p\n", p);
    printf("p + 1    = %p  (advances by %zu bytes)\n", p + 1, sizeof(int));
    printf("p + 2    = %p\n", p + 2);
    
    printf("\nAccessing array elements:\n");
    printf("arr[0] = %d,  *p       = %d\n", arr[0], *p);
    printf("arr[1] = %d,  *(p+1)   = %d\n", arr[1], *(p+1));
    printf("arr[2] = %d,  *(p+2)   = %d\n", arr[2], *(p+2));
    
    // Traverse array with pointer
    printf("\nTraversing with pointer:\n");
    for (int *q = arr; q < arr + 5; q++) {
        printf("%d ", *q);
    }
    printf("\n");
    
    // Pointer subtraction: number of elements between two pointers
    int *start = &arr[1];  // points to 20
    int *end   = &arr[4];  // points to 50
    printf("\nElements between arr[1] and arr[4]: %td\n", end - start);  // 3
    
    return 0;
}
```

**Pointer arithmetic rules:**
- `p + n` → advances `n * sizeof(*p)` bytes
- `p - n` → retreats `n * sizeof(*p)` bytes
- `p1 - p2` → number of elements between them (signed)
- `p++`, `p--` → move to next/previous element
- Comparison: `p < q`, `p == q`, `p > q` compare positions in memory

### Example 2: Pointers to pointers (depth)

```c
#include <stdio.h>

void set_to_zero(int **pp) {
    // pp is a pointer to a pointer to int
    // *pp gives us the original pointer
    // **pp gives us the original int
    
    // Allocate memory and make the original pointer point to it
    *pp = malloc(sizeof(int));
    **pp = 0;
}

int main() {
    int *ptr = NULL;
    
    set_to_zero(&ptr);  // Pass the address of our pointer
    
    if (ptr != NULL) {
        printf("Value: %d\n", *ptr);  // 0
        free(ptr);
    }
    
    // Practical use: array of strings
    char *fruits[] = {"apple", "banana", "cherry"};
    // fruits is an array of pointers (each is a char*)
    // fruits[0] is a pointer to "apple"
    // fruits[0][0] is 'a'
    
    for (int i = 0; i < 3; i++) {
        printf("%s\n", fruits[i]);
    }
    
    return 0;
}
```

**Multi-level indirection:**
```c
int x = 42;
int *p = &x;    // one level: points to int
int **pp = &p;  // two levels: points to pointer to int
int ***ppp = &pp; // three levels: points to pointer to pointer to int

***ppp = 100;   // changes x to 100
```

### Example 3: void* pointer (generic pointer)

`void*` can point to anything, but you must cast before dereferencing:

```c
#include <stdio.h>

// Generic function: prints any value given its size
void print_bytes(void *data, size_t size) {
    unsigned char *bytes = (unsigned char*)data;
    
    for (size_t i = 0; i < size; i++) {
        printf("%02x ", bytes[i]);
    }
    printf("\n");
}

int main() {
    int x = 123456;
    double d = 3.14159;
    char c = 'A';
    
    printf("int bytes:    ");
    print_bytes(&x, sizeof(x));
    
    printf("double bytes: ");
    print_bytes(&d, sizeof(d));
    
    printf("char bytes:   ");
    print_bytes(&c, sizeof(c));
    
    return 0;
}
```

**Common uses of void*:**
- Generic data structures (like `qsort` and `bsearch`)
- Raw memory manipulation (`memcpy`, `memset`)
- Opaque types (hide implementation details)
- Callback data passing

### Example 4: Function pointers

A function pointer stores the address of a function:

```c
#include <stdio.h>

// Some arithmetic functions
int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }
int multiply(int a, int b) { return a * b; }
int divide(int a, int b) { return b != 0 ? a / b : 0; }

int main() {
    // Declare a function pointer: pointer to a function that takes two ints and returns int
    int (*operation)(int, int);
    
    // Point it to different functions
    operation = add;
    printf("add(10, 5):      %d\n", operation(10, 5));
    
    operation = subtract;
    printf("subtract(10, 5): %d\n", operation(10, 5));
    
    operation = multiply;
    printf("multiply(10, 5): %d\n", operation(10, 5));
    
    // Array of function pointers
    int (*ops[])(int, int) = {add, subtract, multiply, divide};
    char *names[] = {"add", "subtract", "multiply", "divide"};
    
    printf("\nOperation table for (10, 5):\n");
    for (int i = 0; i < 4; i++) {
        printf("%s: %d\n", names[i], ops[i](10, 5));
    }
    
    return 0;
}
```

**Declaration syntax breakdown:**
```c
int (*operation)(int, int);
// ^   ^            ^     ^
// |   |            |     └── parameter types
// |   └────────────└──────── pointer name
// └── return type
```

Without the parentheses: `int *operation(int, int)` — this is a function that returns `int*`, NOT a function pointer!

### Example 5: Dynamic arrays using malloc + pointer

Pointers are essential for dynamic memory (memory allocated at runtime):

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    
    printf("How many numbers? ");
    scanf("%d", &n);
    
    // Allocate an array of n ints on the heap
    int *arr = malloc(n * sizeof(int));
    
    if (arr == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }
    
    // Use it like a regular array
    for (int i = 0; i < n; i++) {
        arr[i] = i * i;
    }
    
    printf("Squares:\n");
    for (int i = 0; i < n; i++) {
        printf("%d: %d\n", i, arr[i]);
    }
    
    // Free the memory when done
    free(arr);
    
    return 0;
}
```

**Key difference from static arrays:**
- Static: `int arr[10];` — fixed size, stack-allocated, automatically freed
- Dynamic: `int *arr = malloc(n * sizeof(int));` — runtime size, heap-allocated, must be manually freed

### Example 6: const and pointers

`const` with pointers has subtle but important rules:

```c
#include <stdio.h>

int main() {
    int x = 10;
    int y = 20;
    
    // 1. Pointer to const int (can't modify what it points TO)
    const int *p1 = &x;
    // *p1 = 20;  // ERROR: can't modify through p1
    p1 = &y;       // OK: can change what p1 points to
    
    // 2. Const pointer to int (can't change the pointer itself)
    int *const p2 = &x;
    *p2 = 30;      // OK: can modify through p2
    // p2 = &y;    // ERROR: p2 is const, can't reassign
    
    // 3. Const pointer to const int (neither can change)
    const int *const p3 = &x;
    // *p3 = 40;   // ERROR
    // p3 = &y;    // ERROR
    
    // Read declarations from right to left:
    const int *p;          // p is a pointer to const int
    int *const p;          // p is a const pointer to int
    const int *const p;    // p is a const pointer to const int
    
    return 0;
}
```

**Rule of thumb:** Read from right to left. `const` to the left of `*` means the data is const. `const` to the right of `*` means the pointer is const.

## 4. Common mistakes

### Pointer arithmetic on void*
```c
void *p = malloc(10);
p++;  // ERROR: can't do arithmetic on void* (unknown size)
```
Cast to `char*` first if you need byte-level arithmetic.

### Confusing array and pointer sizeof
```c
int arr[10];
int *p = arr;
sizeof(arr);  // 40
sizeof(p);    // 8
```

### Function pointer syntax
```c
int *func();           // function returning int*
int (*func)();         // pointer to function returning int
int (*func)(int, int); // pointer to function taking two ints, returning int
```

### Dereferencing a function pointer wrong
```c
int (*fp)(int, int) = add;
fp(3, 4);      // OK, implicit dereference
(*fp)(3, 4);   // Also OK, explicit dereference
```

### Forgetting parentheses in function pointer declaration
```c
int *fp(int, int);  // This is a FUNCTION declaration, not a pointer!
```

## 5. Exercises

### Easy
1. Write a program that uses pointer arithmetic to print every byte of an `int` variable as hexadecimal.
2. Create a pointer to a pointer, use it to modify the original value.
3. Write a program that demonstrates that `arr[i]` is identical to `*(arr + i)`.

### Medium
4. Write a generic `swap` function using `void*` that can swap any two values of equal size.
5. Write a function that takes a function pointer (operating on two ints) and an array, and applies the function to adjacent elements.
6. Create an array of function pointers for a calculator (add, subtract, multiply, divide). Let the user choose which operation to perform.

### Hard
7. Implement a simple sort function using `void*` and a comparison function pointer (like `qsort`).
8. Write a function `int** create_matrix(int rows, int cols)` that dynamically allocates a 2D matrix and fills it with 0s.
9. Write a program that uses a function pointer as a callback — e.g., a `transform` function that applies a transformation to each element of an array.

## 6. Self-check questions

1. When you add 1 to an `int*`, how many bytes forward does it move? What about a `char*`?
2. What is the difference between an array name and a pointer variable?
3. Why can't you do arithmetic on `void*` without casting?
4. Write the declaration of a pointer to a function that takes two doubles and returns a double.
5. What is the difference between `const int *p` and `int *const p`?
6. How do you create a dynamically-sized array at runtime?
7. What does `pp` represent if `pp` is `int **`?
8. How do you use an array of function pointers?
9. What is the result of `ptr2 - ptr1` when both point into the same array?
10. Why must you cast `void*` before dereferencing it?

## 7. What's next

Pointers give you precise control over memory. Now you're ready to combine variables into groups, work with files, and build complex programs.

Next: **Level 09 — Structs & Files**. You'll learn how to group related data together with `struct`, use `typedef` and `union`, and read/write files.
