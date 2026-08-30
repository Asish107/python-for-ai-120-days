# Day 007 — Files

Reference notes. Read these *after* trying to recall the answer yourself.

---

## The mechanism

Back to Day 2's desk and filing cabinet.

A **file** lives in the cabinet — it survives your program ending. To work on it
you **open** it, which gives you a connection; you read or write through that
connection; then you **close** it, which flushes anything still pending and
releases the file.

**Forget to close and your writes may never reach the disk.** They sit in a
buffer and vanish when the program ends badly.

### `with` — always use it

```python
with open("notes.txt", "r", encoding="utf-8") as file:
    ...
```

`with` closes the file automatically when the block ends — **including when your
code crashes halfway through**. That last part is what makes it non-negotiable:
manual `.close()` calls get skipped by exceptions, and the file stays open or the
data stays unwritten.

You'll see older code that opens without `with`. It's a bug waiting for the right
moment.

---

## Modes

| mode | meaning |
|---|---|
| `"r"` | read (default). Errors if the file doesn't exist |
| `"w"` | write — **destroys existing contents the instant you open it** |
| `"a"` | append — adds to the end, keeps what's there |
| `"x"` | create, and fail if it already exists |

**`"w"` is the most destructive thing learned so far.** The truncation happens on
*open*, before you write a single byte. Opening a file in `"w"` mode and then
crashing still leaves you with an empty file.

Learn this on a file you don't care about. Everybody learns it once.

`"a"` is what you want when adding to something that already exists.

---

## Encoding — always specify `utf-8`

```python
open("notes.txt", "r", encoding="utf-8")
```

Text is stored on disk as **bytes**. An encoding is the rulebook for turning
bytes into characters. UTF-8 is the modern universal standard.

**Python's default encoding varies by operating system.** Code that works on your
Mac can crash on Windows the moment it meets a curly quote, an accented letter or
an emoji — or worse, silently read the wrong characters and corrupt your data.

Four extra words that remove an entire class of "works on my machine" bug.
Put it on **every** `open` call.

---

## Reading: whole file vs line by line

```python
text = file.read()          # entire file as one string
lines = file.readlines()    # entire file as a list of lines
for line in file:           # ONE LINE AT A TIME  ← prefer this
```

The first two load **everything into memory**. On a 10GB file they fail; the desk
isn't that big.

`for line in file` streams — it holds one line at a time and works at any size.
Make it the default and reach for `.read()` only when you know the file is small.

---

## The trailing newline

Every line read from a file ends with `\n`. That's why printing lines produces
blank lines between them — `print` adds its own newline on top of the one already
in the data.

Two fixes, and they are **not** interchangeable:

| fix | when |
|---|---|
| `print(line, end="")` | you're only displaying it |
| `line.rstrip()` | you're going to **process** it |

Use `rstrip` whenever the line is data. Otherwise the invisible `\n` rides along
into your comparisons, and `"done\n" == "done"` is `False` for reasons you cannot
see on screen. This is a classic afternoon-losing bug.

---

## `enumerate`

```python
for i, line in enumerate(file, start=1):
```

Hands you the index alongside the item. `start=1` because humans number lines
from 1 and Python counts from 0.

The alternative — keeping your own counter and remembering to increment it — is
the `while`-loop bug from Day 3 waiting to happen. `enumerate` can't forget.

---

## Writing

```python
file.write("some text\n")
```

**`write` does not add newlines.** Omit the `\n` and everything lands on one
enormous line.

---

## Sorting by a computed key

```python
sorted(dict_words.items(), key=lambda item: item[1], reverse=True)
```

**`lambda` is a function with no name**, written inline. `lambda item: item[1]` is
the same as a `def` taking `item` and returning `item[1]` — just small enough that
naming it would be noise. Parameters, return value, scope: all the same.

**What `sorted` does with it:** for every item it calls your function to compute a
**sort key**, then orders by those keys. You are not sorting the tuples — you're
sorting by a value derived from each one.

Here `item` is each `(word, count)` pair from `.items()`, so:

- `item[0]` → the word → sorts alphabetically
- `item[1]` → the count → sorts by frequency
- `reverse=True` → biggest first

The key function can return a **tuple** for multi-level sorting — e.g. count
descending, then alphabetical within equal counts.

---

## `try` / `except` — first contact

```python
def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Sorry, that file does not exist."
```

### Catch specific errors, not everything

`except Exception` is too wide a net. It catches **everything**, including typos
in your own code inside the `try`. A misspelled variable would surface as
"We got the following exception: name 'fil' is not defined" — and you'd spend an
hour investigating a file problem that isn't one.

> **Catch the errors you can actually do something about. Let the rest crash,
> loudly, where they happened.**

### The design flaw still in this version

Returning `"Sorry, that file does not exist."` means the caller receives a string
either way, with **no way to distinguish file contents from a failure message**.

Same shape as Day 4's `None` problem: the failure was handled by returning
something that *looks like* success. The function is lying about what happened.

Three options, none universally right:

- return `None` — caller must check, and forgetting means a crash further away
- return a message — as here; indistinguishable from real content
- **raise** — fails loudly at the source, caller decides

(Proper treatment on error-handling day.)

---

## The pipeline

Problems 4 and 5 together:

```
read file → clean → count → sort → write file
```

**That is the shape of essentially every data program ever written.** Every ETL
job, every preprocessing script, every dataset cleaner is this with more steps in
the middle.

Day 5's cleaning carried over unchanged — `.lower()`, `.strip(string.punctuation)`
— because the lesson doesn't change when the input gets bigger. Only the source
did.

**And `word_counts.txt`, with one `word,count` per line, is a CSV file.** Written
by hand, without knowing it.

---

## Self-test

1. What does `with` protect you from that a manual `.close()` doesn't?
2. Why is `"w"` mode dangerous, and *when* exactly does the damage happen?
3. Why specify `encoding="utf-8"` when it works fine without it on your machine?
4. Why prefer `for line in file` over `file.readlines()`?
5. Why do printed lines come out double-spaced, and what are the two fixes?
6. When must you use `.rstrip()` rather than `print(..., end="")`?
7. What is a `lambda`, and what does `key=` do in `sorted`?
8. Why is `except Exception` a bad habit?
9. What's wrong with returning `"Sorry, that file does not exist."`?
