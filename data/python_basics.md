# Python Basics

## What is Python?

Python is a high-level, interpreted programming language created by
**Guido van Rossum** and first released in **1991**. It emphasizes code
readability with its use of significant whitespace indentation.

## Key Features

- **Easy to learn** - Clean syntax that reads like English
- **Dynamically typed** - No need to declare variable types
- **Garbage collected** - Automatic memory management
- **Cross-platform** - Runs on Windows, macOS, Linux, and more
- **Large standard library** - "Batteries included" philosophy

## Data Types

Python has several built-in data types:

- `int` - Integer numbers (e.g., 42, -7, 0)
- `float` - Decimal numbers (e.g., 3.14, -0.5)
- `str` - Text strings (e.g., "hello", 'world')
- `bool` - Boolean values (True or False)
- `list` - Ordered collections (e.g., [1, 2, 3])
- `dict` - Key-value pairs (e.g., {"name": "Alice", "age": 30})
- `tuple` - Immutable ordered collections (e.g., (1, 2, 3))
- `set` - Unordered unique values (e.g., {1, 2, 3})

## Control Flow

Python uses `if`, `for`, and `while` for control flow:

```python
# If statement
age = 25
if age >= 18:
    print("You are an adult")
elif age >= 13:
    print("You are a teenager")
else:
    print("You are a child")

# For loop
for i in range(5):
    print(i)  # Prints 0, 1, 2, 3, 4

# While loop
count = 0
while count < 3:
    print(count)
    count += 1
```

## Functions

Functions are defined with the `def` keyword:

```python
def greet(name):
    """Returns a greeting message."""
    return f"Hello, {name}!"

message = greet("Alice")
print(message)  # Output: Hello, Alice!
```

## List Comprehensions

A concise way to create lists:

```python
# Traditional way
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension (same result, one line)
squares = [x ** 2 for x in range(10)]

# With condition
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
```

## Error Handling

Python uses try/except blocks for error handling:

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
finally:
    print("This always runs")
```

## Python Versions

- **Python 2** (2000): Legacy, no longer maintained
- **Python 3** (2008): Current version, breaking changes from Python 2
- **Python 3.12** (2023): Improved error messages, new type parameter syntax
- **Python 3.13** (2024): Experimental JIT compiler, improved REPL
