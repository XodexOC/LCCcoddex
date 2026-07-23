# [09] Structs & Files
> **Track:** C Programming · **Level:** 09 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

So far, we've worked with individual values and arrays of the same type. But real-world data is complex:
- A student has a name, age, grade, and ID number — mixed types
- A file contains text or binary data that must be read and written
- We need types that represent "multiple values as one thing"

**Structs** group related data of different types into one compound type. **File I/O** lets programs store data permanently.

## 2. Core concept (absolute zero explanation)

### What is a struct?

A **struct** is a way to group multiple variables of different types under one name. Think of it like a paper form: it has many fields (name, age, address), but the whole form is one object.

```c
struct Student {
    char name[50];
    int age;
    double gpa;
    int id;
};
// Now "struct Student" is a type we can use
```

This defines a blueprint. `struct Student` is now a type, like `int` or `double`, but it contains multiple pieces of data.

### What is a file?

A **file** is a sequence of bytes stored on disk. C treats files as streams of bytes — you open a file, read or write bytes, then close it.

Think of a file like a tape reel:
- You open it (mount the reel)
- You read or write at the current position
- You close it when done

## 3. Step-by-step breakdown

### Example 1: Defining and using structs

```c
#include <stdio.h>
#include <string.h>

// Define the struct type (usually outside functions, at the top)
struct Point {
    double x;
    double y;
};

int main() {
    // Declare a struct variable (like declaring an int)
    struct Point p1;
    
    // Access members with dot operator
    p1.x = 3.5;
    p1.y = 7.2;
    
    printf("Point: (%.1f, %.1f)\n", p1.x, p1.y);
    
    // Initialize at declaration
    struct Point p2 = {10.0, 20.0};
    printf("p2: (%.1f, %.1f)\n", p2.x, p2.y);
    
    // Designated initializers (C99+)
    struct Point p3 = { .y = 5.0, .x = 1.0 };
    printf("p3: (%.1f, %.1f)\n", p3.x, p3.y);
    
    // Copying structs
    struct Point p4 = p1;  // Copies all members
    printf("p4: (%.1f, %.1f)\n", p4.x, p4.y);
    
    return 0;
}
```

### Example 2: Arrays of structs and nested structs

```c
#include <stdio.h>
#include <string.h>

struct Date {
    int day;
    int month;
    int year;
};

struct Person {
    char name[50];
    int age;
    struct Date birthday;  // Nested struct
};

int main() {
    // Array of structs
    struct Person people[3];
    
    // Fill the array
    strcpy(people[0].name, "Alice");
    people[0].age = 25;
    people[0].birthday.day = 15;
    people[0].birthday.month = 3;
    people[0].birthday.year = 1999;
    
    strcpy(people[1].name, "Bob");
    people[1].age = 30;
    people[1].birthday = (struct Date){10, 7, 1994};  // Compound literal
    
    strcpy(people[2].name, "Charlie");
    people[2].age = 22;
    
    // Print all
    for (int i = 0; i < 3; i++) {
        printf("%s, age %d, born %d/%d/%d\n",
               people[i].name, people[i].age,
               people[i].birthday.day,
               people[i].birthday.month,
               people[i].birthday.year);
    }
    
    return 0;
}
```

### Example 3: typedef for cleaner types

`typedef` creates an alias for a type:

```c
#include <stdio.h>

// Without typedef:
struct Point {
    double x, y;
};
// Usage: struct Point p;  // Verbose

// With typedef:
typedef struct {
    double x, y;
} Point;
// Usage: Point p;  // Cleaner

// Also works with function pointers:
typedef int (*Operation)(int, int);

int add(int a, int b) { return a + b; }

int main() {
    Point p = {3.5, 7.2};
    printf("(%.1f, %.1f)\n", p.x, p.y);
    
    Operation op = add;
    printf("add(5, 3) = %d\n", op(5, 3));
    
    return 0;
}
```

**Convention:** Use `typedef` for structs to avoid typing `struct` everywhere. But some codebases prefer explicit `struct` for clarity — pick one style and stay consistent.

### Example 4: Pointers to structs and the -> operator

When you have a pointer to a struct, use `->` instead of `.`:

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char name[50];
    int score;
} Player;

void print_player(Player *p) {
    // (*p).score is correct but ugly
    // p->score is the same thing, cleaner
    
    printf("Player: %s, Score: %d\n", p->name, p->score);
    // Equivalent to: (*p).name, (*p).score
}

void set_score(Player *p, int new_score) {
    p->score = new_score;
}

int main() {
    Player p1 = {"Hero", 100};
    print_player(&p1);
    
    set_score(&p1, 200);
    print_player(&p1);
    
    // Dynamic allocation of structs
    Player *p2 = malloc(sizeof(Player));
    if (p2 != NULL) {
        // strcpy(p2->name, "Villain");  // This crashes because malloc doesn't initialize
        // Actually p2->name is an array, not a pointer — this is fine
        // But p2->name might contain garbage if we read it before writing
        strcpy(p2->name, "Villain");
        p2->score = 50;
        print_player(p2);
        free(p2);
    }
    
    return 0;
}
```

### Example 5: Padding and alignment

The size of a struct is NOT always the sum of its fields:

```c
#include <stdio.h>

// Without padding consideration:
struct Packed {
    char c;    // 1 byte
    int i;     // 4 bytes
    char d;    // 1 byte
};  // Naively: 1 + 4 + 1 = 6 bytes

// Actual layout (with padding):
// | c | pad | pad | pad | i | i | i | i | d | pad | pad | pad |
// 1 + 3(pad) + 4 + 1 + 3(pad) = 12 bytes!

struct Better {
    int i;     // 4 bytes
    char c;    // 1 byte
    char d;    // 1 byte
    // Padding: 2 bytes
};  // 4 + 1 + 1 + 2(pad) = 8 bytes

int main() {
    printf("sizeof(struct Packed): %zu\n", sizeof(struct Packed));  // 12
    printf("sizeof(struct Better): %zu\n", sizeof(struct Better));  // 8
    
    printf("Offset of c: %zu\n", offsetof(struct Packed, c));  // 0
    printf("Offset of i: %zu\n", offsetof(struct Packed, i));  // 4 (skips 3 padding bytes)
    printf("Offset of d: %zu\n", offsetof(struct Packed, d));  // 8
    
    return 0;
}
```

**Why padding exists:** CPUs access memory fastest when values are aligned to their size (e.g., 4-byte `int` at addresses divisible by 4). The compiler adds unused bytes (padding) to maintain alignment.

**Optimization tip:** Order struct members from largest to smallest to minimize padding.

### Example 6: Union for type punning

A `union` stores all members at the same memory location — size is the largest member:

```c
#include <stdio.h>

typedef union {
    int i;
    float f;
    unsigned char bytes[4];
} Number;

int main() {
    Number n;
    
    n.i = 1065353216;  // This bit pattern is 1.0 as a float
    printf("As int:   %d\n", n.i);
    printf("As float: %f\n", n.f);  // Interpret same bytes as float
    
    // See the raw bytes
    n.f = 3.14159;
    printf("\nBytes of float 3.14159:\n");
    for (int i = 0; i < 4; i++) {
        printf("  byte %d: 0x%02x\n", i, n.bytes[i]);
    }
    
    return 0;
}
```

**Warning:** Reading a union member that wasn't the last one written is **implementation-defined** (but commonly used in systems programming).

### Example 7: enum for named constants

`enum` creates a set of named integer constants:

```c
#include <stdio.h>

// Days of the week
enum Day { MON, TUE, WED, THU, FRI, SAT, SUN };
//         0    1    2    3    4    5    6

// Custom values
enum Status { OK = 0, WARNING = 1, ERROR = -1 };

// Flags (powers of 2)
enum Permission { READ = 1, WRITE = 2, EXECUTE = 4 };

int main() {
    enum Day today = WED;
    
    if (today == SAT || today == SUN) {
        printf("Weekend!\n");
    } else {
        printf("Weekday\n");
    }
    
    // enum values are integers
    for (int i = MON; i <= SUN; i++) {
        printf("%d ", i);
    }
    printf("\n");
    
    // Combining flags with bitwise OR
    enum Permission perms = READ | WRITE;  // 1 | 2 = 3
    if (perms & READ) {
        printf("Can read\n");
    }
    if (perms & EXECUTE) {
        printf("Can execute\n");
    }
    
    return 0;
}
```

### Example 8: File operations (text mode)

```c
#include <stdio.h>
#include <errno.h>
#include <string.h>

int main() {
    // WRITING to a text file
    FILE *fp = fopen("example.txt", "w");  // "w" = write mode
    
    if (fp == NULL) {
        printf("Error opening file: %s\n", strerror(errno));
        return 1;
    }
    
    fprintf(fp, "Hello, file!\n");
    fprintf(fp, "Line %d: value = %f\n", 1, 3.14);
    
    fclose(fp);  // Always close!
    
    // READING from a text file
    fp = fopen("example.txt", "r");  // "r" = read mode
    
    if (fp == NULL) {
        printf("Error: %s\n", strerror(errno));
        return 1;
    }
    
    char line[256];
    while (fgets(line, sizeof(line), fp) != NULL) {
        printf("Read: %s", line);  // fgets includes \n
    }
    
    fclose(fp);
    
    return 0;
}
```

### Example 9: Binary file operations

```c
#include <stdio.h>

typedef struct {
    int id;
    char name[30];
    double salary;
} Employee;

int main() {
    Employee emp = {1, "Alice", 75000.50};
    
    // WRITE binary
    FILE *fp = fopen("employee.bin", "wb");
    if (fp == NULL) { perror("fopen"); return 1; }
    
    fwrite(&emp, sizeof(Employee), 1, fp);  // Write 1 struct
    fclose(fp);
    
    // READ binary
    Employee emp2;
    fp = fopen("employee.bin", "rb");
    if (fp == NULL) { perror("fopen"); return 1; }
    
    fread(&emp2, sizeof(Employee), 1, fp);  // Read 1 struct
    fclose(fp);
    
    printf("ID: %d, Name: %s, Salary: %.2f\n",
           emp2.id, emp2.name, emp2.salary);
    
    return 0;
}
```

### Example 10: Error handling with perror and errno

```c
#include <stdio.h>
#include <errno.h>
#include <string.h>

int main() {
    FILE *fp = fopen("/nonexistent/file.txt", "r");
    
    if (fp == NULL) {
        // Method 1: perror prints the error message
        perror("fopen failed");
        
        // Method 2: strerror(errno) gives the error string
        printf("Error code %d: %s\n", errno, strerror(errno));
        
        return 1;
    }
    
    fclose(fp);
    return 0;
}
```

## 4. Common mistakes

### Forgetting fclose
Leaving files open wastes resources and can corrupt data. Always close files.

### Using uninitialized struct fields
```c
struct Point p;
printf("%f\n", p.x);  // Garbage! Initialize first.
```

### Confusing . and ->
```c
struct Point *p = malloc(sizeof(struct Point));
p.x = 5.0;   // Wrong! p is a pointer, use ->
p->x = 5.0;  // Correct
```

### Assuming struct size = sum of member sizes
Due to padding, `sizeof(struct)` might be larger than expected.

### Ignoring fopen return value
Always check if `fopen` returns NULL before reading/writing.

### Using text mode for binary data (or vice versa)
On Windows, text mode translates `\n` → `\r\n`. Use `"rb"`/`"wb"` for binary files.

## 5. Exercises

### Easy
1. Define a `struct Book` with title, author, and year. Create and print one.
2. Create a `typedef` for a struct and use it.
3. Write a program that writes "Hello, file!" to a text file and reads it back.

### Medium
4. Create a `struct Student` array of 5 students, read data from user input, save to a binary file, then read back and print.
5. Use `enum` for months and create a function that returns the number of days in a month.
6. Write a program that copies a file byte by byte (like `cp`).

### Hard
7. Write a program that reads a CSV file of student records, parses them into an array of structs, and prints the average grade.
8. Use a `union` to store either an `int`, a `float`, or a `char[20]` string, with an `enum` tag to track which type is stored.
9. Measure and report the padding in several struct and reorder members to minimize it.

## 6. Self-check questions

1. What is a struct and why is it useful?
2. What does `->` do? When do you use it instead of `.`?
3. What is struct padding and why does it exist?
4. What is the difference between a `struct` and a `union`?
5. What does `typedef` do?
6. What are the four common file open modes (`"r"`, `"w"`, `"a"`, `"rb"`)?
7. Why should you always check if `fopen` returns NULL?
8. What does `perror` do?
9. How do you read and write binary data with `fread` and `fwrite`?
10. What is an `enum` and how is it different from a `#define` constant?

## 7. What's next

You can now define complex types and work with files. The final level brings everything together: dynamic memory management, building data structures, working with multi-file projects, and debugging.

Next: **Level 10 — Dynamic Memory & Capstone**. You'll master the heap, build a linked list, use Makefiles, debug with gdb, and create a capstone project.
