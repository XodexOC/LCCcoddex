# [05] Collections: Lists, Tuples, Sets, Dicts
> **Track:** Python · **Level:** 05 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

So far you have stored single values (one number, one string). Most real
programs work with *groups* of data — a list of students, a set of unique tags,
a dictionary mapping usernames to scores.

Python has four main **collection types** — each designed for a different job:

| Type | Ordered? | Mutable? | Duplicates? | Use case |
|---|---|---|---|---|
| `list` | ✅ | ✅ | Allowed | Ordered sequence of items |
| `tuple` | ✅ | ❌ | Allowed | Fixed sequence (coordinates, config) |
| `set` | ❌ | ✅ | ❌ unique | Membership tests, deduplication |
| `dict` | ✅ (3.7+) | ✅ | Unique keys | Key→value mappings |

In this lesson you will learn:
- **Lists**: creating, indexing, methods, **list comprehensions**
- **Tuples**: immutability, unpacking, when to use them
- **Sets**: union, intersection, difference
- **Dicts**: keys, values, items, methods, **dict comprehensions**
- How to choose the right collection for your data

---

## 2. Core concept

### 2.1 Sequences vs collections

- A **sequence** (list, tuple, string) has a defined order. You can access
  `items[2]` and get the third element.
- A **set** has *no* order. You cannot index into a set.
- A **dict** maps keys to values. Access by key, not by numeric index.

### 2.2 Mutability

- **Mutable** collections (list, set, dict) can be changed after creation.
- **Immutable** collections (tuple) cannot be changed — you must create a new
  one.

### 2.3 Comprehensions

A **comprehension** is a concise way to build a collection from an iterable.
Instead of a multi-line loop, you write one expressive line:

```python
squares = [x**2 for x in range(10)]   # list of 0, 1, 4, 9, ..., 81
```

Comprehensions exist for lists, sets, and dicts.

---

## 3. Step-by-step breakdown

### Step 1: Creating lists

```python
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
nested = [[1, 2], [3, 4]]    # list of lists
```

`list()` constructor:

```python
list("abc")        # ['a', 'b', 'c']
list(range(5))     # [0, 1, 2, 3, 4]
```

### Step 2: List indexing and slicing

Same as strings (Level 02):

```python
items = [10, 20, 30, 40, 50]
items[0]        # 10
items[-1]       # 50
items[1:4]      # [20, 30, 40]
items[::-1]     # [50, 40, 30, 20, 10]
```

Slicing returns a **new** list (shallow copy).

### Step 3: List methods

**Adding elements:**

```python
fruits = ["apple", "banana"]
fruits.append("cherry")         # ['apple', 'banana', 'cherry']
fruits.extend(["date", "elderberry"])  # ['apple', 'banana', 'cherry', 'date', 'elderberry']
fruits.insert(0, "apricot")     # ['apricot', 'apple', 'banana', 'cherry', 'date', 'elderberry']
```

**Removing elements:**

```python
fruits.remove("banana")         # removes first occurrence — ValueError if not found
popped = fruits.pop()           # removes and returns last item
popped = fruits.pop(0)          # removes and returns item at index 0
fruits.clear()                  # [] — removes everything
```

**Finding and sorting:**

```python
nums = [4, 2, 8, 1, 9, 2]
nums.index(8)                   # 2 (first occurrence)
nums.count(2)                   # 2
nums.sort()                     # in-place sort → [1, 2, 2, 4, 8, 9]
nums.reverse()                  # in-place reverse → [9, 8, 4, 2, 2, 1]
```

`sorted()` returns a new list without modifying the original:

```python
sorted([3, 1, 2])    # [1, 2, 3]
```

### Step 4: List comprehensions

**Basic syntax:**
```python
[expression for item in iterable if condition]
```

**Examples:**

```python
# Squares
[x**2 for x in range(10)]        # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Only evens
[x for x in range(20) if x % 2 == 0]  # [0, 2, 4, ..., 18]

# Nested
[x*y for x in range(1, 4) for y in range(1, 4)]  # [1, 2, 3, 2, 4, 6, 3, 6, 9]
```

**List comprehension vs loop:**

```python
# Loop version
evens = []
for x in range(10):
    if x % 2 == 0:
        evens.append(x)

# Comprehension (same result, one line)
evens = [x for x in range(10) if x % 2 == 0]
```

### Step 5: Tuples

```python
empty = ()
point = (3, 5)
single = (1,)               # trailing comma required for one-element tuple
no_parens = 1, 2, 3          # also a tuple — parentheses are optional
```

**Indexing and slicing** work the same as lists.

**Immutability:**

```python
point = (3, 5)
point[0] = 10    # ❌ TypeError: 'tuple' object does not support item assignment
```

**Tuple unpacking:**

```python
point = (3, 5)
x, y = point        # x=3, y=5
a, b, c = (1, 2, 3)  # a=1, b=2, c=3
```

Swapping two variables the Pythonic way:

```python
a, b = b, a         # uses tuple packing/unpacking
```

**When to use tuples:**
- Fixed data that should not change (coordinates, RGB colors, config)
- Dictionary keys (lists cannot be dict keys, tuples can)
- Multiple return values from a function

### Step 6: Sets

Sets store **unique**, **unordered** elements.

```python
empty = set()               # {} creates an empty dict, not set!
fruits = {"apple", "banana", "cherry", "apple"}  # {'apple', 'banana', 'cherry'}
```

**Set methods:**

```python
fruits.add("date")          # {'apple', 'banana', 'cherry', 'date'}
fruits.remove("banana")     # KeyError if not found
fruits.discard("banana")    # no error if not found
popped = fruits.pop()       # removes and returns an arbitrary element
fruits.clear()              # empty set
```

**Set operations:**

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b    # union:        {1, 2, 3, 4, 5, 6}
a & b    # intersection: {3, 4}
a - b    # difference:   {1, 2}
b - a    # difference:   {5, 6}
a ^ b    # symmetric difference: {1, 2, 5, 6}
```

**Set comprehensions:**

```python
{x**2 for x in range(10) if x % 2 == 0}   # {0, 4, 16, 36, 64}
```

### Step 7: Dicts

```python
empty = {}
person = {"name": "Alice", "age": 30, "city": "New York"}
```

**Accessing values:**

```python
person["name"]          # 'Alice'
person.get("name")      # 'Alice'
person.get("salary")    # None — no error
person.get("salary", 0) # 0 — default value
person["salary"]        # ❌ KeyError
```

**Adding/updating:**

```python
person["email"] = "alice@example.com"     # new key
person["age"] = 31                         # update existing
```

**Checking keys:**

```python
"name" in person        # True
"salary" in person      # False
```

### Step 8: Dict methods

```python
person.keys()     # dict_keys(['name', 'age', 'city'])
person.values()   # dict_values(['Alice', 30, 'New York'])
person.items()    # dict_items([('name', 'Alice'), ('age', 30), ('city', 'New York')])
```

Looping:

```python
for key in person:
    print(key, person[key])

for key, value in person.items():
    print(f"{key}: {value}")
```

**Removing:**

```python
removed = person.pop("age")       # removes and returns value
del person["city"]                # removes key — KeyError if missing
person.clear()                    # {}
```

### Step 9: Dict comprehensions

```python
{x: x**2 for x in range(5)}          # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Swap keys and values
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}  # {1: 'a', 2: 'b', 3: 'c'}
```

### Step 10: When to use which collection

| Situation | Collection |
|---|---|
| You need to keep items in order | `list` |
| You need to modify items (add/remove) | `list` or `set` |
| You need fast membership checking | `set` |
| You need to eliminate duplicates | `set` |
| You need to map keys to values | `dict` |
| Data should never change after creation | `tuple` |
| You need a dict key that is a collection | `tuple` (list won't work) |
| You need ordered unique items | `list` + manual dedup (or dict) |

---

## 4. Common mistakes

### Using `{}` for an empty set
```python
s = {}          # ❌ dict, not set!
s = set()       # ✅ correct
```

### Forgetting lists are mutable
```python
a = [1, 2, 3]
b = a           # b and a are the SAME list
b.append(4)     # mutates a too!
print(a)        # [1, 2, 3, 4]
```
Use `b = a.copy()` or `b = a[:]` for a real copy.

### Using mutable objects as dict keys
```python
d = {}
d[[1, 2]] = "value"   # ❌ TypeError: unhashable type: 'list'
# Use tuple instead: d[(1, 2)]
```

### Confusing `remove()` and `pop()`
- `remove(x)` removes **by value** (first occurrence).
- `pop(i)` removes **by index** (default last).

### Modifying a list while iterating
```python
nums = [1, 2, 3, 4, 5]
for n in nums:
    if n % 2 == 0:
        nums.remove(n)   # ❌ elements shift, iteration skips
```
Iterate over a copy: `for n in nums[:]:`

### Using `=` instead of `==` in comprehensions
```python
[x = x*2 for x in range(5)]   # ❌ SyntaxError — can't assign in comprehension
```

---

## 5. Exercises

1. **List operations** — Start with `numbers = [3, 1, 4, 1, 5, 9, 2, 6]`.
   Do each in sequence:
   - Append 5
   - Insert 0 at position 0
   - Remove the first 1
   - Sort descending
   - Print the list

2. **List comprehension** — Given `words = ["hello", "world", "python", "is", "fun"]`,
   use a comprehension to create a new list with word lengths. Then create a
   list of words longer than 3 characters.

3. **Tuple unpacking** — Given `points = [(1, 2), (3, 4), (5, 6)]`, loop over
   the list and print each point's x and y coordinates separately.

4. **Set operations** — Given `all_students = {"Alice", "Bob", "Charlie", "Diana"}`
   and `present = {"Bob", "Diana", "Eve"}`, print:
   - Students present (intersection)
   - Students absent (difference)
   - All unique students (union)

5. **Word frequency** — Given a sentence, use a dict to count how many times
   each word appears. Print the result.

6. **Dict comprehension** — Given `names = ["Alice", "Bob", "Charlie"]`, create
   a dict mapping each name to its length. Print it.

7. **Shopping cart** — Create a dict where keys are item names and values are
   prices. Add three items. Calculate and print the total price.

8. **Filter a dict** — Given `scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 95}`,
   use a dict comprehension to keep only students with a score ≥ 90.

---

## 6. Self-check questions

1. What is the main difference between a list and a tuple?
2. Can a set contain duplicate elements?
3. How do you create an empty set? Why not `{}`?
4. What does `dict.items()` return?
5. What is a list comprehension?
6. How do you make a copy of a list (instead of referencing the same list)?
7. What happens if you access a dict key that doesn't exist without `.get()`?
8. Can a list be a dict key? Why or why not?
9. What does `set_a | set_b` compute?
10. When would you use a tuple instead of a list?

---

## 7. What's next

You now have the four essential Python collections at your command. You know:
- Lists: `append`, `extend`, `remove`, `pop`, `sort`, list comprehensions
- Tuples: immutability, unpacking
- Sets: `add`, `remove`, `|`, `&`, `-`, set comprehensions
- Dicts: `keys()`, `values()`, `items()`, `.get()`, dict comprehensions
- How to choose the right collection for the job

In **Level 06** you will learn about **functions** — defining reusable blocks
of code with `def`, parameters, return values, scope, lambda, and docstrings.

Close this lesson and open `06-functions.md`.
