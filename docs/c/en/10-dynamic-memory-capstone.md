# [10] Dynamic Memory & Capstone
> **Track:** C Programming · **Level:** 10 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

So far, all memory we've used has been:
- **Stack memory** — automatic, fixed-size, freed when functions return (local variables, fixed arrays)
- **Static memory** — allocated at program start, lives forever (global variables)

Both have rigid lifetimes and sizes determined at compile time. Real programs need:
- Data structures that grow and shrink at runtime (user input, network data)
- Precise control over when memory is allocated and freed
- Objects that outlive the function that created them
- Efficient use of limited memory

**Dynamic memory** on the **heap** solves these problems. This final lesson brings everything together into a capstone project.

## 2. Core concept (absolute zero explanation)

### The stack vs the heap

| Stack | Heap |
|-------|------|
| Automatic allocation/deallocation | Manual allocation/free |
| Fast allocation | Slower allocation |
| Fixed-size arrays only | Any size at runtime |
| Variables freed when function returns | Memory lives until you free it |
| Limited size (~1-8 MB typical) | Large (limited by RAM) |
| No fragmentation | Can fragment over time |

**Analogy:**
- **Stack** = a notepad where you write temporary notes. When you finish a task, you tear off the page. Fast and tidy.
- **Heap** = a giant warehouse where you rent storage lockers. You can get any size locker at any time. But you must return the key when done, or it leaks.

### malloc, calloc, realloc, free

These four functions from `<stdlib.h>` manage heap memory:

- `malloc(size)` — allocates `size` bytes, returns pointer (uninitialized)
- `calloc(count, size)` — allocates `count * size` bytes, zero-initialized
- `realloc(ptr, new_size)` — resizes previously allocated memory
- `free(ptr)` — releases memory back to the heap

## 3. Step-by-step breakdown

### Example 1: malloc and free basics

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // Allocate space for one int (4 bytes)
    int *p = malloc(sizeof(int));
    
    if (p == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }
    
    *p = 42;
    printf("Value: %d\n", *p);
    
    free(p);  // Return memory to the heap
    p = NULL; // Good practice: avoid dangling pointer
    
    // Allocate space for an array of 10 doubles
    double *arr = malloc(10 * sizeof(double));
    
    if (arr == NULL) {
        printf("Allocation failed!\n");
        return 1;
    }
    
    for (int i = 0; i < 10; i++) {
        arr[i] = i * 1.5;
    }
    
    for (int i = 0; i < 10; i++) {
        printf("%.1f ", arr[i]);
    }
    printf("\n");
    
    free(arr);
    arr = NULL;
    
    return 0;
}
```

**MALLOC RULES:**
1. Always check if `malloc` returns `NULL` (out of memory)
2. Always `free` what you allocate
3. After freeing, set pointer to `NULL` (prevents use-after-free)
4. Only free memory that `malloc`/`calloc`/`realloc` returned

### Example 2: calloc — zero-initialized allocation

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // malloc: content is garbage
    int *a = malloc(5 * sizeof(int));
    for (int i = 0; i < 5; i++) {
        printf("malloc[%d] = %d\n", i, a[i]);  // Garbage values
    }
    free(a);
    
    // calloc: content is zero
    int *b = calloc(5, sizeof(int));
    for (int i = 0; i < 5; i++) {
        printf("calloc[%d] = %d\n", i, b[i]);  // All zeros
    }
    free(b);
    
    return 0;
}
```

**When to use which:**
- `malloc` — when you'll immediately initialize all memory
- `calloc` — when you need zero-initialization, or for large allocations (calloc can be more efficient by using OS zero-page tricks)

### Example 3: realloc — resizing allocations

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int size = 5;
    int *arr = malloc(size * sizeof(int));
    
    if (arr == NULL) return 1;
    
    // Fill initial array
    for (int i = 0; i < size; i++) {
        arr[i] = i * 10;
    }
    
    // Need more space — realloc
    int new_size = 10;
    int *temp = realloc(arr, new_size * sizeof(int));
    
    if (temp == NULL) {
        // realloc failed; arr is still valid
        printf("Realloc failed!\n");
        free(arr);
        return 1;
    }
    
    arr = temp;  // Use the new pointer
    
    // Initialize new elements
    for (int i = size; i < new_size; i++) {
        arr[i] = i * 10;
    }
    
    for (int i = 0; i < new_size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    
    free(arr);
    return 0;
}
```

**realloc details:**
- If new size is larger: may move to a new location, copies old data
- If new size is smaller: truncates, may keep same location
- Returns NULL on failure — always use a temporary pointer (don't do `arr = realloc(arr, ...)`)

### Example 4: Memory leaks and valgrind

A **memory leak** happens when you allocate memory but never free it:

```c
#include <stdlib.h>

void leak() {
    int *x = malloc(1000 * sizeof(int));
    // Forgot to free(x) — memory is lost until program exits
}

int main() {
    for (int i = 0; i < 1000000; i++) {
        leak();  // Each call loses 4000 bytes
    }
    // Program will consume all available memory and crash
    return 0;
}
```

**Checking with valgrind:**

```bash
gcc -g program.c -o program
valgrind ./program
```

Valgrind output example:
```
==12345== HEAP SUMMARY:
==12345==     in use at exit: 4,000,000 bytes in 1,000,000 blocks
==12345==   total heap usage: 1,000,000 allocs, 0 frees
==12345== LEAK SUMMARY:
==12345==    definitely lost: 4,000,000 bytes in 1,000,000 blocks
```

### Example 5: Buffer overflow

A **buffer overflow** writes past the end of allocated memory:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char *buffer = malloc(5);  // Space for 4 chars + \0
    
    if (buffer == NULL) return 1;
    
    strcpy(buffer, "Hello, world!");  // OVERFLOW! Way more than 5 bytes
    
    // This may:
    // 1. Corrupt heap metadata (crash on free)
    // 2. Corrupt other data
    // 3. Create a security vulnerability
    
    printf("%s\n", buffer);
    free(buffer);
    
    return 0;
}
```

**Checking with valgrind:**
```bash
valgrind ./program
```
Output includes: `Invalid write of size 1` at the overflow.

### Example 6: Building a dynamic array (vector)

A dynamic array grows as needed — the foundation of many data structures:

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    int size;      // Number of elements currently stored
    int capacity;  // Allocated capacity
} Vector;

Vector* vector_create() {
    Vector *v = malloc(sizeof(Vector));
    v->data = NULL;
    v->size = 0;
    v->capacity = 0;
    return v;
}

void vector_push(Vector *v, int value) {
    if (v->size >= v->capacity) {
        // Need to grow: double the capacity
        int new_cap = v->capacity == 0 ? 4 : v->capacity * 2;
        int *temp = realloc(v->data, new_cap * sizeof(int));
        
        if (temp == NULL) {
            printf("Out of memory!\n");
            exit(1);
        }
        
        v->data = temp;
        v->capacity = new_cap;
    }
    
    v->data[v->size] = value;
    v->size++;
}

int vector_get(Vector *v, int index) {
    if (index < 0 || index >= v->size) {
        printf("Index out of bounds!\n");
        exit(1);
    }
    return v->data[index];
}

void vector_free(Vector *v) {
    free(v->data);
    free(v);
}

int main() {
    Vector *v = vector_create();
    
    for (int i = 0; i < 100; i++) {
        vector_push(v, i * i);
    }
    
    printf("Size: %d, Capacity: %d\n", v->size, v->capacity);
    printf("Element 50: %d\n", vector_get(v, 50));
    
    vector_free(v);
    return 0;
}
```

### Example 7: Building a linked list

A linked list where each node points to the next:

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

typedef struct {
    Node *head;
} LinkedList;

LinkedList* list_create() {
    LinkedList *list = malloc(sizeof(LinkedList));
    list->head = NULL;
    return list;
}

void list_prepend(LinkedList *list, int value) {
    Node *node = malloc(sizeof(Node));
    node->data = value;
    node->next = list->head;
    list->head = node;
}

void list_append(LinkedList *list, int value) {
    Node *node = malloc(sizeof(Node));
    node->data = value;
    node->next = NULL;
    
    if (list->head == NULL) {
        list->head = node;
        return;
    }
    
    Node *current = list->head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = node;
}

void list_print(LinkedList *list) {
    for (Node *current = list->head; current != NULL; current = current->next) {
        printf("%d -> ", current->data);
    }
    printf("NULL\n");
}

void list_free(LinkedList *list) {
    Node *current = list->head;
    while (current != NULL) {
        Node *next = current->next;
        free(current);
        current = next;
    }
    free(list);
}

int main() {
    LinkedList *list = list_create();
    
    list_prepend(list, 10);
    list_prepend(list, 20);
    list_append(list, 30);
    list_append(list, 40);
    
    list_print(list);  // 20 -> 10 -> 30 -> 40 -> NULL
    
    list_free(list);
    return 0;
}
```

### Example 8: Multiple .c files and header files

Separate your program into modules:

**main.c:**
```c
#include <stdio.h>
#include "math_utils.h"  // Our header, use quotes

int main() {
    int result = add(5, 3);
    printf("5 + 3 = %d\n", result);
    printf("5! = %d\n", factorial(5));
    return 0;
}
```

**math_utils.h:**
```c
#ifndef MATH_UTILS_H   // Include guard — prevents double inclusion
#define MATH_UTILS_H

int add(int a, int b);
int factorial(int n);

#endif
```

**math_utils.c:**
```c
#include "math_utils.h"

int add(int a, int b) {
    return a + b;
}

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

**Compile:**
```bash
gcc -c main.c -o main.o        # Compile to object file
gcc -c math_utils.c -o math_utils.o
gcc main.o math_utils.o -o program  # Link
# Or in one step:
gcc main.c math_utils.c -o program
```

### Example 9: Makefiles

A `Makefile` automates compilation:

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -g
TARGET = program
OBJS = main.o math_utils.o

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET)

main.o: main.c math_utils.h
	$(CC) $(CFLAGS) -c main.c

math_utils.o: math_utils.c math_utils.h
	$(CC) $(CFLAGS) -c math_utils.c

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: clean
```

**Usage:**
```bash
make        # Build the program
make clean  # Remove built files
```

### Example 10: Debugging with gdb

```c
#include <stdio.h>

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int main() {
    int nums[] = {1, 2, 3, 4, 5};
    int sum = 0;
    
    for (int i = 0; i <= 5; i++) {  // BUG: should be < 5, not <= 5
        sum += nums[i];
    }
    
    printf("Sum: %d\n", sum);
    printf("10! = %d\n", factorial(10));
    
    return 0;
}
```

**gdb session:**
```bash
gcc -g program.c -o program  # -g includes debug symbols
gdb ./program

(gdb) break main             # Set breakpoint at main
(gdb) run                    # Run until breakpoint
(gdb) next                   # Step to next line
(gdb) print i                # Print variable i
(gdb) print nums[i]          # Print nums[i]
(gdb) watch sum              # Stop when sum changes
(gdb) continue               # Continue execution
(gdb) backtrace              # Show call stack
(gdb) quit                   # Exit gdb
```

### Capstone project: Student Grade Manager

Build a complete program that uses everything you've learned:

```c
/*
 * Student Grade Manager — Capstone Project
 *
 * Features:
 * - Add students (name, ID, grades)
 * - Calculate averages
 * - Save/load from file
 * - Dynamic memory for flexible student count
 * - Makefile for building
 * - gdb debuggable
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME 50
#define MAX_GRADES 20

typedef struct {
    char name[MAX_NAME];
    int id;
    int grades[MAX_GRADES];
    int grade_count;
    double average;
} Student;

typedef struct {
    Student *students;
    int count;
    int capacity;
} Gradebook;

Gradebook* gradebook_create() {
    Gradebook *gb = malloc(sizeof(Gradebook));
    gb->students = NULL;
    gb->count = 0;
    gb->capacity = 0;
    return gb;
}

void gradebook_add(Gradebook *gb, const char *name, int id) {
    if (gb->count >= gb->capacity) {
        int new_cap = gb->capacity == 0 ? 4 : gb->capacity * 2;
        Student *temp = realloc(gb->students, new_cap * sizeof(Student));
        if (temp == NULL) {
            printf("Out of memory!\n");
            exit(1);
        }
        gb->students = temp;
        gb->capacity = new_cap;
    }
    
    Student *s = &gb->students[gb->count];
    strncpy(s->name, name, MAX_NAME - 1);
    s->name[MAX_NAME - 1] = '\0';
    s->id = id;
    s->grade_count = 0;
    s->average = 0.0;
    gb->count++;
}

void gradebook_add_grade(Gradebook *gb, int index, int grade) {
    if (index < 0 || index >= gb->count) return;
    Student *s = &gb->students[index];
    if (s->grade_count >= MAX_GRADES) {
        printf("Max grades reached for %s\n", s->name);
        return;
    }
    s->grades[s->grade_count++] = grade;
    
    // Recalculate average
    int sum = 0;
    for (int i = 0; i < s->grade_count; i++) {
        sum += s->grades[i];
    }
    s->average = (double)sum / s->grade_count;
}

void gradebook_save(Gradebook *gb, const char *filename) {
    FILE *fp = fopen(filename, "wb");
    if (fp == NULL) {
        perror("fopen");
        return;
    }
    
    fwrite(&gb->count, sizeof(int), 1, fp);
    fwrite(gb->students, sizeof(Student), gb->count, fp);
    
    fclose(fp);
    printf("Saved %d students to %s\n", gb->count, filename);
}

Gradebook* gradebook_load(const char *filename) {
    FILE *fp = fopen(filename, "rb");
    if (fp == NULL) {
        perror("fopen");
        return NULL;
    }
    
    Gradebook *gb = gradebook_create();
    
    fread(&gb->count, sizeof(int), 1, fp);
    gb->students = malloc(gb->count * sizeof(Student));
    gb->capacity = gb->count;
    
    fread(gb->students, sizeof(Student), gb->count, fp);
    
    fclose(fp);
    printf("Loaded %d students from %s\n", gb->count, filename);
    return gb;
}

void gradebook_print(Gradebook *gb) {
    printf("\n=== Gradebook ===\n");
    for (int i = 0; i < gb->count; i++) {
        Student *s = &gb->students[i];
        printf("%d. %s (ID: %d) — Avg: %.1f  Grades:",
               i + 1, s->name, s->id, s->average);
        for (int g = 0; g < s->grade_count; g++) {
            printf(" %d", s->grades[g]);
        }
        printf("\n");
    }
    printf("Total: %d students\n", gb->count);
}

void gradebook_free(Gradebook *gb) {
    free(gb->students);
    free(gb);
}

int main() {
    Gradebook *gb = gradebook_create();
    
    gradebook_add(gb, "Alice", 1001);
    gradebook_add(gb, "Bob", 1002);
    gradebook_add(gb, "Charlie", 1003);
    
    gradebook_add_grade(gb, 0, 85);
    gradebook_add_grade(gb, 0, 92);
    gradebook_add_grade(gb, 0, 78);
    
    gradebook_add_grade(gb, 1, 90);
    gradebook_add_grade(gb, 1, 88);
    
    gradebook_add_grade(gb, 2, 95);
    gradebook_add_grade(gb, 2, 87);
    gradebook_add_grade(gb, 2, 91);
    gradebook_add_grade(gb, 2, 84);
    
    gradebook_print(gb);
    
    gradebook_save(gb, "gradebook.bin");
    
    Gradebook *gb2 = gradebook_load("gradebook.bin");
    if (gb2) {
        gradebook_print(gb2);
        gradebook_free(gb2);
    }
    
    gradebook_free(gb);
    return 0;
}
```

## 4. Common mistakes

### Memory leaks
```c
void leak() {
    int *p = malloc(100);
    // never free(p)
}
```
**Fix:** Always match `malloc`/`calloc`/`realloc` with `free`.

### Use-after-free
```c
int *p = malloc(sizeof(int));
free(p);
*p = 42;  // BUG! p is freed — undefined behavior
```
**Fix:** Set `p = NULL` after freeing.

### Double free
```c
free(p);
free(p);  // BUG! Undefined behavior
```
**Fix:** Only free once. Set pointer to NULL after freeing.

### Dangling pointers
When multiple pointers point to the same memory and you free one:
```c
int *p = malloc(sizeof(int));
int *q = p;
free(p);
*q = 10;  // BUG! q points to freed memory
```

### Forgetting to free in all paths
```c
void func() {
    int *p = malloc(100);
    if (something) {
        return;  // BUG: memory leak if this branch is taken
    }
    free(p);
}
```

### Not checking malloc return
```c
int *p = malloc(1000000000000);  // May fail!
*p = 42;  // CRASH if p is NULL
```

## 5. Exercises

### Easy
1. Use `malloc` to create an array of 10 ints, fill with values, print, free.
2. Write a program that demonstrates a memory leak, then fix it.
3. Use `calloc` to create an array of 20 doubles and confirm they're zero.

### Medium
4. Write a program that reads `n` from the user, dynamically allocates an array of `n` ints, fills with `n..1`, and prints.
5. Implement a stack (push/pop) using a dynamic array.
6. Create a Makefile for a project with 3 source files and a header.

### Hard
7. Implement a singly linked list with insert, delete, search, and print functions.
8. Build the capstone Grade Manager and add a "find student by name" feature.
9. Use valgrind to check an intentionally leaky program you write. Fix all leaks.

## 6. Self-check questions

1. What is the difference between the stack and the heap?
2. What does `malloc` return if memory allocation fails?
3. What is the difference between `malloc` and `calloc`?
4. What does `realloc` do? Why should you use a temporary pointer for the return?
5. What is a memory leak? How do you detect one?
6. What is a buffer overflow? Why is it dangerous?
7. What is an include guard (`#ifndef`/`#define`/`#endif`) and why is it needed?
8. What does `-g` do when compiling with gcc?
9. How do you set a breakpoint in gdb?
10. What does a Makefile target look like?

## 7. What's next

Congratulations! You've completed the C Programming track (levels 00-10). You now understand:

- How to write, compile, and run C programs
- Variables, types, math, and operators
- Control flow and loops
- Functions, scope, and recursion
- Arrays and strings
- Pointers (basic and advanced)
- Structs, unions, enums
- File I/O
- Dynamic memory management
- Multi-file projects and Makefiles
- Debugging with gdb

**Where to go from here:**
- **Practice:** Solve problems on coding challenge sites
- **Real projects:** Contribute to open-source C projects
- **Embedded systems:** C on microcontrollers (Arduino, ESP32)
- **Operating systems:** Study Linux kernel or write a simple OS
- **Data structures:** Implement trees, hash tables, graphs
- **Systems programming:** Networking, databases, compilers

C is the foundation. You now have the tools to understand how computers actually work — and to build almost anything.
