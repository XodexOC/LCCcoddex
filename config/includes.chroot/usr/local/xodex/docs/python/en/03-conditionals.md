# [03] Conditionals & Decision Making
> **Track:** Python · **Level:** 03 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

So far every program ran top-to-bottom, always executing every line the same
way. But real programs must make choices: "If the user is logged in, show the
dashboard; otherwise, show the login screen."

**Conditionals** let your program branch — run some code only when a certain
condition is true and different code otherwise.

In this lesson you will learn:
- The `if`/`elif`/`else` decision chain
- **Truthiness** — which values Python considers false
- The `in` and `not in` membership operators
- `is` and `is not` for identity comparisons
- **Ternary expressions** — compact if/else on one line
- `match`/`case` — Python 3.10+ pattern matching

---

## 2. Core concept

### 2.1 The `if` statement

```python
if condition:
    # code here runs if condition is True
```

The `condition` is any expression that evaluates to `True` or `False`. The body
is **indented** (usually 4 spaces). Indentation is how Python knows which code
belongs to the `if`.

### 2.2 `elif` and `else`

```python
if condition1:
    # runs if condition1 is True
elif condition2:
    # runs if condition1 is False and condition2 is True
else:
    # runs if neither condition1 nor condition2 was True
```

- You can have zero or more `elif` blocks.
- `else` is optional.
- Only **one** branch ever runs — the first one whose condition is `True`.

### 2.3 Truthiness

Every value in Python is either **truthy** or **falsy** when used in a
conditional. The following are *always* falsy:

| Value | Why it's falsy |
|---|---|
| `False` | Boolean false |
| `None` | Nothing |
| `0` | Zero integer |
| `0.0` | Zero float |
| `""` | Empty string |
| `[]` | Empty list (Level 05) |
| `()` | Empty tuple (Level 05) |
| `{}` | Empty dict (Level 05) |
| `set()` | Empty set (Level 05) |

Everything else is truthy.

### 2.4 `in` and `is`

- `in` checks if a value is *contained* in a collection or string.
- `is` checks if two variables refer to the *same object in memory* (not just
  equal values).

### 2.5 `match`/`case`

Python 3.10 introduced `match`/`case` (structural pattern matching). It is like
a supercharged `if`/`elif` that can match on values, types, and even structures.

---

## 3. Step-by-step breakdown

### Step 1: Simple `if`

```python
age = 18

if age >= 18:
    print("You are an adult.")
```

If `age` is 18 or greater, Python prints the message. Otherwise it skips the
indented block.

```python
age = 15

if age >= 18:
    print("You are an adult.")   # never runs
```

### Step 2: `if`/`else`

```python
age = 15

if age >= 18:
    print("You can vote.")
else:
    print("You are too young to vote.")
```

### Step 3: `if`/`elif`/`else` chain

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade is {grade}.")   # B
```

### Step 4: Nested conditionals

You can put `if` inside another `if`:

```python
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("Welcome!")
    else:
        print("ID required.")
else:
    print("Too young.")
```

But deep nesting makes code hard to read. Prefer `and`:

```python
if age >= 18 and has_id:
    print("Welcome!")
elif age < 18:
    print("Too young.")
else:
    print("ID required.")
```

### Step 5: Truthiness examples

```python
name = ""

if name:                     # empty string is falsy
    print(f"Hello, {name}")
else:
    print("No name entered.")    # this runs
```

```python
count = 0

if count:                    # zero is falsy
    print(f"You have {count} items.")
else:
    print("Your cart is empty.")  # this runs
```

**Common idiom:** check if a value is not None/empty:

```python
result = get_something()   # might return None
if result:                 # works if result is truthy
    process(result)
```

Be careful: this fails if the valid result could be `0`, `""`, `False`, etc.

### Step 6: `in` and `not in`

**With strings:**

```python
>>> "Py" in "Python"
True
>>> "xyz" in "Python"
False
>>> "Py" not in "Python"
False
```

**With lists (Level 05):**

```python
>>> fruits = ["apple", "banana", "cherry"]
>>> "banana" in fruits
True
>>> "grape" in fruits
False
```

**Practical use:**

```python
name = input("Enter your name: ")
if name in ("Alice", "Bob", "Charlie"):
    print("Welcome, VIP!")
else:
    print("Welcome, guest.")
```

### Step 7: `is` vs `==`

`==` checks **value equality** — do two things hold the same value?

`is` checks **identity** — do two variables point to the exact same object in
memory?

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

a == b   # True — same value
a is b   # False — different objects
a is c   # True — same object
```

**Use `is` for:** comparing to `None`, `True`, `False`.

```python
if result is None:      # ✅ preferred
if result == None:      # ❌ works but not idiomatic
```

### Step 8: Ternary (conditional expression)

A compact way to write simple `if`/`else` in one line:

```python
value_if_true if condition else value_if_false
```

```python
age = 20
status = "adult" if age >= 18 else "minor"
print(status)   # adult
```

```python
x = 5
result = "even" if x % 2 == 0 else "odd"
print(result)   # odd
```

### Step 9: `match`/`case` (Python 3.10+)

Basic usage — like a switch statement in other languages:

```python
command = input("Enter command: ")

match command:
    case "start":
        print("Starting...")
    case "stop":
        print("Stopping...")
    case "restart":
        print("Restarting...")
    case _:                     # default case (underscore matches anything)
        print("Unknown command.")
```

**Matching with a variable:**

```python
point = (3, 5)

match point:
    case (0, 0):
        print("Origin")
    case (x, 0):
        print(f"On X axis at {x}")
    case (0, y):
        print(f"On Y axis at {y}")
    case (x, y):
        print(f"At ({x}, {y})")
```

**Adding guards (additional conditions):**

```python
value = 42

match value:
    case x if x < 0:
        print("Negative")
    case x if x == 0:
        print("Zero")
    case x if x > 0:
        print("Positive")
```

### Step 10: Putting it all together

```python
age = int(input("Enter your age: "))
has_license = input("Do you have a license? (yes/no): ").lower() == "yes"

if age < 16:
    print("You are too young to drive.")
elif age >= 16 and has_license:
    print("You can drive!")
elif age >= 16 and not has_license:
    print("Get your license first.")
else:
    print("Invalid input.")
```

---

## 4. Common mistakes

### Forgetting the colon `:`
```python
if x > 5    # ❌ SyntaxError — colon missing
if x > 5:   # ✅
```

### Inconsistent indentation
```python
if x > 5:
print("big")   # ❌ IndentationError
```

Python expects consistent indentation. Use 4 spaces. Never mix tabs and spaces.

### Using `=` instead of `==`
```python
if x = 5:   # ❌ SyntaxError (in Python 3, assignment in if is illegal)
```

### Confusing `is` with `==`
```python
a = 256
b = 256
a is b   # True — but only because Python caches small integers!
# Never rely on this. Use == for value comparison.
```

### Over-nesting
Instead of:
```python
if condition:
    if other:
        do_something()
```
Prefer:
```python
if condition and other:
    do_something()
```

### Checking truthiness wrong
```python
if x == True:    # redundant — just use "if x:"
if len(lst) > 0: # redundant — just use "if lst:"
```

---

## 5. Exercises

1. **Even or odd** — Ask the user for a number. Print "Even" if it is
   divisible by 2, otherwise "Odd".

2. **Leap year** — Ask for a year. Print whether it is a leap year:
   - Divisible by 400 → leap year
   - Divisible by 100 → not a leap year
   - Divisible by 4 → leap year
   - Otherwise → not a leap year

3. **Password checker** — Set a password (hard-coded). Ask the user to guess.
   If correct, print "Access granted". If wrong, print "Access denied".

4. **Grade calculator** — Ask for a percentage (0–100). Print the letter grade
   (A: 90+, B: 80+, C: 70+, D: 60+, F: below 60).

5. **Number classifier** — Ask for a number. Classify it as:
   - "Positive and even" (if > 0 and divisible by 2)
   - "Positive and odd"
   - "Negative"
   - "Zero"

6. **Match/case calculator** — Write a simple calculator that takes two numbers
   and an operator (`+`, `-`, `*`, `/`) using `match`/`case`. Print the result.

7. **Ternary max** — Given two numbers, use a ternary expression to print the
   larger one.

---

## 6. Self-check questions

1. What is the syntax of an `if` statement? What character ends the condition
   line?
2. Why is indentation important in Python?
3. List all the falsy values in Python.
4. What is the difference between `in` and `is`?
5. When should you use `is None` instead of `== None`?
6. What does a ternary expression look like?
7. What does `match`/`case` do?
8. What does the `_` mean in a `case` block?
9. Can you have multiple `elif` blocks? Can you have more than one `else`?
10. What happens if no `if`/`elif` condition is `True` and there is no `else`?

---

## 7. What's next

Your programs can now make decisions. You know how to:
- Branch with `if`/`elif`/`else`
- Use truthiness to write concise conditions
- Check membership with `in` and identity with `is`
- Write compact ternary expressions
- Use `match`/`case` for pattern matching

In **Level 04** you will learn about **loops** — repeating actions with `for`
and `while`, controlling iteration with `break`/`continue`, and common loop
patterns.

Close this lesson and open `04-loops.md`.
