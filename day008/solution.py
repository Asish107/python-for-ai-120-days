# 1. Take a list of numbers. Build a new list of their squares; first with a loop and append, then as a comprehension.
# Put them side by side and read both out loud.

def squares(some_list):
    squared = []
    for i in some_list:
        result = i*i
        squared.append(result)
    return squared
squares([4,5,6,7])
squares([1,2,3])

def squares(numbers):
    return [number * number for number in numbers]

squares([4,5,6,7])


# From a list of numbers, build a list containing only the even ones. Then only the even ones, squared.
# Notice where the condition goes versus where the transformation goes.

def even_nums(some_list):
    even_numbers = [number for number in some_list if number % 2 == 0]
    even_numbers_squared = [number*number for number in even_numbers]
    return even_numbers, even_numbers_squared

evens, squares = even_nums([4,5,6,7])
print(evens)
print(squares)

# Go back to your Day 6 palindrome function.
# You wrote a loop that built up a cleaned string character by character —
# the slow, immutability-violating version. Rewrite the cleaning as a comprehension joined at the end.

def check_palindrome(long_sent):
    cleaned = "".join(char.lower() for char in long_sent if char.isalnum())
    is_palindrome = cleaned == cleaned[::-1]

    return cleaned, is_palindrome

long_sent = "A man, a plan, a canal: Panama"


cleaned, is_pal = check_palindrome(long_sent)

print(cleaned, is_pal)

# Take your people dictionary from Day 5. Build a new dictionary mapping each name to just their city.
# Then one containing only the people over 26. That's a dict comprehension with a filter.


people = {
    "Maya": {
        "age": 28,
        "city": "Chicago",
        "hobbies": ["reading", "painting", "hiking"]
    },
    "Leo": {
        "age": 34,
        "city": "New York",
        "hobbies": ["cooking", "running", "photography"]
    },
    "Nina": {
        "age": 25,
        "city": "Austin",
        "hobbies": ["gaming", "traveling", "gardening"]
    }
}


# Build a new dictionary mapping each name to just their city.

new_dict = {key: people[key]["city"] for key, value in people.items()}

print(new_dict)


# Then one containing only the people over 26. That's a dict comprehension with a filter.
new_dict = {key: people[key]["age"] for key, value in people.items() if people[key]["age"]>26}
print(new_dict)

# Take a sentence and build a set of the unique word lengths in it.
# Then a dict mapping each word to its length. Compare how much code your Day 6 deduplication took.

sentence = "Heya! Hola Amigo, Como Estas?"

print(set(len(word) for word in sentence.split()))

# Then a dict mapping each word to its length. Compare how much code your Day 6 deduplication took.

print({word:len(word) for word in sentence.split()})