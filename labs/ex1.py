
# ==================================================
# Exercises
# ==================================================
# Try to solve the following exercises:
#
# 1. Write a function `is_even(n)` that returns True if n is even, and False if n is odd.
#    (Hint: Use the modulus operator % to check for evenness.)
#
# 2. Write a function `greet_user(name, greeting="Hello")` that takes a name and an optional greeting, and prints "{greeting}, {name}!".
#    Call this function with both positional and keyword arguments to test it.
#
# 3. Write a function `multiply_all(*numbers)` that takes any number of numeric arguments and returns the product of all of them.
#
# 4. Write a function `print_dict(**kwargs)` that takes any number of keyword arguments and prints out each key and value in the format "key: value".
#
# 5. Given a list of integers, use `filter` and a `lambda` to create a new list that contains only the even integers from the original list.
#    (For example, filter even numbers from [3, 4, 5, 6, 7, 8] to get [4, 6, 8].)
#
# 6. (Advanced) Write a decorator `announce` that, when applied to a function, prints messages before and after the function runs.
#    For example:
#       @announce
#       def say_goodnight():
#           print("Good night!")
#    Calling say_goodnight() should print:
#       "About to run say_goodnight..."
#       "Good night!"
#       "Done running say_goodnight."
#
# Try to solve these on your own before looking at the solutions below.
# Scroll down for the solutions when you're ready...















# ==================================================
# Solutions to Exercises
# ==================================================
# 1. Solution: Function to check if a number is even
def is_even(n):
    return n % 2 == 0

# Testing the solution:
print(is_even(4))  # True
print(is_even(7))  # False

# 2. Solution: greet_user with an optional greeting
def greet_user(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

# Testing:
greet_user("Alice")                      # uses default greeting
greet_user("Bob", "Hi")                 # uses custom greeting
greet_user(name="Charlie", greeting="Welcome")  # using keyword arguments

# 3. Solution: multiply_all using *args
def multiply_all(*numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

# Testing:
print(multiply_all(2, 3, 4))   # 24
print(multiply_all(5,))        # 5
print(multiply_all())          # 1 (no arguments, returns 1)

# 4. Solution: print_dict using **kwargs
def print_dict(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Testing:
print_dict(name="Alice", age=30, country="Mexico")

# 5. Solution: filter even numbers with lambda
nums = [3, 4, 5, 6, 7, 8]
evens_filtered = list(filter(lambda x: x % 2 == 0, nums))
print("Even numbers:", evens_filtered)
# Expected output: Even numbers: [4, 6, 8]

# 6. Solution: announce decorator
def announce(func):
    def wrapper(*args, **kwargs):
        print(f"About to run {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"Done running {func.__name__}.")
        return result
    return wrapper

# Applying the decorator to test it
@announce
def say_goodnight():
    print("Good night!")

say_goodnight()
# Expected output:
# About to run say_goodnight...
# Good night!
# Done running say_goodnight.