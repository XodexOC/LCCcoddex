# [04] Loops
> **Track:** C Programming · **Level:** 04 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Writing code once is rarely enough. You might need to:
- Print numbers 1 to 100
- Process every character in a document
- Keep asking the user for input until they give a valid answer
- Calculate the sum of a thousand numbers

Copying and pasting the same code 100 times is absurd. We need a way to **repeat** a block of code — either a fixed number of times, or while a condition is true, or until a condition is met.

Loops solve this problem.

## 2. Core concept (absolute zero explanation)

### What is a loop?

A **loop** is a programming construct that repeats a block of code multiple times.

Think of a loop like a washing machine cycle:
1. Start the machine
2. Wash clothes
3. Check if the timer has run out
4. If not, go back to step 2
5. If yes, stop

The washing machine "loops" through the wash step until the timer condition is met.

### The three elements of every loop

Every loop needs:
1. **Initialization** — set up before the loop starts (e.g., `int i = 0;`)
2. **Condition** — check before each repetition (e.g., `i < 10`)
3. **Update** — change something each iteration (e.g., `i++`)

If you forget the update, the condition might never become false, causing an **infinite loop**.

## 3. Step-by-step breakdown

### Example 1: while loop

The `while` loop checks the condition **before** executing the body. If the condition is false initially, the body never runs.

```c
#include <stdio.h>

int main() {
    int count = 1;
    
    while (count <= 5) {
        printf("Count: %d\n", count);
        count++;  // VERY IMPORTANT: update the condition variable
    }
    
    printf("Loop finished!\n");
    
    return 0;
}
```

Output:
```
Count: 1
Count: 2
Count: 3
Count: 4
Count: 5
Loop finished!
```

**Execution trace:**
1. `count = 1`
2. Check: `1 <= 5` → true → print, `count` becomes 2
3. Check: `2 <= 5` → true → print, `count` becomes 3
4. Check: `3 <= 5` → true → print, `count` becomes 4
5. Check: `4 <= 5` → true → print, `count` becomes 5
6. Check: `5 <= 5` → true → print, `count` becomes 6
7. Check: `6 <= 5` → false → exit loop

```c
// SYNTAX
while (condition) {
    // body: runs while condition is true
}
```

### Example 2: do-while loop

The `do-while` loop checks the condition **after** executing the body. This guarantees the body runs **at least once**.

```c
#include <stdio.h>

int main() {
    int guess;
    int secret = 7;
    
    do {
        printf("Guess the number (1-10): ");
        scanf("%d", &guess);
        
        if (guess < secret) {
            printf("Too low!\n");
        } else if (guess > secret) {
            printf("Too high!\n");
        }
    } while (guess != secret);
    
    printf("Correct!\n");
    
    return 0;
}
```

This is perfect for user input — you always prompt at least once.

```c
// SYNTAX
do {
    // body: runs at least once
} while (condition);  // ← note the semicolon!
```

**When to use while vs do-while:**
- `while` — "Maybe zero times" (check before)
- `do-while` — "At least once" (check after)

### Example 3: for loop

The `for` loop is the most compact. It bundles initialization, condition, and update into one line.

```c
#include <stdio.h>

int main() {
    for (int i = 1; i <= 5; i++) {
        printf("Iteration %d\n", i);
    }
    return 0;
}
```

Output:
```
Iteration 1
Iteration 2
Iteration 3
Iteration 4
Iteration 5
```

**Structure:**
```
for (initialization; condition; update) {
    // body
}
```

| Part | What it does | When it runs |
|------|-------------|-------------|
| `int i = 1` | Initialization | Once, before the loop starts |
| `i <= 5` | Condition | Checked before each iteration |
| `i++` | Update | After each iteration's body |

**The for loop's execution order:**
1. `int i = 1` (once)
2. Check: `i <= 5` → true
3. Execute body: `printf`
4. Update: `i++`
5. Go to step 2

**Equivalent while loop:**
```c
int i = 1;          // initialization
while (i <= 5) {    // condition
    printf("%d\n", i);
    i++;            // update
}
```

### Example 4: Loop patterns

**Counting pattern:**

```c
// Count up
for (int i = 0; i < 10; i++) {
    printf("%d ", i);
}
// Output: 0 1 2 3 4 5 6 7 8 9

// Count down
for (int i = 10; i > 0; i--) {
    printf("%d ", i);
}
// Output: 10 9 8 7 6 5 4 3 2 1

// Count by 2
for (int i = 0; i <= 10; i += 2) {
    printf("%d ", i);
}
// Output: 0 2 4 6 8 10
```

**Accumulating pattern (sum):**

```c
#include <stdio.h>

int main() {
    int sum = 0;
    
    for (int i = 1; i <= 100; i++) {
        sum += i;  // add each number to the running total
    }
    
    printf("Sum of 1 to 100: %d\n", sum);
    
    return 0;
}
```

**Searching/finding pattern:**

```c
#include <stdio.h>

int main() {
    // Find the first number divisible by 7 and 13
    for (int i = 1; ; i++) {  // no condition = infinite loop
        if (i % 7 == 0 && i % 13 == 0) {
            printf("Found: %d\n", i);
            break;  // exit the loop
        }
    }
    
    return 0;
}
```

### Example 5: break and continue

**break** — immediately exits the loop:

```c
#include <stdio.h>

int main() {
    for (int i = 1; i <= 10; i++) {
        if (i == 5) {
            break;  // loop stops when i is 5
        }
        printf("%d ", i);
    }
    printf("\nDone!");
    
    return 0;
}
```

Output: `1 2 3 4 Done!`

**continue** — skips the rest of the current iteration and moves to the next:

```c
#include <stdio.h>

int main() {
    for (int i = 1; i <= 10; i++) {
        if (i % 2 == 0) {
            continue;  // skip even numbers
        }
        printf("%d ", i);
    }
    printf("\nOnly odds above!");
    
    return 0;
}
```

Output: `1 3 5 7 9 Only odds above!`

### Example 6: Nested loops

A loop inside another loop. The inner loop runs completely for each iteration of the outer loop.

```c
#include <stdio.h>

int main() {
    for (int row = 1; row <= 3; row++) {
        for (int col = 1; col <= 4; col++) {
            printf("[%d,%d] ", row, col);
        }
        printf("\n");  // new line after each row
    }
    
    return 0;
}
```

Output:
```
[1,1] [1,2] [1,3] [1,4]
[2,1] [2,2] [2,3] [2,4]
[3,1] [3,2] [3,3] [3,4]
```

**Multiplication table:**

```c
#include <stdio.h>

int main() {
    for (int i = 1; i <= 10; i++) {
        for (int j = 1; j <= 10; j++) {
            printf("%4d", i * j);  // %4d pads to 4 characters
        }
        printf("\n");
    }
    
    return 0;
}
```

### Example 7: Infinite loops (and how to avoid them)

An **infinite loop** runs forever because the condition never becomes false.

```c
// Infinite loop — missing update
int i = 0;
while (i < 10) {
    printf("Oops\n");
    // forgot i++ — i stays 0 forever
}

// Infinite loop — condition never false
for (int i = 0; i >= 0; i++) {
    printf("i keeps growing but never becomes negative\n");
}
```

**Deliberate infinite loops:**

Sometimes you want an infinite loop on purpose:

```c
// Server that runs forever
while (1) {   // 1 is always true
    // handle network requests
}

// Or equivalently:
for (;;) {
    // handle network requests
}
```

Exit these with `break` or `return`.

### Example 8: Variable scope in loops

Variables declared inside a loop are re-created each iteration:

```c
for (int i = 0; i < 3; i++) {
    int x = 10;        // created fresh each iteration
    x += i;
    printf("x = %d\n", x);
}
// Output: x = 10, x = 11, x = 12 — each iteration starts with x = 10
```

Variables declared in the initialization part (C99) are local to the loop:

```c
for (int i = 0; i < 5; i++) { }
// printf("%d", i);  // Error: i is out of scope here!
```

## 4. Common mistakes

### Off-by-one errors
```c
// Runs 10 times (i = 0 to 9), NOT 9 times
for (int i = 0; i < 10; i++) { }

// Also runs 10 times (i = 1 to 10)
for (int i = 1; i <= 10; i++) { }

// Common bug: using <= when you meant <
int arr[10];
for (int i = 0; i <= 10; i++) {  // Bug! i goes 0 to 10 = 11 iterations
    arr[i] = 0;                   // arr[10] is out of bounds!
}
```

### Infinite loop due to semicolon
```c
int i = 0;
while (i < 10);  // <-- semicolon! Empty body, loops forever
{
    printf("%d\n", i);
    i++;
}
```

### Forgetting to update the loop variable
```c
int i = 0;
while (i < 10) {
    printf("%d\n", i);
    // forgot i++ → infinite loop
}
```

### Using = instead of == in condition
```c
for (int i = 0; i = 10; i++)  // Condition is assignment (=10), always true
```

### Loop variable overflow
```c
for (unsigned int i = 10; i >= 0; i--)  // Infinite! unsigned is never < 0
```

## 5. Exercises

### Easy
1. Print numbers 1 to 20 using a `for` loop.
2. Print the even numbers between 1 and 50 using a `while` loop.
3. Calculate and print the sum of integers from 1 to `n` (user enters `n`).

### Medium
4. Print a right-angle triangle of stars:
   ```
   *
   **
   ***
   ****
   ```
5. Print the multiplication table for a number entered by the user.
6. Use nested loops to print a 5x5 grid of numbers 1-25.
7. Write a program that keeps reading numbers until the user enters 0, then prints the sum.

### Hard
8. Print a diamond shape using nested loops and spaces.
9. FizzBuzz: print 1 to 100, but multiples of 3 → "Fizz", multiples of 5 → "Buzz", both → "FizzBuzz".
10. Write a program that finds the Greatest Common Divisor (GCD) of two numbers using Euclid's algorithm (while loop).

## 6. Self-check questions

1. What are the three elements every loop needs?
2. What is the difference between `while` and `do-while`?
3. Write a `for` loop that counts from 10 down to 1.
4. What does `break` do in a loop? What does `continue` do?
5. What is the execution order of a `for` loop's three parts?
6. How do nested loops work — does the inner or outer loop complete first?
7. How do you write an intentional infinite loop?
8. What is an off-by-one error? Give an example.
9. What happens if the condition in a `for` loop is initially false?
10. What is the scope of a variable declared inside a `for` loop's initialization?

## 7. What's next

You can now repeat code efficiently. But as programs grow, you need to organize code into reusable blocks.

Next: **Level 05 — Functions**. You'll learn how to create named blocks of reusable code, pass data in and get results back, and understand scope and the call stack.
