# # Python Functions, Parameters, Lambda, and Decorators - Tutorial
#
# This script demonstrates the basics of defining and using functions in Python,
# different types of function parameters, anonymous functions (lambdas),
# and decorators (how to define and use them).
# Explanations are provided as comments, and example usage is shown with print statements.

class animal():
    def runs():
        pass


class dog(animal):
    def bark():
        pass



# --------------------------------------------------
# Basic Function Definition and Calling
# --------------------------------------------------
# A function in Python is defined using the 'def' keyword.
# Syntax:
#    def function_name(parameters):
#        """optional docstring"""
#        <function_body>
#        [return value]  (optional return statement)
#
# Functions may or may not return a value. If no `return` is used, the function returns None by default.
#
# Let's define a simple function and call it:
def greet():
    print("Hello, world!")

# Calling the function:
greet()
# Expected output: Hello, world!

# The function above takes no parameters and just prints a message.
# We can also write functions that take parameters (inputs) and return values.
# For example:
def add(x, y):
    return x + y

# Using the function and printing its result:
result = add(5, 3)
print("5 + 3 =", result)
# Expected output: 5 + 3 = 8

# The function 'add' takes two parameters and returns their sum.
# We used a return statement to send back a value to the caller (which we stored in 'result').

# --------------------------------------------------
# Function Parameters and Arguments
# --------------------------------------------------
# When calling functions, you can pass arguments either by position or by keyword.
# By default, function parameters are positional-or-keyword, meaning you can call the function
# either by passing arguments in order, or by naming them.
# Example:
def describe_pet(animal, name):
    print(f"I have a {animal} named {name}.")

# Calling with positional arguments (order matters):
describe_pet("dog", "Buddy")
# Output: I have a dog named Buddy.

# Calling with keyword arguments (order doesn't matter when using keywords):
describe_pet(name="Max", animal="cat")
# Output: I have a cat named Max.

# We can mix positional and keyword arguments, but positional arguments must come first:
describe_pet("rabbit", name="Thumper")
# Output: I have a rabbit named Thumper.
# (Here we passed "rabbit" positionally for animal, and used keyword for name.)
# Note: The following would **not** work (positional argument after a keyword argument):
# describe_pet(name="Thumper", "rabbit")  # Invalid syntax!

# Default parameter values:
# We can provide default values for parameters in the function definition.
# Default parameters make some arguments optional when calling the function.
def greet_person(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet_person("Alice")
# Output: Hello, Alice!
greet_person("Bob", "Hi")
# Output: Hi, Bob!
greet_person(name="Charlie", greeting="Good morning")
# Output: Good morning, Charlie!

# In greet_person, 'greeting' has a default value "Hello". If we don't provide it, it uses the default.
# We can override it by passing a different value (positionally or by keyword).

# Arbitrary positional arguments (*args):
# Sometimes, you want a function to accept any number of positional arguments.
# Use *args in the definition to collect extra positional arguments into a tuple.
def multiply(*args):
    # *args allows 0 or more positional arguments, accessible as a tuple 'args'.
    result = 1
    for num in args:
        result *= num
    return result

print(multiply(2, 3, 4))  # 2*3*4 = 24
print(multiply(5,))       # just 5 (single argument tuple)
print(multiply())         # no arguments, result = 1 (multiplicative identity)
# Output:
# 24
# 5
# 1

# In multiply(), *args collects all extra positional arguments.
# e.g., multiply(2,3,4) → inside the function, args = (2, 3, 4), and the product is returned.

# Arbitrary keyword arguments (**kwargs):
# Similarly, **kwargs in the definition collects extra keyword arguments into a dictionary.
def print_kwargs(**kwargs):
    # kwargs is a dict of all keyword arguments passed.
    for key, value in kwargs.items():
        print(f"{key} = {value}")

print_kwargs(name="Alice", age=30, country="Mexico")
# Example output:
# name = Alice
# age = 30
# country = Mexico

# In print_kwargs(), **kwargs captures all keyword args into a dict.
# We can iterate over kwargs to access keys and values.

# You can combine different kinds of parameters in one function definition.
# The typical order is:
#   1. Positional-or-keyword parameters (regular parameters, can have defaults)
#   2. *args (optional, for variable number of positional args)
#   3. Keyword-only parameters (require keywords, can have defaults)
#   4. **kwargs (optional, for variable number of keyword args)
# (Positional-only parameters, if used, would be defined before all these and separated by '/')
#
# Example: a function using multiple kinds of parameters
def example_func(a, b=2, *args, c, d=5, **kwargs):
    # a: positional-or-keyword (required)
    # b: positional-or-keyword with default 2
    # *args: arbitrary extra positional arguments (tuple)
    # c: keyword-only (required, no default)
    # d: keyword-only (optional, default 5)
    # **kwargs: arbitrary extra keyword arguments (dict)
    print("a =", a)
    print("b =", b)
    print("args =", args)
    print("c =", c)
    print("d =", d)
    print("kwargs =", kwargs)

# Call the function with a mix of arguments:
example_func(1, 3, 4, 5, c=7, e=9, f=10)
# Explanation of the call above:
# a = 1  (first positional argument)
# b = 3  (second positional argument, overrides default 2)
# *args collects (4, 5)  (the remaining positional arguments)
# c = 7  (must be provided as keyword, as defined)
# d uses default 5 (not provided in call)
# **kwargs collects {'e': 9, 'f': 10}
# Expected output:
# a = 1
# b = 3
# args = (4, 5)
# c = 7
# d = 5
# kwargs = {'e': 9, 'f': 10}

# Positional-only and Keyword-only arguments (advanced):
# Python allows you to specify some parameters as positional-only (cannot be passed by name)
# or keyword-only (cannot be passed by position).
# - To mark positional-only parameters, use '/' in the function definition.
# - To mark keyword-only parameters, use '*' in the function definition (a bare asterisk or *args).
# These are advanced features (positional-only parameters were added in Python 3.8).
#
# Positional-only example:
def pow_pos_only(x, y, /):
    # x and y are positional-only; they cannot be passed as keyword arguments.
    return x ** y

print(pow_pos_only(2, 3))   # 2**3 = 8
# pow_pos_only(x=2, y=3)    # This would error: x and y must be given positionally.

# Keyword-only example:
def greet_kw_only(*, greeting, name):
    # All arguments after * must be passed by keyword.
    print(f"{greeting}, {name}!")

# greet_kw_only("Hello", "Alice")  # This would error: greeting and name must be keywords.
greet_kw_only(greeting="Hi", name="Sam")
# Output: Hi, Sam!

# According to Python documentation, there are five kinds of parameters in function definitions:
# 1. Positional-or-keyword (can be passed by position or name)
# 2. Positional-only (use '/' in def, must be passed by position)
# 3. Keyword-only (use '*' in def, must be passed by keyword)
# 4. Var-positional (*args, for arbitrary extra positional args)
# 5. Var-keyword (**kwargs, for arbitrary extra keyword args)
# :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}

# --------------------------------------------------
# Anonymous Functions (Lambda Expressions)
# --------------------------------------------------
# In Python, you can create small anonymous functions using the `lambda` keyword.
# Lambda functions are defined inline and are not given a formal name.
# They are useful for short, simple operations, especially as arguments to other functions.
# Syntax: lambda <parameters>: <expression>
# (The lambda returns the value of the expression.)
#
# Example: a lambda that adds two numbers
add = lambda x, y: x + y
print(add(10, 5))  # Output: 15
# This lambda performs the same operation as a def function that adds two numbers.
#
# Lambdas are often used with built-in functions like map, filter, sorted, etc.
# Example: using lambda with map to square a list of numbers
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
print("Squares:", squares)
# Output: Squares: [1, 4, 9, 16, 25]
#
# Example: using lambda with filter to get even numbers from a list
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Evens:", evens)
# Output: Evens: [2, 4]
#
# Example: using lambda as a key in sorting (sort list of tuples by the second element)
pairs = [(1, 'a'), (2, 'c'), (3, 'b')]
pairs_sorted = sorted(pairs, key=lambda pair: pair[1])
print("Sorted by second element:", pairs_sorted)
# Output: Sorted by second element: [(1, 'a'), (3, 'b'), (2, 'c')]
#
# Note: Lambda functions are limited to a single expression. For more complex operations, 
# use a regular function defined with def.

# --------------------------------------------------
# Decorators in Python
# --------------------------------------------------
# Decorators are a powerful feature that allow you to modify or enhance the behavior of functions.
# A decorator is essentially a function that takes another function as input and returns a new function with added functionality:contentReference[oaicite:2]{index=2}.
# This is useful for cross-cutting concerns (logging, timing, access control, etc.) without changing the original function's code.
#
# Key concept: Functions in Python are "first-class citizens" (first-class objects):contentReference[oaicite:3]{index=3}.
# This means functions can be passed around like any other object (assigned to variables, passed as arguments, returned from other functions).
# Decorators leverage this fact to wrap one function with another.
#
# Basic decorator example:
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function '{func.__name__}'")
        result = func(*args, **kwargs)   # call the original function
        print(f"Finished calling '{func.__name__}'")
        return result
    return wrapper

# Use the decorator on a function with the @ syntax
@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")

# Now, calling say_hello will actually call the wrapper defined in my_decorator
say_hello("Alice")
# Output:
# Calling function 'say_hello'
# Hello, Alice!
# Finished calling 'say_hello'

# Explanation:
# The line @my_decorator is equivalent to: say_hello = my_decorator(say_hello).
# my_decorator returns the 'wrapper' function which adds extra behavior (printing messages) around the original function call.
#
# You can also apply a decorator manually without using @:
def say_goodbye(name):
    print(f"Goodbye, {name}!")

say_goodbye = my_decorator(say_goodbye)  # decorating manually
say_goodbye("Bob")
# Output:
# Calling function 'say_goodbye'
# Goodbye, Bob!
# Finished calling 'say_goodbye'
#
# Notice that our decorator uses *args and **kwargs in wrapper so it can accept any function arguments.
# This makes the decorator flexible enough to wrap functions of any signature.
#
# (Advanced note: When writing decorators, use functools.wraps to preserve the original function's metadata like name and docstring. 
# This is beyond our current scope, but important for real-world decorator usage.)