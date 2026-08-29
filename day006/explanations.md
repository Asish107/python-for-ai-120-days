# Day 006 — Strings

Reference notes. Read these *after* trying to recall the answer yourself.

---

## The mechanism

**A string is an ordered sequence of characters**, each at a numbered position
starting from 0. Everything you know about indexing lists applies unchanged —
same syntax, same rules.

```
sentence[0]    # first character
sentence[5]    # sixth character
```

You do **not** need to `.split()` into words to reach a character.
`sentence.split()[0][0]` gets there by a detour; `sentence[0]` is the direct
route.

(`sentence[0][0]` also "works" — it takes the first character, then the first
character *of that*, which is itself. Working by accident is still worth
deleting.)

### Strings are immutable

No method ever changes a string. Every one returns a **new** string.

**Consequence:** `some_string.strip()` on a line by itself is a no-op bug. It
computes a cleaned string and throws it away. You must capture the result:

```python
name = name.strip()          # capture it
print(clean(name), name)     # or use it directly
```

This is why problem 3's original string was unchanged after cleaning — it *had*
to be. Nothing can modify a string in place.

---

## Indexing forwards and backwards

| expression | meaning |
|---|---|
| `s[0]` | first character |
| `s[len(s) - 1]` | last character, counting from the front |
| `s[-1]` | last character, counting from the back |
| `len(s)` | number of characters |

**`s[-1]` is better**, and not just because it's shorter:

- **No arithmetic to get wrong.** `s[len(s)]` crashes — forgetting the `- 1` is
  the most common indexing mistake there is. `s[-1]` has no off-by-one to make.
- **It says what you mean.** "The last one" reads instantly; "the one at
  length-minus-one" makes the reader do subtraction in their head.

> **Fewer moving parts means fewer places to be wrong.**

---

## Slicing

`s[start:stop:step]` — `start` included, `stop` **excluded**.

| slice | result |
|---|---|
| `s[0:5]` | first five characters |
| `s[-5:]` | last five |
| `s[5:-5]` | everything in the middle |
| `s[::2]` | every second character |
| `s[::-1]` | **the whole thing reversed** |

Omit a part and you get the sensible default: start of string, end of string,
step of 1.

`[::-1]` is the reversal idiom. You'll see it constantly — it's how the
palindrome check works, and how problem 4 reversed the word order.

**The same syntax works on lists.** Learning slicing once buys you both.

---

## Methods you'll use constantly

| method | does |
|---|---|
| `.lower()` / `.upper()` | change case |
| `.strip()` | remove whitespace **from the ends only** |
| `.strip(chars)` | remove those specific characters from the ends |
| `.title()` | capitalise the first letter of each word |
| `.replace(a, b)` | swap text |
| `.startswith()` / `.endswith()` | boolean checks |
| `.find()` | position of a substring, or `-1` if absent |
| `.isalnum()` | is this character a letter or digit? |
| `.split()` | string → list |
| `.join()` | list → string |

All of them return new strings. None of them modify.

---

## `.split()` and `.join()` — two halves of one idea

```python
words = sentence.split()          # "a b c"  →  ["a", "b", "c"]
sentence = " ".join(words)        # ["a", "b", "c"]  →  "a b c"
```

**`.join()` is written in the order that confuses everyone:** the *separator*
goes first and owns the method. Read `", ".join(items)` as *"glue these together
with a comma and a space."*

### The whitespace-normalising trick

```python
" ".join(messy.split())
```

`.split()` with **no argument** splits on any run of whitespace and discards the
empty pieces. So this one line fixes leading spaces, trailing spaces, *and*
multiple spaces in the middle — all at once.

`.strip()` alone only touches the ends. `"aSiSh    KuMar"` stays mangled in the
middle. Real names arrive like that.

### Reversing word order

```python
" ".join(sentence.split()[::-1])
```

Split into words → reverse the list → join back. A classic interview question,
and three ideas composed.

---

## f-strings

```python
f"{name} is {person['age']} years old"
```

Note the quote style inside: the f-string uses double quotes, so the dictionary
key inside uses single quotes. Mixing them is how you nest quotes safely.

**Format specs** go after a colon:

| spec | effect |
|---|---|
| `{value:.2f}` | two decimal places |
| `{name:<10}` | left-align in 10 columns |
| `{name:>10}` | right-align in 10 columns |
| `{n:,}` | thousands separators — `1,234,567` |

Column widths are what turn a pile of prints into a readable table.

---

## Escapes and multi-line strings

- `\n` newline, `\t` tab, `\\` a literal backslash
- `\"` to put a double quote inside a double-quoted string (or just use single
  quotes outside)
- Triple quotes `"""..."""` for text spanning several lines

---

## Building strings in a loop — the immutability trap

```python
cleaned = ""
for char in text:
    cleaned = cleaned + char      # works, but...
```

Strings are immutable, so this does **not** append a character. It builds an
entirely new string every single time round the loop, then throws the old one
away.

For 30 characters, irrelevant. For a large file, that's hundreds of thousands of
throwaway strings, and it gets genuinely slow.

**The standard approach:** collect into a list, join once at the end.

```python
parts = []
for char in text:
    parts.append(char)
cleaned = "".join(parts)
```

Lists *can* be mutated, so appending is cheap. One string, built once.

> Day 2's immutability with a performance consequence attached.

---

## The palindrome pattern

```python
cleaned = "".join(c.lower() for c in text if c.isalnum())
return cleaned == cleaned[::-1]
```

The comparison is one line. **The cleaning is the entire job** — stripping
punctuation, spaces and case so `"A man, a plan, a canal: Panama"` reduces to
`amanaplanacanalpanama`.

---

## Tuples, met by accident

```python
return cleaned, is_palindrome        # this makes a tuple
cleaned, ok = check_palindrome(text) # tuple unpacking
```

A **tuple** is an immutable sequence. Returning two values makes one
automatically.

Unpacking beats `result[0]` / `result[1]`, which force the reader to count.
`for key, value in d.items()` has been doing exactly this since Day 5.

And because tuples are immutable, they *can* be dictionary keys — unlike lists.
Day 2 and Day 5 again.

**Design note:** `check_palindrome` returning both the cleaned text and the
boolean means it does two jobs. Useful while debugging; if you only want the
answer, returning just the boolean is honest to the function's name.

---

## The recurring theme

Three days running, the same lesson:

- Day 5: punctuation stuck to words broke the word count
- Day 6: extra spaces and mixed case broke the name
- Day 6: punctuation and case broke the palindrome

**The logic is the easy part. Cleaning the input is the work.** That isn't a
coincidence of these exercises — it's the actual job in data and AI work.

---

## Still flagged: the print reflex

Problem 3 was specified as *returns* and was first written with `print`. Third
occurrence.

> Before finishing any function, ask: **does this hand something back?**

The test: can the result be fed into another function?

---

## Self-test

1. Why is `some_string.strip()` on its own line a bug?
2. Why is `s[-1]` better than `s[len(s) - 1]`?
3. What does `s[::-1]` do, and why?
4. In `", ".join(items)`, which part is the separator?
5. What does `" ".join(messy.split())` fix that `.strip()` cannot?
6. Why is building a string with `s = s + char` in a long loop slow?
7. What is the real work in a palindrome check?
8. What kind of object does `return a, b` create, and why can it be a dict key?
