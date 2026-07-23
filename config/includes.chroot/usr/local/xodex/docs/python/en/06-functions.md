# [06] Functions
> **Track:** Python · **Level:** 06 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

As programs get larger, you find yourself repeating the same calculation over
and over. Copy-pasting code is error-prone — fix a bug in one place and miss
the three other copies.

**Functions** let you package a reusable block of code under a name. Write it
once, call it anywhere. This is the foundation of organized, maintainable
programming.

In this lesson you will learn:
- `def` and `return` — defining and returning from functions
- The difference between **parameters** and **arguments**
- **Default parameter values**
- **Keyword arguments** — explicitly naming arguments
- `*args` and `**kwargs` — handling variable numbers of arguments
- **Scope** — where variables live (LEGB rule)
- **Lambda functions** — anonymous one-liners
- Functions as **first-class objects**
- **Docstrings** — documenting your functions
- **Type hints** — declaring expected types

---

## 2. Core concept

### 2.1 What is a function?

A function is a named block of code that:
1. **Takes input** (parameters)
2. **Does work** (the body)
3. **Returns output** (return value)

```python
def add(x, y):
    return x + y
```

- `def` is the keyword that defines a function.
- `add` is the function name.
- `x` and `y` are **parameters** (placeholders).
- `return x + y` sends the result back to the caller.

### 2.2 Parameters vs arguments

- **Parameter**: the variable name in the function definition (`x`, `y`).
- **Argument**: the actual value you pass when calling (`5`, `3`).

```python
add(5, 3)   # 5 and 3 are arguments → parameters x=5, y=3
```

### 2.3 Scope

**Scope** defines where a variable is accessible. Python uses the **LEGB**
rule to look up variables:

1. **L**ocal — inside the current function
2. **E**nclosing — outer functions (nested functions)
3. **G**lobal — top-level of the module
4. **B**uilt-in — Python's built-in names (`print`, `len`, etc.)

Variables defined inside a function are not visible outside it.

---

## 3. Step-by-step breakdown

### Step 1: Defining and calling a function

```python
def greet():
    print("Hello, world!")

greet()   # Hello, world!
```

### Step 2: Parameters and return

```python
def add(x, y):
    result = x + y
    return result

sum = add(3, 5)
print(sum)   # 8
```

A function without `return` implicitly returns `None`:

```python
def nothing():
    pass

result = nothing()
print(result)   # None
```

### Step 3: Multiple return values

Python functions can return multiple values as a tuple:

```python
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 7, 2, 9])
print(low, high)   # 1 9
```

### Step 4: Default parameter values

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))            # Hello, Alice!
print(greet("Bob", "Hi"))        # Hi, Bob!
print(greet("Charlie", "Hey"))   # Hey, Charlie!
```

**Important:** default values are evaluated **once** at definition time. Never
use a mutable default like `[]` or `{}`:

```python
def bad(item, items=[]):     # ❌ items is shared across all calls!
    items.append(item)
    return items

print(bad(1))   # [1]
print(bad(2))   # [1, 2] — not [2]!

def good(item, items=None):  # ✅ correct pattern
    if items is None:
        items = []
    items.append(item)
    return items
```

### Step 5: Keyword arguments

You can pass arguments by name, in any order:

```python
def create_profile(name, age, city):
    return f"{name}, {age}, {city}"

print(create_profile(age=30, name="Alice", city="NYC"))
```

Mix positional and keyword, but positional must come first:

```python
create_profile("Alice", city="NYC", age=30)   # ✅
create_profile(name="Alice", 30, "NYC")        # ❌ SyntaxError
```

### Step 6: `*args` — variable positional arguments

The `*` prefix collects extra positional arguments into a tuple:

```python
def sum_all(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

print(sum_all(1, 2, 3))       # 6
print(sum_all(1, 2, 3, 4, 5)) # 15
```

You can have regular parameters before `*args`:

```python
def greet(greeting, *names):
    for name in names:
        print(f"{greeting}, {name}!")

greet("Hello", "Alice", "Bob", "Charlie")
```

### Step 7: `**kwargs` — variable keyword arguments

The `**` prefix collects extra keyword arguments into a dict:

```python
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="NYC")
```

### Step 8: Scope — LEGB rule

```python
x = "global"     # global variable

def outer():
    x = "enclosing"   # enclosing variable

    def inner():
        x = "local"   # local variable
        print(x)

    inner()   # prints "local"
    print(x)  # prints "enclosing"

outer()
print(x)      # prints "global"
```

**Modifying global variables:**

```python
count = 0

def increment():
    global count   # you must declare it global to modify
    count += 1
```

Avoid globals when possible. Pass parameters instead.

### Step 9: Lambda functions

A **lambda** is a small anonymous function defined in one expression:

```python
square = lambda x: x ** 2
print(square(5))   # 25
```

Lambdas are most useful as short callbacks:

```python
pairs = [(1, "one"), (3, "three"), (2, "two")]
pairs.sort(key=lambda pair: pair[0])   # sort by number
print(pairs)   # [(1, 'one'), (2, 'two'), (3, 'three')]
```

```python
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

Lambda body must be a single expression — no `if`/`elif`/`else` statements
(though you can use a ternary).

### Step 10: Functions as first-class objects

In Python, functions are values just like integers or strings. You can:
- Assign them to variables
- Pass them as arguments
- Return them from other functions

```python
def say_hello():
    return "Hello"

def say_bye():
    return "Bye"

def repeat(func, times):
    return [func() for _ in range(times)]

print(repeat(say_hello, 3))   # ['Hello', 'Hello', 'Hello']
```

**Functions that return functions (closures):**

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```

### Step 11: Docstrings

A **docstring** documents what a function does. Write it as the first statement
inside the function body, using triple quotes:

```python
def calculate_area(radius):
    """Return the area of a circle given its radius."""
    return 3.14159 * radius ** 2
```

Multi-line docstrings:

```python
def calculate_area(radius):
    """
    Return the area of a circle given its radius.

    Args:
        radius: The radius of the circle (float or int).

    Returns:
        The area as a float.
    """
    return 3.14159 * radius ** 2
```

Access the docstring with `help(calculate_area)` or `print(calculate_area.__doc__)`.

### Step 12: Type hints

Type hints (Python 3.5+) indicate expected types. They are **not enforced** at
runtime — they help tools (IDEs, linters) and other humans.

```python
def add(x: int, y: int) -> int:
    return x + y

def greet(name: str, age: int) -> str:
    return f"{name} is {age} years old."
```

For collections:

```python
from typing import List, Dict, Optional

def process(items: List[int]) -> Dict[str, int]:
    return {"sum": sum(items), "count": len(items)}

def find_user(uid: int) -> Optional[str]:
    # returns str or None
    ...
```

---

## 4. Common mistakes

### Forgetting `return`
```python
def add(x, y):
    x + y          # ❌ no return — result is None

result = add(3, 5)
print(result)      # None
```

### Modifying a mutable default argument
```python
def append_to(item, lst=[]):   # ❌ default list is shared
    lst.append(item)
    return lst
```
Use `None` as the default and create a new list inside.

### Confusing `return` and `print`
`return` sends a value back to the caller. `print` shows text on the screen.
They are not interchangeable.

### Using global variables when parameters suffice
```python
total = 0
def add_to_total(x):
    global total   # avoid this pattern
    total += x
```
Better: pass `total` as parameter and return the new value.

### Shadowing built-in names
```python
list = [1, 2, 3]   # ❌ now you can't use list() anymore!
```

### Argument order with positional + keyword
```python
def f(a, b, c): ...
f(1, c=3, 2)   # ❌ positional arg after keyword
```

---

## 5. Exercises

1. **Basic function** — Write a function `is_even(n)` that returns `True` if
   `n` is even, `False` otherwise.

2. **Default values** — Write `power(base, exponent=2)` that returns
   `base ** exponent`. Call it with one argument and with two.

3. **`*args`** — Write `average(*numbers)` that returns the mean of any number
   of arguments. Test it with `average(1, 2, 3)` and `average(10, 20)`.

4. **`**kwargs`** — Write `build_profile(first, last, **info)` that returns a
   dict with `first_name`, `last_name`, and any additional keys from `info`.

5. **Scopes** — Write a function `outer(x)` that defines an inner function
   `inner(y)` that returns `x + y`. `outer` should return the inner function.
   Call `outer(5)(3)` — what do you get?

6. **Lambda** — Given `words = ["apple", "banana", "cherry", "date"]`, use
   `sorted()` with a `key=lambda` to sort by the last character of each word.

7. **Docstrings** — Write a function `factorial(n)` with a proper docstring.
   Use `help(factorial)` to verify it shows.

8. **Type hints** — Add type hints to all the functions above.

9. **Palindrome checker** — Write `is_palindrome(s: str) -> bool` that returns
   `True` if `s` reads the same forward and backward (ignoring case).

---

## 6. Self-check questions

1. What keyword defines a function in Python?
2. What is the difference between a parameter and an argument?
3. What does a function return if it has no `return` statement?
4. Why is using `[]` as a default parameter dangerous?
5. What is the difference between `*args` and `**kwargs`?
6. What does the LEGB rule describe?
7. What is a lambda? When would you use one?
8. Can you pass a function as an argument to another function?
9. What is a docstring and how do you create one?
10. Do type hints affect how the code runs?

---

## 7. What's next

You now understand functions — the building blocks of modular code. You know:
- `def`, `return`, parameters, arguments
- Default values, keyword arguments, `*args`, `**kwargs`
- LEGB scope rules
- Lambda functions and first-class functions
- Docstrings and type hints

In **Level 07** you will learn about **files and error handling** — reading
and writing files, working with CSV and JSON, and handling errors gracefully
with `try`/`except`.

Close this lesson and open `07-files-errors.md`.
