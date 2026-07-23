# [00] Hello, Python & the REPL
> **Track:** Python · **Level:** 00 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Computers only understand machine code — long sequences of 0s and 1s. Writing
software directly in machine code is brutally hard and takes forever. We need a
way to tell the computer what to do using language that looks closer to English.

That's what **Python** is for. Python is a *programming language* that lets you
write instructions in a readable way. Another program (the *interpreter*) then
translates your Python code into machine code so the computer can run it.

In this lesson you will:
- Learn what Python is and how it compares to other languages
- Open the Python **REPL** and use it as a calculator
- Store values in **variables**
- Write your first **Python script** (a `.py` file)
- Run your script from the terminal
- Add **comments** to explain your code

By the end you will have run Python code two different ways and written your
very first program. No prior experience needed.

---

## 2. Core concept

### 2.1 What is Python?

Python is a **high-level**, **interpreted** programming language.

- **High-level** means you write human-readable code instead of machine code.
- **Interpreted** means another program (the Python interpreter) reads your code
  and runs it line by line. You do **not** need a separate compilation step.

| Compiled language (C, Rust, Go) | Interpreted language (Python, JavaScript) |
|---|---|
| You write source code → you *compile* it into an executable → you run the executable | You write source code → you run it with the interpreter directly |
| Faster at runtime | Slower at runtime, but easier to write and test |

Python trades a little speed for huge gains in readability and speed of
development. For most programs that is exactly what you want.

### 2.2 What is the REPL?

REPL stands for **R**ead-**E**val-**P**rint **L**oop.

1. **Read** — it reads what you type.
2. **Eval** — it evaluates (runs) your code.
3. **Print** — it prints the result.
4. **Loop** — it goes back to step 1.

The REPL is great for experimenting. You type one line, Python runs it, you see
the result immediately. There is no faster way to learn.

### 2.3 What is a variable?

A **variable** is a named box that holds a value. Think of it like a sticky note
you put on a file cabinet drawer. The sticky note has a name ("bills"), and the
drawer holds the actual content ($200).

In Python:
```python
age = 25
```
- `age` is the name (the sticky note)
- `25` is the value (the content)
- `=` is the *assignment operator* — it binds the value to the name

You can then use the name wherever you want the value.

### 2.4 What is `print()`?

`print()` is a **function** — a reusable chunk of code that does something
useful. This particular function shows text on the screen.

```python
print("Hello, world!")
```

When Python runs this line it prints:
```
Hello, world!
```

The parentheses `()` tell Python to *call* (run) the function. Inside the
parentheses you put the *argument(s)* — the data the function needs.

### 2.5 Comments

A **comment** is text the interpreter ignores. In Python comments start with `#`.

```python
# This is a comment — Python won't run it
print("Hello")  # This part after the # is also a comment
```

Comments are for humans. They explain *why* the code exists, not *what* it does
(the code itself shows what it does). Use comments to explain tricky logic,
remind yourself why you made a choice, or temporarily disable a line.

---

## 3. Step-by-step breakdown

### Step 1: Open a terminal

On Linux / macOS:
```
Ctrl + Alt + T
```
or find "Terminal" in your applications menu.

On Windows you can use **Command Prompt** or **PowerShell**.

### Step 2: Start the Python REPL

Type `python3` and press Enter.

```bash
$ python3
Python 3.11.5 (main, ...)
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

The `>>>` prompt means Python is waiting for your command.

If `python3` does not work, try `python`.

### Step 3: Use the REPL as a calculator

Type an expression and press Enter. Python prints the result immediately.

```python
>>> 2 + 2
4
>>> 10 / 3
3.3333333333333335
>>> 2 ** 10
1024
>>> (5 + 3) * 2
16
```

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `9 - 4` | `5` |
| `*` | Multiplication | `3 * 4` | `12` |
| `/` | Division | `10 / 3` | `3.333...` |
| `**` | Exponentiation | `2 ** 10` | `1024` |

Every expression produces a value. Python evaluates the expression and prints
the result.

### Step 4: Create variables

```python
>>> x = 5
>>> x
5
>>> name = "Xodex"
>>> name
'Xodex'
>>> price = 19.99
>>> quantity = 3
>>> price * quantity
59.97
```

Variables let you store intermediate results and reuse them.

```python
>>> width = 10
>>> height = 5
>>> area = width * height
>>> area
50
```

### Step 5: Strings

Text values are called **strings**. You can use single quotes `'...'` or double
quotes `"..."`.

```python
>>> greeting = "Hello"
>>> language = 'Python'
>>> greeting + " " + language
'Hello Python'
```

### Step 6: Use `print()`

In the REPL, `print()` works the same as just typing the variable name, but
`print()` is needed when you run a `.py` file (see below).

```python
>>> print("Hello from print!")
Hello from print!
>>> name = "Xodex"
>>> print("Welcome to", name)
Welcome to Xodex
```

`print()` can take multiple arguments separated by commas. It adds a space
between them.

### Step 7: Create a `.py` file

Leave the REPL (press `Ctrl + D` or type `exit()`).

Open a text editor and write:

```python
# hello.py
print("Hello, world!")
name = "Xodex"
print("Welcome to", name)
```

Save the file as `hello.py`. The `.py` extension tells your system this is a
Python source file.

### Step 8: Run the `.py` file

In the terminal, navigate to where you saved `hello.py` and run:

```bash
$ python3 hello.py
Hello, world!
Welcome to Xodex
```

Python reads the whole file, runs every line from top to bottom, then exits.

### Step 9: More code in a file

Edit `hello.py` to add more lines:

```python
# This program calculates the area of a rectangle
width = 10
height = 5
area = width * height
print("The area is:")
print(area)
```

Run it again:

```bash
$ python3 hello.py
The area is:
50
```

### Step 10: Comments in depth

```python
# Single-line comment — ignored by Python

print("Visible")  # Inline comment — also ignored

"""
Multi-line string used as a comment.
Python still reads this but does nothing
with it unless you assign it to something.
"""
```

Use comments to:
- Explain *why* you wrote code a certain way
- Document assumptions ("this function expects positive numbers")
- Disable code temporarily (add `#` at the front of a line)

---

## 4. Common mistakes

### Forgetting quotation marks for strings
```python
print(Hello)           # ❌ NameError: name 'Hello' is not defined
print("Hello")         # ✅
```

### Using `=` instead of `==` for comparison
```python
if x = 5:   # ❌ SyntaxError
if x == 5:  # ✅
```

### Spaces in variable names
```python
my name = "Xodex"  # ❌ SyntaxError
my_name = "Xodex"  # ✅ (use underscore)
```

### Confusing Python 2 vs 3
```bash
$ python hello.py   # might be Python 2 on some systems
$ python3 hello.py  # explicitly Python 3 ✅
```

### Not saving the file before running
If you edit the `.py` file but forget to save, Python runs the old version.

### Using `print` in the REPL unnecessarily
In the REPL you can just type a variable name and see its value — no need for
`print()`. But `print()` is required in `.py` files.

---

## 5. Exercises

1. **Calculator in the REPL** — Open the REPL and compute:
   - `(12 + 34) * 5`
   - `100 / 7` (note the many decimal places)
   - `3 ** 3` (what do you expect?)

2. **Variables** — In the REPL, create a variable `minutes` set to `120`.
   Compute how many hours that is (`minutes / 60`). Store the result in a
   variable called `hours`.

3. **Your first script** — Write and run a `.py` file that:
   - Creates a variable `city` with your city's name
   - Creates a variable `temperature` with a number
   - Prints both in a sentence

4. **String concatenation** — In a file, create three variables `a`, `b`, `c`
   each containing a word. Print them all together in one sentence using `+`.

5. **Comments** — Write a short script that calculates how many seconds are in
   a day. Use comments to explain each step.

---

## 6. Self-check questions

1. What does REPL stand for?
2. What is the difference between an interpreted language and a compiled
   language?
3. How do you start the Python REPL from the terminal?
4. What character starts a comment in Python? Why are comments useful?
5. What is wrong with this variable name: `my age`?
6. Do you need `print()` in the REPL to see a variable's value? Do you need it
   in a `.py` file?
7. What file extension do Python scripts use?
8. What is the result of `2 ** 3`?
9. What happens if you forget the quotes around a string in `print()`?
10. How do you exit the REPL?

---

## 7. What's next

You have written your first Python code and run it both interactively (REPL)
and as a script. You know how to:
- Start and use the Python REPL as a calculator
- Create variables to store numbers and text
- Write a `.py` file and run it with `python3`
- Add comments to your code

In **Level 01** you will learn about Python's **data types** — the different
kinds of values Python can work with: integers, floats, strings, booleans, and
the special value `None`. You will also learn how to compare values and combine
conditions with logical operators.

Now close this lesson and open `01-types-operators.md`.
