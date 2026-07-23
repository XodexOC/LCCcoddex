# [09] Object-Oriented Programming
> **Track:** Python · **Level:** 09 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

So far our code is built from functions operating on data structures. For simple
programs that is fine. But as complexity grows, you want to bundle **data** and
**behavior** together. If you are modeling a bank account, you want the balance
and the deposit/withdraw logic in one place.

**Object-Oriented Programming (OOP)** lets you define your own types
(classes). Each **object** (instance) has its own data and can perform actions
(methods). This keeps related code together and makes large projects easier to
reason about.

In this lesson you will learn:
- `class` and `__init__` — defining and initializing objects
- The `self` parameter — how methods access the instance
- **Instance variables** vs **class variables**
- **Instance methods**, **class methods** (`@classmethod`), **static methods**
  (`@staticmethod`)
- **Inheritance** — one class extending another
- **`super()`** — calling the parent class
- **`@property`** — computed attributes that look like plain attributes
- **Dunder methods** — `__str__`, `__repr__`, `__eq__`, `__len__`
- **`@dataclass`** — auto-generating boilerplate
- **Composition** vs **inheritance**

---

## 2. Core concept

### 2.1 Class vs instance

- A **class** is a blueprint (a template).
- An **instance** (object) is a concrete copy built from the blueprint.

```python
class Dog:
    pass

my_dog = Dog()      # my_dog is an instance of Dog
```

### 2.2 `__init__` — the constructor

`__init__` is a special method that runs automatically when you create an
instance. It initializes the object's data.

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

### 2.3 The `self` parameter

The first parameter of every instance method is `self`. It refers to the
current instance. When you call `my_dog.bark()`, Python automatically passes
`my_dog` as `self` — you do not pass it explicitly.

### 2.4 Encapsulation

OOP bundles data (attributes) and behavior (methods) together. Good practice:
expose a clean public interface and keep internal details private.

---

## 3. Step-by-step breakdown

### Step 1: Defining a simple class

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def introduce(self):
        return f"Hi, I'm {self.name} and I'm in grade {self.grade}."

alice = Student("Alice", 10)
print(alice.introduce())   # Hi, I'm Alice and I'm in grade 10.
```

### Step 2: Instance vs class variables

- **Instance variable** — unique to each object (set via `self`).
- **Class variable** — shared across all instances (set on the class itself).

```python
class Dog:
    species = "Canis familiaris"        # class variable

    def __init__(self, name, age):
        self.name = name                # instance variable
        self.age = age                  # instance variable

d1 = Dog("Rex", 5)
d2 = Dog("Fido", 3)

print(d1.species)    # Canis familiaris
print(d2.species)    # Canis familiaris
print(Dog.species)   # Canis familiaris

Dog.species = "Canis lupus"
print(d1.species)    # Canis lupus
```

### Step 3: Instance methods

Regular methods that operate on an instance (receive `self`):

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, amount=1):
        self.count += amount

    def reset(self):
        self.count = 0

c = Counter()
c.increment()
c.increment(5)
print(c.count)   # 6
```

### Step 4: Class methods (`@classmethod`)

Class methods operate on the class itself, not on an instance. They receive
`cls` instead of `self`. Use them for alternative constructors or operations
that affect the whole class.

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_str):
        """Alternative constructor: parse '2026-07-23'"""
        parts = date_str.split("-")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))

d = Date.from_string("2026-07-23")
print(d.year, d.month, d.day)   # 2026 7 23
```

### Step 5: Static methods (`@staticmethod`)

Static methods belong to the class's namespace but receive no special first
parameter. They are just regular functions grouped inside a class.

```python
class MathUtils:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

    @staticmethod
    def is_odd(n):
        return n % 2 != 0

print(MathUtils.is_even(4))   # True
print(MathUtils.is_odd(4))    # False
```

### Step 6: Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound."

class Dog(Animal):           # Dog inherits from Animal
    def speak(self):         # override the parent method
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

animals = [Dog("Rex"), Cat("Whiskers"), Animal("Generic")]
for a in animals:
    print(a.speak())
```

Output:
```
Rex says Woof!
Whiskers says Meow!
Generic makes a sound.
```

### Step 7: `super()` — calling the parent

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Employee(Person):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)   # call Person.__init__
        self.employee_id = employee_id

e = Employee("Alice", 30, "E123")
print(e.name, e.age, e.employee_id)   # Alice 30 E123
```

### Step 8: `@property` — computed attributes

Properties let you define methods that are accessed like plain attributes
(no `()` needed). Useful for computed values or validation.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

    @property
    def circumference(self):
        return 2 * 3.14159 * self._radius

c = Circle(5)
print(c.area)             # 78.53975 — accessed like an attribute
c.radius = 10             # setter works too
print(c.area)             # 314.159
# c.radius = -1            # ValueError!
```

### Step 9: Dunder methods

Dunder (double underscore) methods let you define how objects behave with
Python's built-in operations.

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        # Called by print() and str()
        return f"{self.title} by {self.author}"

    def __repr__(self):
        # Called by repr() — should be unambiguous
        return f"Book({self.title!r}, {self.author!r}, {self.pages})"

    def __eq__(self, other):
        # Called by ==
        if not isinstance(other, Book):
            return NotImplemented
        return self.title == other.title and self.author == other.author

    def __len__(self):
        # Called by len()
        return self.pages

    def __lt__(self, other):
        # Called by <
        return self.pages < other.pages

b1 = Book("1984", "Orwell", 328)
b2 = Book("1984", "Orwell", 328)
b3 = Book("Brave New World", "Huxley", 311)

print(b1)               # 1984 by Orwell
print(repr(b1))         # Book('1984', 'Orwell', 328)
print(b1 == b2)         # True
print(len(b1))          # 328
print(b1 < b3)          # False (328 > 311)
```

### Step 10: `@dataclass`

Python 3.7+ dataclasses auto-generate `__init__`, `__repr__`, `__eq__`, and
more — saving a lot of boilerplate.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

p1 = Point(3, 4)
p2 = Point(3, 4)
print(p1)               # Point(x=3, y=4)
print(p1 == p2)         # True
print(p1.distance_from_origin())  # 5.0
```

Additional features:

```python
from dataclasses import dataclass, field

@dataclass(order=True)    # generates __lt__, __le__, __gt__, __ge__
class Student:
    name: str
    grade: int = 0
    subjects: list = field(default_factory=list)  # mutable default hack

s = Student("Alice", 10)
```

### Step 11: Composition vs inheritance

- **Inheritance**: "is-a" relationship (Dog **is an** Animal).
- **Composition**: "has-a" relationship (Car **has an** Engine).

```python
# Composition
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self):
        self.engine = Engine()    # Car has an Engine

    def start(self):
        return self.engine.start()
```

Prefer composition over inheritance. It is more flexible and avoids deep
class hierarchies.

---

## 4. Common mistakes

### Forgetting `self` as the first parameter
```python
class Dog:
    def bark():      # ❌ missing self — TypeError when called
        return "Woof!"
```

### Using mutable default arguments in `__init__`
Same problem as functions — use `None` and create inside.

### Confusing class variables with instance variables
Mutable class variables (like `[]`) are shared — modifying via one instance
affects all instances.

### Overusing inheritance
```python
class Animal: ...
class Mammal(Animal): ...
class Dog(Mammal): ...
class Poodle(Dog): ...    # too deep — prefer composition
```

### Forgetting `super().__init__()`
If you override `__init__` in a subclass, the parent's `__init__` is not called
unless you call `super().__init__()` explicitly.

### Using `@property` for simple attributes that don't need logic
Properties add complexity. Use them when you need computed values or
validation, not for every attribute.

---

## 5. Exercises

1. **BankAccount** — Create a class with `owner`, `balance`, `deposit(amount)`,
   `withdraw(amount)` (check for sufficient funds). Add `__str__`.

2. **Inheritance** — Create `Shape` with `area()` method. Create `Circle` and
   `Rectangle` that inherit from `Shape` and override `area()`. Use `super()`
   in `__init__`.

3. **Library system** — Create `Book` (title, author, is_checked_out) and
   `Library` (name, books list). Methods: `add_book(book)`, `check_out(title)`,
   `return_book(title)`. Use `@dataclass` for `Book`.

4. **Property validation** — Create `Temperature` class with a `celsius`
   property. The setter should reject values below -273.15 (absolute zero).
   Add a `fahrenheit` property that converts.

5. **Dunder methods** — Create a `Vector2D` class with `x` and `y`. Implement
   `__add__` (vector addition), `__sub__`, `__mul__` (scalar), `__eq__`,
   `__repr__`, and `__abs__` (magnitude).

6. **Class method** — Add a `from_polar(r, theta)` class method to `Vector2D`
   that creates a vector from polar coordinates.

7. **Composition** — Model a `Computer` that has a `CPU`, `RAM`, and `Storage`.
   Each component is its own class with `__str__`. `Computer.__str__` should
   list its components.

8. **Dataclass with default_factory** — Create a `Team` dataclass with `name`
   and `members` (list, default empty). Add a method `add_member(name)`.

---

## 6. Self-check questions

1. What is the difference between a class and an instance?
2. What is `self`? Why is it needed?
3. What is the difference between a class variable and an instance variable?
4. What does `@classmethod` do? How is it different from a static method?
5. What is inheritance? How do you specify that `Dog` inherits from `Animal`?
6. What does `super()` do?
7. What is `@property` used for?
8. Name three dunder methods and what they do.
9. What is `@dataclass` and what does it auto-generate?
10. What is the difference between composition and inheritance? When would you
    prefer one over the other?

---

## 7. What's next

You now understand object-oriented programming in Python. You know:
- Classes, `__init__`, `self`, instance/class variables
- Instance, class, and static methods
- Inheritance and `super()`
- Properties, dunder methods, dataclasses
- Composition vs inheritance

In **Level 10** — the capstone — you will put everything together. You will
learn about **testing** with `pytest`, **command-line argument parsing** with
`argparse`, practical standard library modules, and build a **complete CLI
tool** from scratch.

Close this lesson and open `10-testing-cli-capstone.md`.
