# 1. Write a function `is_even(n)` that returns True if n is even, and False if n is odd.
#    (Hint: Use the modulus operator % to check for evenness.)
def is_even(n):
    if n % 2:
        return False
    else:
        return True
    
print(is_even(2))
print(is_even(3))

# 2. Write a function `greet_user(name, greeting="Hello")` that takes a name and an optional greeting, and prints "{greeting}, {name}!".
#    Call this function with both positional and keyword arguments to test it.
def greet_user(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet_user("Pablo", "WAZZUP")

# 3. Write a function `multiply_all(*numbers)` that takes any number of numeric arguments and returns the product of all of them.
def multiply_all(*numbers):
    num = 1
    for i in numbers:
        num *= i
    return num

print(multiply_all(13, 2, 5, 6))

# 4. Write a function `print_dict(**kwargs)` that takes any number of keyword arguments and prints out each key and value in the format "key: value".
def print_dict(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_dict(name = "Alice", age = 30, country = "Mexico")

# 5. Given a list of integers, use `filter` and a `lambda` to create a new list that contains only the even integers from the original list.
#    (For example, filter even numbers from [3, 4, 5, 6, 7, 8] to get [4, 6, 8].)
numList = [1,2,3,4,5,6,7,8,9]
filterList = list(filter(lambda x: x % 2 == 0, numList))
print(filterList)

# 6. (Advanced) Write a decorator `announce` that, when applied to a function, prints messages before and after the function runs.
#    For example:
#       @announce
#       def say_goodnight():
#           print("Good night!")
#    Calling say_goodnight() should print:
#       "About to run say_goodnight..."
#       "Good night!"
#       "Done running say_goodnight."

