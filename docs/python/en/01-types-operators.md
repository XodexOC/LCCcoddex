# [01] Data Types & Basic Operators
> **Track:** Python · **Level:** 01 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

In Level 00 you stored numbers and text in variables. But Python treats
different *kinds* of values differently. Adding two numbers is normal; adding
two strings glues them together; adding a number and a string causes an error.

You need to understand **data types** so you know what Python will do with your
data — and why errors happen when you mix incompatible types.

In this lesson you will learn:
- How to check the type of any value with `type()`
- The five fundamental data types: `int`, `float`, `str`, `bool`, `None`
- Arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- String operators: `+` (concatenation), `*` (repeat), `len()`
- Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Chained comparisons
- Logical operators: `and`, `or`, `not`

---

## 2. Core concept

### 2.1 Dynamic typing

Python is **dynamically typed**. You do not declare the type of a variable; the
interpreter infers it from the value you assign. A variable can even change type
during the program:

```python
x = 5       # x is int
x = "five"  # now x is str — perfectly legal in Python
```

Most languages (Java, C++, Rust) do not allow this. Dynamic typing makes Python
more flexible but also means you must keep track of types yourself.

### 2.2 The `type()` function

Pass any value to `type()` and it tells you what type it is:

```python
>>> type(5)
<class 'int'>
>>> type(3.14)
<class 'float'>
>>> type("hello")
<class 'str'>
>>> type(True)
<class 'bool'>
>>> type(None)
<class 'NoneType'>
```

### 2.3 The five basic data types

| Type | Name | Examples | Notes |
|---|---|---|---|
| `int` | Integer | `42`, `-7`, `2_000_000` | Whole numbers (no decimal) |
| `float` | Floating-point | `3.14`, `-0.001`, `1e6` | Decimal numbers; scientific notation |
| `str` | String | `"hi"`, `'bye'` | Text; any characters in quotes |
| `bool` | Boolean | `True`, `False` | Only two values |
| `NoneType` | None | `None` | Represents "nothing" or "no value" |

### 2.4 Operators

An **operator** is a symbol that performs an operation on one or more values
(called **operands**). `2 + 3` uses the `+` operator with operands `2` and `3`.

Python has operators for arithmetic, string work, comparison, and logic.

---

## 3. Step-by-step breakdown

### Step 1: Integers (`int`)

```python
>>> age = 25
>>> population = 8_000_000_000  # underscores ignored — improves readability
>>> temperature = -12
>>> type(age)
<class 'int'>
```

Integers have unlimited precision in Python. You can work with numbers that
are thousands of digits long.

### Step 2: Floats (`float`)

```python
>>> pi = 3.14159
>>> price = 19.99
>>> scientific = 1.5e-4       # 1.5 × 10⁻⁴ = 0.00015
>>> large = 1e6               # 1.0 × 10⁶ = 1_000_000.0
>>> type(pi)
<class 'float'>
```

Floats have limited precision (about 15–17 decimal digits). This can lead to
surprising results:

```python
>>> 0.1 + 0.2
0.30000000000000004  # not exactly 0.3!
```

This is a limitation of how computers store decimal numbers in binary — not a
bug in Python. For exact decimal arithmetic you would use the `decimal` module.

### Step 3: Arithmetic operators

```python
>>> 10 + 3      # addition → 13
>>> 10 - 3      # subtraction → 7
>>> 10 * 3      # multiplication → 30
>>> 10 / 3      # division → 3.3333... (always float)
>>> 10 // 3     # integer (floor) division → 3 (discards remainder)
>>> 10 % 3      # modulo (remainder) → 1
>>> 2 ** 3      # exponentiation → 8 (2 × 2 × 2)
```

Pay attention to `/` vs `//`:

| Expression | Result | Type |
|---|---|---|
| `10 / 3` | `3.3333333333333335` | `float` |
| `10 // 3` | `3` | `int` |
| `10.0 // 3` | `3.0` | `float` (both operands determine type) |

### Step 4: Strings (`str`)

```python
>>> single = 'Hello'
>>> double = "World"
>>> empty = ""
>>> space = " "
```

Use either single or double quotes — be consistent. Use the other kind when
your string contains a quote:

```python
>>> text = "It's a nice day"   # single quote inside double is fine
>>> text = 'It\'s a nice day'  # or escape with backslash
```

**Multiline strings** use triple quotes:

```python
>>> poem = """Roses are red,
... Violets are blue,
... Python is awesome,
... And so are you."""
```

### Step 5: String operators

```python
>>> "Hello" + " World"       # concatenation → "Hello World"
>>> "Ha" * 3                 # repetition → "HaHaHa"
>>> len("Python")             # length → 6
>>> len("")                   # empty string → 0
```

`+` with strings combines them. `*` repeats a string a given number of times.
`len()` returns the number of characters.

### Step 6: Booleans (`bool`)

Only two values:

```python
>>> is_active = True
>>> is_finished = False
>>> type(True)
<class 'bool'>
```

Booleans are the result of comparison operations:

```python
>>> 5 > 3
True
>>> 10 == 20
False
```

### Step 7: `None`

`None` represents the *absence* of a value — nothing, null, empty.

```python
>>> result = None
>>> print(result)
None
>>> type(None)
<class 'NoneType'>
```

Functions that do not explicitly return something return `None`:

```python
>>> x = print("hi")
hi
>>> print(x)
None
```

### Step 8: Comparison operators

```python
>>> 5 == 5     # equal → True
>>> 5 == 4     # equal → False
>>> 5 != 4     # not equal → True
>>> 5 < 10     # less than → True
>>> 5 > 10     # greater than → False
>>> 5 <= 5     # less than or equal → True
>>> 5 >= 3     # greater than or equal → True
```

**Comparisons with strings** use lexicographic (alphabetical) order:

```python
>>> "apple" < "banana"   # True (a comes before b)
>>> "apple" > "Apple"    # True in most cases (lowercase > uppercase in ASCII)
```

**Chained comparisons** let you check ranges concisely:

```python
>>> x = 15
>>> 10 < x < 20          # True: same as 10 < x and x < 20
>>> 5 < x < 10           # False
>>> 10 < x < 15          # False (x is 15, not less than 15)
```

### Step 9: Logical operators

`and`, `or`, `not` combine boolean values.

```python
>>> True and True    # True — both must be True
>>> True and False   # False
>>> True or False    # True — at least one must be True
>>> False or False   # False
>>> not True         # False
>>> not False        # True
```

Practical example:

```python
>>> age = 20
>>> has_license = True
>>> age >= 18 and has_license  # True — can drive
```

**Short-circuit evaluation:**
- `and` stops evaluating as soon as it sees `False`
- `or` stops evaluating as soon as it sees `True`

```python
>>> False and print("never runs")   # print is not called
>>> True or print("never runs")     # print is not called
```

### Step 10: Type conversion

Sometimes you need to explicitly convert between types:

```python
>>> int(3.9)        # → 3 (truncates, does not round)
>>> float(5)        # → 5.0
>>> str(42)         # → "42"
>>> bool(1)         # → True
>>> bool(0)         # → False
>>> bool("")        # → False
>>> bool("text")    # → True
```

---

## 4. Common mistakes

### Dividing integers expecting integer result
```python
>>> 10 / 3
3.3333333333333335  # use // for integer division
```

### Confusing `=` (assignment) with `==` (equality)
```python
if x = 5:    # ❌ SyntaxError
if x == 5:   # ✅ correct comparison
```

### Mixing types with `+`
```python
>>> "Age: " + 25       # ❌ TypeError: can only concatenate str (not "int") to str
>>> "Age: " + str(25)  # ✅ "Age: 25"
```

### Floating-point precision surprises
```python
>>> 0.1 + 0.2 == 0.3  # False — because of binary representation
```

### Forgetting parentheses with operators
```python
>>> 5 + 3 * 2   # → 11 (multiplication has higher precedence)
>>> (5 + 3) * 2 # → 16 — use parens when in doubt
```

---

## 5. Exercises

1. **Type detective** — In the REPL, find the type of each:
   - `42`
   - `3.14`
   - `"42"`
   - `True`
   - `None`
   - `"True"`

2. **Geometry** — Write a script that computes the area of a circle. Use
   `radius = 5` and `pi = 3.14159`. Area formula: `π × r²`. Print the result.

3. **Temperatures** — Convert 100°F to Celsius and back. Formula:
   `C = (F - 32) × 5/9`. Print both values.

4. **String art** — Use `*` to print a triangle made of `"*"`:
   ```
   *
   **
   ***
   ```
   Hint: `"*" * 1`, `"*" * 2`, etc.

5. **Truth table** — Write a script that prints all four combinations of
   `True`/`False` with `and` and `or`. Example output:
   ```
   True and True = True
   True and False = False
   ...
   ```

6. **Chained comparison** — Pick a number. Write an expression that checks if
   it is between 10 and 50 (inclusive). Print the result.

---

## 6. Self-check questions

1. What does `type()` do?
2. What is the difference between `/` and `//`?
3. Why is `0.1 + 0.2` not exactly `0.3`?
4. What does `"ab" * 3` produce?
5. What does `len("")` return?
6. What is the difference between `=` and `==`?
7. What is the result of `not (True and False)`?
8. What does `int(3.99)` return?
9. What is short-circuit evaluation?
10. What happens if you write `"hello" + 5`? How do you fix it?

---

## 7. What's next

You now understand Python's core data types, arithmetic, string operators,
comparisons, and logical operators. You can:
- Check the type of any value with `type()`
- Use integers, floats, strings, booleans, and `None`
- Perform arithmetic with `+`, `-`, `*`, `/`, `//`, `%`, `**`
- Concatenate and repeat strings, find their length
- Compare values and chain comparisons
- Combine conditions with `and`, `or`, `not`

In **Level 02** you will dive deeper into **strings**: indexing, slicing,
powerful methods, f-strings, user input with `input()`, and escape sequences.

Close this lesson and open `02-strings-input.md`.
