# 1. Write a few lines of text to a new file.
# Close it, open it in your editor, and confirm it's really there.
# Then read it back and print it. You've now made something that outlives your program.

with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("Hello, this is my first line.\n")
    file.write("Python makes working with files easy.\n")
    file.write("I am learning file handling.\n")

with open("notes.txt", "r", encoding="utf-8") as file:
    print(file.read())


# Open that same file in "w" mode again and write a single short line. Look at the file.
# Everything else is gone. Sit with that for a second — then find the mode that adds to the end instead of destroying.

# with open("notes.txt", "w") as file:
#     file.write("I am adding a new line in the file, but I am guess it will not be appended.\n")


with open("notes.txt", "a", encoding="utf-8") as file:
    file.write("This is a new line, I am sure that this will be added as a new line.\n")


# Read a file line by line and print each line with its line number.
# Your output will have blank lines between entries — work out why, then fix it.
# That's the trailing newline, and finding it yourself is the point.

with open("notes.txt", "r", encoding="utf-8") as file:
    for line in file.readlines():
        print(line)





with open("notes.txt", "r", encoding="utf-8") as file:
    for i, line in enumerate(file, start=1):
        print(f"Line {i}: {line}", end="")



# Take the word-count program from Day 5 and point it at a real text file instead of a hardcoded sentence.
# Print the ten most common words. Your Day 5 cleaning — lowercase, strip punctuation — carries over.
# (Grab any plain-text file: paste an article into one, or use one of your own notes files.)

import string

with open("notes.md", "r", encoding="utf-8") as file:
    sentence = file.read()

dict_words = {}

for word in sentence.split():
    word = word.lower().strip(string.punctuation)

    if word in dict_words:
        dict_words[word] = dict_words[word] + 1
    else:
        dict_words[word] = 1

most_common = sorted(
    dict_words.items(),
    key=lambda item: item[1],
    reverse=True
)

print(most_common[:10])


# Write the results of problem 4 back out to a new file, one word,count per line.
# You've now built a read → process → write pipeline, which is the shape of essentially every data program ever written.
with open("word_counts.txt", "w", encoding="utf-8") as file:
    for word, count in most_common[:10]:
        file.write(f"{word},{count}\n")


# Try to open a file that doesn't exist. Read the error. Then write a function that reads a file if it's there and
# returns something sensible if it isn't — without crashing. You'll need to look up try/except;
# this is your first contact with error handling, and we'll do it properly soon.

# 6. Write a function that tries to read a file.
# If the file doesn't exist, handle the error sensibly.

def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        return "Sorry, that file does not exist."


result = read_file("somefile.txt")

print(result)