# [06] Arrays & Strings
> **Track:** C Programming · **Level:** 06 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

So far, every variable holds one value. What if you need to store 100 test scores? Creating 100 separate variables (`score1`, `score2`, `score3`...) would be insane. You cannot loop over 100 differently-named variables.

We need a way to store a **collection** of values under one name, and access each value by its position (index). This is an **array**.

We also need to work with **text** — a person's name, a sentence, a file path. Text in C is stored as an array of characters, with some special rules.

## 2. Core concept (absolute zero explanation)

### What is an array?

An **array** is a contiguous block of memory that holds multiple values of the **same type**, all under one name.

Think of an array like a row of lockers in a school hallway:
- The lockers are next to each other (contiguous)
- Each locker holds the same kind of thing (same type)
- Each locker has a number (index: 0, 1, 2, 3...)
- The whole row has one name (e.g., "locker_row")

```
Array: scores[5]
Index: [0]  [1]  [2]  [3]  [4]
Value: 85   92   78   90   88
Memory: | 85 | 92 | 78 | 90 | 88 |
```

**Key rule: Array indices start at 0, not 1.** The first element is `array[0]`, the second is `array[1]`, etc.

### What is a string in C?

A **string** in C is simply an array of characters terminated by a special character: the **null terminator** (`\0`, which has ASCII value 0).

```
String: "Hello"
Memory: | 'H' | 'e' | 'l' | 'l' | 'o' | '\0' |
Index:    0     1     2     3     4     5
```

The `\0` marks the end of the string. Without it, there's no way to know where the string ends.

## 3. Step-by-step breakdown

### Example 1: Declaring and using arrays

```c
#include <stdio.h>

int main() {
    // Declare an array of 5 integers
    int scores[5];
    
    // Assign values to each element
    scores[0] = 85;
    scores[1] = 92;
    scores[2] = 78;
    scores[3] = 90;
    scores[4] = 88;
    
    // Access and print elements
    printf("First score: %d\n", scores[0]);
    printf("Third score: %d\n", scores[2]);
    
    // Initialize at declaration time
    int numbers[4] = {10, 20, 30, 40};
    
    // Partial initialization — remaining are set to 0
    int partial[5] = {1, 2};  // {1, 2, 0, 0, 0}
    
    // Let the compiler count for you
    int auto_size[] = {1, 2, 3, 4, 5};  // size is 5
    
    // Size of array in bytes vs number of elements
    printf("sizeof(numbers) = %zu bytes\n", sizeof(numbers));
    printf("Number of elements = %zu\n", sizeof(numbers) / sizeof(numbers[0]));
    
    return 0;
}
```

### Example 2: Arrays and loops (the fundamental pair)

Arrays and `for` loops are best friends. The loop index gives you the array index:

```c
#include <stdio.h>

int main() {
    int scores[5] = {85, 92, 78, 90, 88};
    int sum = 0;
    
    // Print all scores
    for (int i = 0; i < 5; i++) {
        printf("Score %d: %d\n", i + 1, scores[i]);
    }
    
    // Calculate average
    for (int i = 0; i < 5; i++) {
        sum += scores[i];
    }
    
    printf("Average: %.1f\n", (double)sum / 5);
    
    // Find maximum
    int max = scores[0];
    for (int i = 1; i < 5; i++) {
        if (scores[i] > max) {
            max = scores[i];
        }
    }
    printf("Max score: %d\n", max);
    
    return 0;
}
```

**Pattern:** `for (int i = 0; i < array_size; i++)` — this is the standard array traversal pattern.

### Example 3: Multidimensional arrays

Think of a 2D array as a table (rows and columns):

```c
#include <stdio.h>

int main() {
    // 3 rows, 4 columns
    int grid[3][4] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };
    
    // Access: array[row][col]
    printf("Element at [1][2]: %d\n", grid[1][2]);  // 7
    
    // Nested loops to print the grid
    for (int row = 0; row < 3; row++) {
        for (int col = 0; col < 4; col++) {
            printf("%4d", grid[row][col]);
        }
        printf("\n");
    }
    
    return 0;
}
```

Output:
```
   1   2   3   4
   5   6   7   8
   9  10  11  12
```

**Memory layout:** 2D arrays are stored row-by-row in contiguous memory:
```
grid[0][0], grid[0][1], grid[0][2], grid[0][3],
grid[1][0], grid[1][1], grid[1][2], grid[1][3],
grid[2][0], grid[2][1], grid[2][2], grid[2][3]
```

### Example 4: Strings — char arrays with '\0'

```c
#include <stdio.h>

int main() {
    // Method 1: string literal (compiler adds \0 automatically)
    char name1[] = "Alice";
    // Memory: 'A' 'l' 'i' 'c' 'e' '\0' — size is 6!

    // Method 2: explicit array with \0
    char name2[6] = {'A', 'l', 'i', 'c', 'e', '\0'};
    
    // Method 3: pointer to string literal (read-only)
    const char* name3 = "Bob";
    
    printf("Names: %s, %s, %s\n", name1, name2, name3);
    
    // %s prints until it finds \0
    printf("sizeof(name1) = %zu\n", sizeof(name1));  // 6 (includes \0)
    printf("String length = %zu\n", strlen(name1));   // 5 (does NOT include \0)
    
    return 0;
}
```

**Key difference:**
- `sizeof("Hello")` = 6 (includes `\0`)
- `strlen("Hello")` = 5 (counts characters before `\0`)

### Example 5: String functions (string.h)

```c
#include <stdio.h>
#include <string.h>  // Required for string functions

int main() {
    char dest[20];
    char src[] = "Hello";
    
    // strlen: get string length (excluding \0)
    printf("Length of '%s': %zu\n", src, strlen(src));
    
    // strcpy: copy string (DANGEROUS — no bounds check!)
    strcpy(dest, src);         // dest now contains "Hello"
    printf("Copied: %s\n", dest);
    
    // strcat: concatenate (append) — DANGEROUS!
    strcat(dest, " World");    // dest now contains "Hello World"
    printf("Concatenated: %s\n", dest);
    
    // strcmp: compare strings (returns 0 if equal)
    char a[] = "apple";
    char b[] = "banana";
    char c[] = "apple";
    
    printf("strcmp(\"%s\", \"%s\") = %d\n", a, b, strcmp(a, b));  // negative (a < b)
    printf("strcmp(\"%s\", \"%s\") = %d\n", a, c, strcmp(a, c));  // 0 (equal)
    printf("strcmp(\"%s\", \"%s\") = %d\n", b, a, strcmp(b, a));  // positive (b > a)
    
    return 0;
}
```

**strcmp return values:**
- `0` — strings are equal
- Negative — first string comes before second alphabetically
- Positive — first string comes after second

### Example 6: Safe string input

NEVER use `gets()` — it cannot prevent buffer overflow:

```c
#include <stdio.h>
#include <string.h>

int main() {
    char buffer[10];
    
    // DANGEROUS: gets() has no bounds checking
    // gets(buffer);  // If user types more than 9 chars → buffer overflow!
    
    // SAFE: fgets() limits input
    printf("Enter text (max 9 chars): ");
    fgets(buffer, sizeof(buffer), stdin);
    // fgets reads at most sizeof(buffer)-1 chars, adds \0
    
    // fgets includes the newline; remove it
    size_t len = strlen(buffer);
    if (len > 0 && buffer[len - 1] == '\n') {
        buffer[len - 1] = '\0';  // replace \n with \0
    }
    
    printf("You entered: '%s'\n", buffer);
    
    return 0;
}
```

**Rule:** Always use `fgets()` (or `scanf` with width limit), never `gets()`.

### Example 7: printf and scanf with %s

```c
#include <stdio.h>

int main() {
    char name[50];
    
    printf("What's your name? ");
    scanf("%49s", name);  // %49s reads at most 49 chars (room for \0)
    // Note: no & before name — arrays decay to pointers automatically
    
    printf("Hello, %s!\n", name);
    
    // Multiple inputs
    char first[20], last[20];
    printf("Enter first and last name: ");
    scanf("%19s %19s", first, last);
    printf("First: %s, Last: %s\n", first, last);
    
    return 0;
}
```

**Warning:** `scanf("%s", ...)` stops at whitespace (space, tab, newline). To read a line with spaces, use `fgets`.

### Example 8: Arrays as function arguments

Arrays are **passed by reference** (technically, the pointer to the first element is passed):

```c
#include <stdio.h>

// Must pass the size separately — the function cannot know the array size!
void print_array(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

// Functions can modify arrays through the pointer
void double_elements(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] *= 2;
    }
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    
    printf("Before: ");
    print_array(numbers, size);
    
    double_elements(numbers, size);
    
    printf("After:  ");
    print_array(numbers, size);
    
    return 0;
}
```

**Important:** `sizeof(arr)` inside `print_array` would give the size of a **pointer**, not the array. Always pass the size separately.

## 4. Common mistakes

### Out-of-bounds access
```c
int arr[5] = {1, 2, 3, 4, 5};
arr[5] = 6;  // BUG! Valid indices are 0-4, arr[5] is out of bounds
// This overwrites whatever is next in memory — undefined behavior!
```

### Off-by-one: forgetting index 0
```c
int scores[5];
for (int i = 1; i <= 5; i++) {  // BUG! Skipping scores[0], scores[5] is out of bounds
    scores[i] = i * 10;
}
```

### Forgetting space for \0
```c
char str[5] = "Hello";  // BUG! "Hello" is 5 chars + \0 = 6 bytes
// str needs at least 6 elements
```

### Using = instead of strcpy for strings
```c
char a[20] = "Hello";
char b[20];
b = a;          // BUG! Can't assign arrays with =
strcpy(b, a);   // Correct: copy element by element
```

### Using gets()
```c
gets(buffer);  // NEVER do this
fgets(buffer, sizeof(buffer), stdin);  // Always safe
```

### sizeof on array parameter
```c
void func(int arr[]) {
    printf("%zu\n", sizeof(arr));  // Prints size of a pointer (4 or 8), not the array!
}
```

## 5. Exercises

### Easy
1. Declare an array of 5 doubles, initialize them, and print all values.
2. Write a program that finds the sum of all elements in an array of 10 integers.
3. Create a string containing your name and print it character by character using a loop.

### Medium
4. Write a function that reverses an array in place.
5. Write a function that counts how many times a specific character appears in a string.
6. Create a 2D array representing a 3x3 tic-tac-toe board, fill it with 'X', 'O', and ' ', and print it.
7. Write a program that reads a line of text and prints it in reverse (use `fgets` and `strlen`).

### Hard
8. Write your own `my_strlen` and `my_strcpy` functions (without using `string.h`).
9. Write a program that checks if a string is a palindrome (reads same forwards and backwards).
10. Write a function that removes all spaces from a string in place.

## 6. Self-check questions

1. What index does the first element of an array have?
2. What happens if you access `arr[10]` when `arr` has only 5 elements?
3. What is the difference between `sizeof(arr)` and `strlen(arr)` when `arr` is a string?
4. What does `\0` do, and why is it necessary?
5. Why is `gets()` dangerous, and what should you use instead?
6. What does `strcmp` return when two strings are equal?
7. How do you pass an array to a function? Why must you also pass the size?
8. What is the memory layout of a 2D array?
9. Why does `scanf("%s", name)` not need `&` before `name`?
10. How do you remove the trailing newline from `fgets` input?

## 7. What's next

Arrays give you collections, but they have a fixed size determined at compile time. What if you need to work with dynamically-sized data? And what if you want to work with memory locations directly?

Next: **Level 07 — Pointers Basics**. You'll learn about memory addresses, how to store and use them, and the foundation for dynamic memory management.
