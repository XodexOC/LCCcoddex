# [03] Control Flow
> **Track:** C Programming · **Level:** 03 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Programs that run the same way every time are boring and useless. We need programs that make decisions: "If the user is logged in, show the dashboard; otherwise, show the login screen." Or: "If the temperature is above 30°C, turn on the fan."

This is called **control flow** — deciding which code to execute based on conditions.

## 2. Core concept (absolute zero explanation)

### What is a boolean?

A **boolean** is a value that is either **true** or **false**. In C, there is no dedicated boolean type (until C99 with `_Bool`). Instead, C uses integers:

- **0** means **false**
- **Anything non-zero** means **true**

```c
0      → false
1      → true
-5     → true (any non-zero)
42     → true
```

### What is a condition?

A **condition** is an expression that evaluates to true or false. Conditions typically use **comparison operators**:

```c
age >= 18     // true if age is 18 or more
x == 10       // true if x equals 10
score != 0    // true if score is not 0
```

The condition is checked, and based on the result (true or false), the program follows one path or another.

## 3. Step-by-step breakdown

### Example 1: if statement

The `if` statement executes a block of code only if a condition is true:

```c
#include <stdio.h>

int main() {
    int age = 20;
    
    if (age >= 18) {
        printf("You are an adult.\n");
    }
    
    printf("This line always runs.\n");
    
    return 0;
}
```

Output:
```
You are an adult.
This line always runs.
```

If `age` were 15, the `printf` inside the `if` would not execute.

**Syntax breakdown:**
```
if (condition) {
    // code runs only if condition is true
}
```
- `if` — keyword
- `(condition)` — parentheses contain the condition to check
- `{ ... }` — curly braces contain the body (can be multiple lines)
- For a single statement, braces are optional but always recommended

### Example 2: if-else

Use `else` to provide an alternative when the condition is false:

```c
#include <stdio.h>

int main() {
    int temperature = 35;
    
    if (temperature > 30) {
        printf("It's hot outside.\n");
    } else {
        printf("It's not too hot.\n");
    }
    
    return 0;
}
```

Output:
```
It's hot outside.
```

### Example 3: if-else if-else chain

Check multiple conditions in sequence:

```c
#include <stdio.h>

int main() {
    int score = 85;
    
    if (score >= 90) {
        printf("Grade: A\n");
    } else if (score >= 80) {
        printf("Grade: B\n");
    } else if (score >= 70) {
        printf("Grade: C\n");
    } else if (score >= 60) {
        printf("Grade: D\n");
    } else {
        printf("Grade: F\n");
    }
    
    return 0;
}
```

Output: `Grade: B`

**How it works:**
1. Check `score >= 90` → false
2. Check `score >= 80` → true → print "Grade: B"
3. Skip the rest of the chain

Only **one** branch executes — the first one that matches.

### Example 4: Comparison operators

```c
#include <stdio.h>

int main() {
    int a = 5, b = 10;
    
    printf("a == b: %d\n", a == b);   // 0 (false)
    printf("a != b: %d\n", a != b);   // 1 (true)
    printf("a < b:  %d\n", a < b);    // 1 (true)
    printf("a > b:  %d\n", a > b);    // 0 (false)
    printf("a <= b: %d\n", a <= b);   // 1 (true)
    printf("a >= b: %d\n", a >= b);   // 0 (false)
    
    return 0;
}
```

**Common pitfall:** `=` is assignment, `==` is comparison.
```c
if (x = 5)  // Assigns 5 to x, then checks if x is non-zero (always true!)
if (x == 5) // Checks if x equals 5
```

### Example 5: Logical operators (&&, ||, !)

Combine multiple conditions:

```c
#include <stdio.h>

int main() {
    int age = 25;
    int has_license = 1;   // 1 = true
    int has_insurance = 0; // 0 = false
    
    // && (AND): both must be true
    if (age >= 18 && has_license) {
        printf("You can drive.\n");
    }
    
    // || (OR): at least one must be true
    if (has_license || has_insurance) {
        printf("You have at least one document.\n");
    }
    
    // ! (NOT): inverts the condition
    if (!has_insurance) {
        printf("WARNING: No insurance!\n");
    }
    
    // Combined
    if (age >= 18 && has_license && has_insurance) {
        printf("Fully legal driver.\n");
    } else if (age >= 18 && has_license && !has_insurance) {
        printf("You can drive but it's risky.\n");
    } else {
        printf("Cannot drive.\n");
    }
    
    return 0;
}
```

**Truth tables:**

AND (`&&`):
| A | B | A && B |
|---|---|--------|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

OR (`||`):
| A | B | A \|\| B |
|---|---|--------|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

NOT (`!`):
| A | !A |
|---|----|
| 0 | 1 |
| 1 | 0 |

### Short-circuit evaluation

C uses **short-circuit evaluation**: it stops evaluating as soon as the result is determined.

```c
int x = 0;
int y = 5;

// && short-circuits: when x is 0 (false), the whole AND is false,
// so y++ never executes!
if (x != 0 && y++ > 3) {
    printf("This won't run\n");
}
printf("y is still %d\n", y);  // y is still 5, not 6

// || short-circuits: when first is true, second is skipped
if (x == 0 || y++ > 3) {
    // y++ didn't execute either!
}
```

**Important:** Don't put expressions with side effects (like `++`) in conditions unless you fully understand short-circuiting.

### Example 6: switch/case/break/default

`switch` is useful when checking a single variable against many specific values:

```c
#include <stdio.h>

int main() {
    int day = 3;  // 1=Monday ... 7=Sunday
    
    switch (day) {
        case 1:
            printf("Monday\n");
            break;
        case 2:
            printf("Tuesday\n");
            break;
        case 3:
            printf("Wednesday\n");
            break;
        case 4:
            printf("Thursday\n");
            break;
        case 5:
            printf("Friday\n");
            break;
        case 6:
            printf("Saturday\n");
            break;
        case 7:
            printf("Sunday\n");
            break;
        default:
            printf("Invalid day\n");
            break;
    }
    
    return 0;
}
```

**Why `break` matters:**

Without `break`, execution "falls through" to the next case:

```c
int x = 2;
switch (x) {
    case 1:
        printf("One\n");
    case 2:
        printf("Two\n");    // This runs
    case 3:
        printf("Three\n");  // This ALSO runs (fall-through!)
        break;
    default:
        printf("Other\n");
}
```

Output:
```
Two
Three
```

Fall-through is sometimes useful intentionally:

```c
char grade = 'B';
switch (grade) {
    case 'A':
    case 'B':
    case 'C':
        printf("Passing\n");
        break;
    case 'D':
    case 'F':
        printf("Failing\n");
        break;
    default:
        printf("Invalid grade\n");
}
```

### Example 7: Ternary operator (? :)

A shorthand for simple if-else that returns a value:

```c
#include <stdio.h>

int main() {
    int age = 20;
    
    // Long way:
    char* status;
    if (age >= 18) {
        status = "Adult";
    } else {
        status = "Minor";
    }
    
    // Ternary (short way):
    char* status2 = (age >= 18) ? "Adult" : "Minor";
    
    printf("Status: %s\n", status2);
    
    // Can be used inline:
    printf("You have %d %s.\n", 5, (5 == 1) ? "apple" : "apples");
    
    return 0;
}
```

**Syntax:** `condition ? value_if_true : value_if_false`

### Example 8: Nested conditionals

You can put `if` statements inside other `if` statements:

```c
#include <stdio.h>

int main() {
    int x = 10, y = 5;
    
    if (x > 0) {
        if (y > 0) {
            printf("Both are positive.\n");
        } else if (y == 0) {
            printf("x positive, y is zero.\n");
        } else {
            printf("x positive, y negative.\n");
        }
    } else {
        printf("x is not positive.\n");
    }
    
    return 0;
}
```

**Dangling else problem:** An `else` belongs to the nearest unmatched `if`:

```c
if (x > 0)
    if (y > 0)
        printf("Both positive\n");
else                    // This else belongs to "if (y > 0)", NOT "if (x > 0)"!
    printf("x is not positive\n");
```

Always use braces `{}` to make your intention clear.

## 4. Common mistakes

### Using = instead of ==
```c
if (x = 5)    // Assigns 5 to x, condition is always true
if (x == 5)   // Correct comparison
```

**Defensive trick:** Write the constant on the left:
```c
if (5 == x)   // If you type = by accident, 5 = x won't compile
```

### Forgetting break in switch
```c
switch (x) {
    case 1:
        printf("One\n");  // Falls through to case 2!
    case 2:
        printf("Two\n");
        break;
}
```

### Using & instead of &&
```c
if (x > 0 & x < 10)   // & is bitwise AND, not logical
if (x > 0 && x < 10)  // Correct
```

### Misunderstanding truthiness
```c
if (x = 0)     // Assigns 0 to x, condition is ALWAYS false!
```

### Comparison chain doesn't work like math
```c
if (10 < x < 20)  // This evaluates as (10 < x) < 20
                  // (10 < x) is 0 or 1, which is always < 20 → always true!
if (x > 10 && x < 20)  // Correct
```

## 5. Exercises

### Easy
1. Write a program that checks if a number is positive, negative, or zero.
2. Write a program that takes a number and prints whether it's even or odd using `%`.
3. Write a program that converts a number 1-12 to a month name using `switch`.

### Medium
4. Write a program that takes three numbers and prints the largest (nested if or &&).
5. Write a program that checks if a year is a leap year (divisible by 4, but not 100 unless also 400).
6. Rewrite an if-else chain as a `switch` statement and vice versa.

### Hard
7. Write a simple calculator: take operator (`+`, `-`, `*`, `/`) and two numbers, perform the operation using `switch`.
8. Write a program that categorizes a character: uppercase letter, lowercase letter, digit, or other.
9. Demonstrate short-circuit evaluation: write an expression where the second condition has a side effect but never executes.

## 6. Self-check questions

1. What values are considered "true" in C? What is "false"?
2. What is the difference between `=` and `==`?
3. How do you check if a number is between 10 and 20 (inclusive)?
4. What is short-circuit evaluation? Give an example.
5. What does `break` do in a `switch` statement? What happens without it?
6. What does the ternary operator `? :` do?
7. Why is `10 < x < 20` always true in C?
8. How does C determine which `if` an `else` belongs to (dangling else)?
9. Write an expression that is true if `x` is even and positive.
10. What is the output of `!0` in C? Why?

## 7. What's next

You can now make decisions in your programs. But a program that checks a condition once and stops is still very limited. You need to repeat actions.

Next: **Level 04 — Loops**. You'll learn how to repeat code using `while`, `do-while`, and `for` loops, and control repetition with `break` and `continue`.
