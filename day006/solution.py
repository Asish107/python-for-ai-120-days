# Take a sentence. Print its first character, its last character, and its length.
# Get the last character two different ways — one counting from the front, one from the back.
# Which is better, and why?


sentence = "This is the first line of code I am writing on my own"

print(sentence[0][0])

print(sentence.split()[-1][-1])

print(sentence[len(sentence) - 1])
print(sentence[-1])



# 2. Slice out the first five characters, the last five, and everything in the middle.
# Then slice with a step to get every second character.
# Then find out what a negative step does. That last one is a well-known trick.

print(sentence[0:5])
print(sentence[-5:])
print(sentence[5:-5])
print(sentence[::2])
print(sentence[::-1])


# 3. Write a function that takes a messy name — extra spaces, random capitalization,
# like " aSiSh KuMar " — and returns it cleaned to "Asish Kumar". Chain the methods.
# Then confirm the original string is unchanged, and explain why it must be.

def neat_name(full_name):
    return " ".join(full_name.split()).title()


name = " aSiSh    KuMar "

clean_name = neat_name(name)

print("Cleaned name:", clean_name)
print("Original name:", name)

# 4. Take a sentence and reverse the order of its words (not its characters).
# This is .split() and .join() working together, and it's a classic interview question.

sentence = "This is the first line of code I am writing on my own"

reverse_words = sentence.split()[::-1]

final_output = " ".join(reverse_words)

print(final_output)


    # 5. Write a function that checks whether a word is a palindrome — reads the same forwards and backwards.
    # Then make it work for "A man, a plan, a canal: Panama", which requires cleaning first.
    # The cleaning is the real work, same as Day 5.



def check_palindrome(long_sent):
    cleaned = ""

    for char in long_sent:
        if char.isalnum():
            cleaned = cleaned + char.lower()

    is_palindrome = cleaned == cleaned[::-1]

    return cleaned, is_palindrome


long_sent = "A man, a plan, a canal: Panama"

result = check_palindrome(long_sent)

print(result[0])
print(result[1])

# 6. Build a small report using f-strings: take your nested people dictionary from Day 5 and print one formatted
# line per person — name, age, city, and their hobbies joined into a readable list like "reading, painting and hiking".
# Look up how to control decimal places and column width inside an f-string while you're there.


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

for name, person in people.items():
    hobbies = ", ".join(person["hobbies"])

    print(f"{name} is {person['age']} years old, lives in {person['city']}, and enjoys {hobbies}.")


