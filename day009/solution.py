# 1. Write code that raises three different errors on purpose:
# dividing by zero, indexing past the end of a list, and converting "abc" to a number.
# Read all three tracebacks properly — name the exception type and identify the exact line for each.


def errors(num1, num2, list_a, string_a):
    result_zero = num1 / num2
    result_one = list_a[len(list_a)]
    result_two = int(string_a)

    print(result_zero)
    print(result_one)
    print(result_two)

# 1. ZeroDivisionError
# errors(10, 0, [1, 2, 3], "abc")

# 2. IndexError
# errors(10, 2, [1, 2, 3], "abc")

# 3. ValueError
# errors(10, 2, [1, 2, 3], "abc")


# Write a function that converts a string to a number and handles bad input gracefully.
# Then feed it "abc", "", "12.5" and None. Not all of them raise the same error — catch each specifically.

def convertor(string_a):
    try:
        result = int(string_a)
        print(result)
    except ValueError:
        print("ValueError: Please enter a valid whole number.")
    except TypeError:
        print("TypeError: The input cannot be None.")


convertor("abc")
convertor("")
convertor("12.5")
convertor(None)


# Take your Day 7 read_file function.
# It currently returns "Sorry, that file does not exist." — a string the caller can't distinguish from real content.
# Rewrite it two ways: one that raises, one that returns a clear signal of failure. Write down which you'd ship and why.
#


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


result = read_file("somefile.txt")
print(result)

print(result)

def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None


result = read_file("somefile.txt")

if result is None:
    print("File does not exist.")
else:
    print(result)


# Go back to find_largest. It returns None for an empty list, which broke bigger_max one layer up on Day 4.
# Rewrite it to raise a ValueError instead. Then update bigger_max to catch it.
# Notice that the error is now handled where the caller knows what to do, not where it happened.

def find_largest(numbers):
    if not numbers:
        raise ValueError("Cannot find the largest number in an empty list.")

    largest_so_far = numbers[0]

    for current_number in numbers:
        if current_number > largest_so_far:
            largest_so_far = current_number

    return largest_so_far


def bigger_max(list_1, list_2):
    try:
        list_1_large = find_largest(list_1)
        list_2_large = find_largest(list_2)

        if list_1_large > list_2_large:
            print(f"The greatest number among both lists is {list_1_large}")
        elif list_2_large > list_1_large:
            print(f"The greatest number among both lists is {list_2_large}")
        else:
            print(f"Both {list_1_large} and {list_2_large} are equal")

    except ValueError:
        if not list_1 and not list_2:
            print("Both lists are empty.")
        elif not list_1:
            print(f"The greatest number among both lists is {find_largest(list_2)}")
        else:
            print(f"The greatest number among both lists is {find_largest(list_1)}")

# Write a function that opens a file, reads it, and uses finally to print a message that appears whether it succeeded or failed.
# Then make it fail on purpose and confirm the message still appears. This is why with works.

def open_file():
    try:
        with open("filename.txt", "r") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print("The file does not exist.")
    finally:
        print("Finished attempting to open the file.")


open_file()

# Define your own exception type — something like InvalidRecordError — and raise it when data
# doesn't meet a rule you choose. Then catch it specifically. This is how real codebases signal domain-specific failures.

class InvalidRecordError(Exception):
    pass


def own(age):
    if age < 0 or age > 120:
        raise InvalidRecordError(
            f"age must be between 0 and 120, got {age}"
        )

    print(f"Age {age} is valid.")


own(200)


# The counter-exercise. Write a try/except that catches everything and does nothing with it.
# Then put a typo inside the try. Watch your own bug get silently swallowed. Write down what you'd tell someone who does this.

def convert_number(user_input):
    try:
        result = int(user_input)
        return result
    except ValueError:
        print("Invalid number.")
        return None

