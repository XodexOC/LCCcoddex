# [02] Strings in Depth & User Input
> **Track:** Python · **Level:** 02 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Level 01 introduced strings, but real programs do far more with text —
extracting parts of a string, cleaning up user input, formatting output,
embedding variables inside text. You also need to accept input from the person
using your program, not just hard-code values.

In this lesson you will learn:
- **Indexing** and **slicing** to access any part of a string
- Powerful **string methods** like `.upper()`, `.split()`, `.join()`
- **f-strings** — the best way to embed variables in text
- The `input()` function to get keyboard input
- Converting strings to numbers with `int()` and `float()`
- **Escape sequences** for special characters
- **Multi-line strings** with triple quotes

---

## 2. Core concept

### 2.1 Strings are sequences

A string is an **ordered sequence of characters**. Because it is ordered, you
can ask for "the character at position 3" or "the characters from position 1
to 5".

### 2.2 Indexing

Each character has a position (index). Python uses **zero-based indexing**:
the first character is at index 0.

```
String:  P  y  t  h  o  n
Index:   0  1  2  3  4  5
```

Negative indices count from the end:
```
String:  P   y   t   h   o   n
Index:  -6  -5  -4  -3  -2  -1
```

### 2.3 Slicing

Slicing extracts a **substring** (a contiguous piece) using the syntax
`string[start:stop:step]`.

- `start` — first index to include (inclusive)
- `stop` — first index to *exclude* (exclusive)
- `step` — stride between characters

All three are optional. If omitted:
- `start` defaults to `0`
- `stop` defaults to the end of the string
- `step` defaults to `1`

### 2.4 f-strings

Introduced in Python 3.6, **f-strings** (formatted string literals) let you
embed expressions directly inside a string. Put an `f` before the opening quote
and use `{ }` for expressions:

```python
name = "Xodex"
version = 1.0
print(f"Welcome to {name} v{version}")
```

### 2.5 `input()`

The `input()` function pauses the program and waits for the user to type
something and press Enter. Whatever the user types is returned as a **string**.

```python
name = input("Enter your name: ")
```

**Crucial:** `input()` always returns a string. If you ask for a number, you
must convert it with `int()` or `float()`.

---

## 3. Step-by-step breakdown

### Step 1: Indexing

```python
>>> word = "Python"
>>> word[0]     # 'P'
>>> word[3]     # 'h'
>>> word[-1]    # 'n' (last character)
>>> word[-2]    # 'o' (second to last)
```

Trying to access an index that does not exist raises an error:

```python
>>> word[100]   # IndexError: string index out of range
```

### Step 2: Slicing

```python
>>> text = "Hello, Python!"
>>> text[0:5]       # 'Hello' (indices 0,1,2,3,4 — 5 is excluded)
>>> text[7:13]      # 'Python'
>>> text[:5]        # 'Hello' (start defaults to 0)
>>> text[7:]        # 'Python!' (stop defaults to end)
>>> text[:]         # 'Hello, Python!' (full copy)
```

**Step parameter:**

```python
>>> text[::2]       # 'Hlo yhn' (every second character)
>>> text[::-1]      # '!nohtyP ,olleH' (reversed!)
>>> text[::3]       # 'Hl yh'
```

### Step 3: String methods

Methods are like functions that belong to an object. Call them with the dot
notation: `string.method()`.

**Case conversion:**

```python
>>> "hello".upper()           # 'HELLO'
>>> "HELLO".lower()           # 'hello'
>>> "hello world".title()     # 'Hello World'
>>> "hello".capitalize()      # 'Hello'
>>> "hElLo".swapcase()        # 'HeLlO'
```

**Removing whitespace:**

```python
>>> "  hello  ".strip()       # 'hello' (removes both ends)
>>> "  hello  ".lstrip()      # 'hello  ' (left only)
>>> "  hello  ".rstrip()      # '  hello' (right only)
```

**Splitting and joining:**

```python
>>> "a,b,c".split(",")        # ['a', 'b', 'c']
>>> "one two three".split()   # ['one', 'two', 'three'] (splits on any whitespace)
>>> ", ".join(["a", "b", "c"]) # 'a, b, c'
>>> "".join(["H", "e", "y"])  # 'Hey'
```

**Searching and replacing:**

```python
>>> "hello world".find("world")   # 6 (index where 'world' starts)
>>> "hello world".find("xyz")     # -1 (not found)
>>> "hello world".replace("world", "Python")  # 'hello Python'
>>> "hello".startswith("he")      # True
>>> "hello".endswith("lo")        # True
>>> "hello".count("l")            # 2
```

**Checking content:**

```python
>>> "abc123".isalpha()      # False (has digits)
>>> "abc".isalpha()         # True
>>> "123".isdigit()         # True
>>> "hello".islower()       # True
>>> "HELLO".isupper()       # True
>>> "   ".isspace()         # True
```

### Step 4: f-strings

```python
>>> name = "Xodex"
>>> year = 2026
>>> print(f"{name} was founded in {year}.")
Xodex was founded in 2026.
```

Expressions inside `{}` are evaluated:

```python
>>> a, b = 10, 3
>>> print(f"{a} / {b} = {a / b:.2f}")   # 10 / 3 = 3.33
```

The `:.2f` after the expression is a **format specifier** — it rounds the float
to 2 decimal places.

More format specifiers:

```python
>>> pi = 3.14159265
>>> f"{pi:.2f}"       # '3.14'
>>> f"{pi:10.2f}"     # '      3.14' (right-aligned in width 10)
>>> f"{pi:<10.2f}"    # '3.14      ' (left-aligned)
>>> f"{pi:^10.2f}"    # '   3.14   ' (centered)
>>> f"{1000000:,}"    # '1,000,000' (comma separator)
```

### Step 5: The `input()` function

```python
>>> name = input("What is your name? ")
What is your name? Max
>>> print(f"Hello, {name}!")
Hello, Max!
```

`input()` always returns a string. If you need a number, convert it:

```python
>>> age_str = input("How old are you? ")
>>> age = int(age_str)          # convert to int
>>> next_year = age + 1
>>> print(f"Next year you will be {next_year}.")
```

Or chain in one line:

```python
>>> age = int(input("How old are you? "))
```

### Step 6: Converting strings to numbers

```python
>>> int("42")       # 42
>>> float("3.14")   # 3.14
>>> int("3.14")     # ❌ ValueError — "3.14" is not a valid integer
>>> float("42")     # 42.0 (float accepts integer strings)
```

Always validate user input — if the user types "abc" and you call `int("abc")`,
the program crashes with a `ValueError`. You'll learn how to handle this in
Level 07.

### Step 7: Escape sequences

Some characters are hard to type inside a string. **Escape sequences** start
with a backslash `\` and represent special characters.

| Sequence | Meaning | Example |
|---|---|---|
| `\n` | Newline | `"line1\nline2"` |
| `\t` | Tab | `"col1\tcol2"` |
| `\\` | Backslash | `"path\\to\\file"` |
| `\'` | Single quote | `'it\'s'` |
| `\"` | Double quote | `"say \"hi\""` |

```python
>>> print("Hello\nWorld")
Hello
World
>>> print("1\t2\t3")
1	2	3
>>> print("C:\\Users\\Xodex")
C:\Users\Xodex
```

### Step 8: Raw strings

Prefix with `r` to ignore escape sequences (useful for file paths and regex):

```python
>>> print(r"C:\Users\Xodex")    # C:\Users\Xodex (no double-backslash needed)
```

### Step 9: Multi-line strings with `"""`

Use triple quotes for long text spanning multiple lines:

```python
message = """This is a
multi-line string
in Python."""
print(message)
```

Output:
```
This is a
multi-line string
in Python.
```

### Step 10: Immutability

Strings are **immutable** — you cannot change a character in place:

```python
>>> word = "Python"
>>> word[0] = "J"   # ❌ TypeError: 'str' object does not support item assignment
```

You must create a new string:

```python
>>> word = "J" + word[1:]   # 'Jython'
```

---

## 4. Common mistakes

### Off-by-one errors in slicing
```python
text = "hello"
text[0:4]       # 'hell' — not 'hello'! Stop index is exclusive.
```

### Forgetting `input()` returns a string
```python
age = input("Age: ")
print(age + 1)      # ❌ TypeError — age is a string
```

### Confusing `.split()` and `.join()`
```python
", ".join("hello")        # 'h, e, l, l, o' — splits the string!
", ".join(["hello"])      # 'hello' — correct usage with list
```

### Modifying a string in place
```python
s = "hello"
s[0] = "H"  # ❌ TypeError — strings are immutable
```

### Mixing up `find()` return value
```python
if "hello".find("xyz"):       # ❌ wrong — returns -1, which is truthy!
    print("found")
if "hello".find("xyz") != -1: # ✅ correct
    print("found")
```

---

## 5. Exercises

1. **Slicing practice** — Given `s = "abcdefghij"`, extract:
   - First 3 characters
   - Last 3 characters
   - Characters from index 2 to 6
   - Every other character
   - The string reversed

2. **Username generator** — Ask the user for their first and last name.
   Generate a username: first 3 letters of first name + first 4 letters of
   last name, all lowercase. Print it.

3. **Sentence statistics** — Ask for a sentence. Print:
   - Number of characters (including spaces)
   - Number of words (split by space)
   - The sentence in uppercase
   - The sentence with "bad" replaced by "good"

4. **Formatted table** — Create variables: `name`, `age`, `city`. Use f-strings
   to print a neat table:
   ```
   Name   : Alice
   Age    : 30
   City   : New York
   ```

5. **Multi-line poem** — Write a program that stores a short poem in a
   multi-line string and prints it.

6. **CSV-like line** — Given `"apple,banana,grape,orange"`, use `.split()` to
   split it, then use `.join()` to rejoin with ` | ` between items. Print
   the result.

---

## 6. Self-check questions

1. What is the index of the first character in a string?
2. What does `s[::-1]` do?
3. What does `.strip()` remove from a string?
4. Why is `input()` always returning a string problematic when you want a
   number? How do you fix it?
5. What does `" ".join(["a", "b", "c"])` return?
6. What is an f-string and why is it better than `+` for combining text?
7. What escape sequence produces a newline?
8. Are strings mutable or immutable?
9. What does `.find()` return when the substring is not found?
10. What does `r"C:\new"` print?

---

## 7. What's next

You can now manipulate strings with precision — slice them, clean them, format
them, and accept user input. You know:
- Indexing and slicing with `[start:stop:step]`
- Common string methods: `.split()`, `.join()`, `.replace()`, `.find()`
- f-strings for embedding variables and formatting
- `input()` for reading keyboard input
- Converting strings to numbers
- Escape sequences and raw strings

In **Level 03** you will learn how to make decisions in your code using
`if`/`elif`/`else`, truthiness, membership testing, and the powerful
`match`/`case` statement.

Close this lesson and open `03-conditionals.md`.
