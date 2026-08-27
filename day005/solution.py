# 1.Build a dictionary mapping five people('s names to their ages. Look one up. '
# Add a sixth. Change one age. Delete one. Print the whole thing after each step.)


dict_1 = {
    "Asish": 29,
    "Gai": 32,
    "Man": 31,
    "San": 28,
    "Harsh": 28
}

print(dict_1["Asish"])

dict_1["Man"]=30
print(dict_1)
del dict_1["San"]
print(dict_1)
dict_1.pop("Harsh")
print(dict_1)

#
# Ask it for a name that isn('t there. Read the error. '
# ('Then find the method that lets you ask without crashing, and give it a sensible fallback. '
# 'Write down when you'))d want each behavior — crashing is sometimes the right choice.
# print(dict_1["name7"])
#This raises the KeyError meaning no key in the dict
dict_1.get("Boy")


# Loop over the dictionary and print each name with its age on one line.
# Find the way to get both at once rather than looking up each value inside the loop.

for key, value in dict_1.items():
    print(key, "=", value)

# Count how many times each word appears in a sentence, using a dictionary.
# Split the sentence into words, then build up your counts.
# You'll hit the "this key doesn't exist yet.  problem immediately — solve it.
# This is the single most common dictionary pattern in existence.

sentence = "This is a tree whose trunk is like the size of an elephant. Funny right? but that's true. This is not a joke!"
dict_words = {}
for word in sentence.split():
    word = word.lower()

    if word in dict_words:
        dict_words[word] = dict_words[word] + 1
    else:
        dict_words[word] = 1

print(dict_words)


# Build a nested structure: a dictionary where each person maps to another dictionary holding their age, city,
# and a list of hobbies. Then print one person's second hobby. Getting the chain of brackets right is the skill.

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

print(people["Maya"]["hobbies"][1])



# Take a list with duplicates in it. Produce a list of the unique values, keeping the original order.
# Do it with a loop and something that
# makes "have I seen this already?" fast — think about why a list is the wrong tool for that check.

original_list = [1, 2, 3, 3, 4, 4, "Asish", "Asish"]

seen = set()
unique_values = []

for value in original_list:
    if value not in seen:
        seen.add(value)
        unique_values.append(value)

print(unique_values)
