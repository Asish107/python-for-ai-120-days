# Day 008 — Comprehensions

Reference notes. Read these *after* trying to recall the answer yourself.

---

## First: the accumulator pattern

Problem 1 took five attempts, and none of them were about comprehensions. They
were about **the most reused structure in programming**:

```
line 1:  def squares(numbers):
line 2:      squared = []              ← create BEFORE the loop, inside the function
line 3:      for i in numbers:
line 4:          squared.append(i * i) ← build INSIDE the loop
line 5:      return squared            ← return AFTER the loop
```

Three parts, and **the indentation is what assigns them**. Line 2 runs once. Line
4 runs once per item. Line 5 runs once, at the end.

Same shape as `find_largest` (Day 3), the `while` counter (Day 3), and the
word-count dictionary (Day 5).

### The four ways it went wrong — each worth recognising

| mistake | what happened |
|---|---|
| `print` instead of collecting | nothing was built; the function returned `None` |
| `return` **inside** the loop | exited on the first item; 3 of 4 numbers never processed |
| no container at all | `result = i*i` **overwrites** each pass; only the last value survived |
| container **inside** the loop | recreated empty every pass; four empty lists, all discarded |
| container at **module level** | one list shared across all calls, accumulating forever |

That last one is **the Day 2 mutable-default bug in a new costume** — one object,
created once, shared by every call. Call the function twice and the second result
contains the first call's data. Same mechanism, different hiding place.

> **Assigning replaces. Appending accumulates.** That distinction is the pattern.

---

## What a comprehension actually is

Not a new capability — **the same three-part loop, rearranged** so the result
comes first and the machinery follows.

```python
squared = []
for i in numbers:
    squared.append(i * i)
return squared
```

```python
return [i * i for i in numbers]
```

Read it aloud in this order:

1. **what I want** — `i * i`
2. **what I'm looping over** — `for i in numbers`
3. **what I'm filtering on** — `if ...`

The container is created for you. Once you read them in that order they stop
looking like noise.

---

## The four kinds

```python
[x * x for x in nums]                    # list
{name: info["city"] for name, info in people.items()}   # dict
{len(w) for w in words}                  # set — dedupes for free
(len(w) for w in words)                  # generator — see below
```

### Filtering

```python
[n for n in nums if n % 2 == 0]          # condition at the END
[n * n for n in nums if n % 2 == 0]      # transform at the FRONT, condition at the END
```

**Transformation in front, filter at the back.** Two different jobs, two
different positions.

### Comprehensions compose

```python
evens = [n for n in nums if n % 2 == 0]
squares = [n * n for n in evens]          # build from the previous result
```

Better than filtering the same source list twice.

### If you unpack it, use it

```python
{key: people[key]["city"] for key, value in people.items()}   # value unpacked, then ignored
{name: info["city"] for name, info in people.items()}         # better
```

`.items()` already handed you the value. Going back to `people[key]` does the
lookup twice. Unpacking and then re-indexing means you didn't trust what you
already had.

Also: `name` / `info` beat `key` / `value` — names should say what they hold.

---

## Sets dedupe for free

```python
{len(word) for word in sentence.split()}
```

Day 5's deduplication took a `seen` set, a result list, a loop, a membership
check and two appends — six lines. This is one, and the duplicate collapsing is
automatic because **a set cannot contain duplicates** (hashing again: same value,
same slot).

Trade-off: sets have no order. Use one when order doesn't matter; use Day 5's
loop when it does.

---

## Generator expressions

```python
[len(w) for w in words]     # brackets  → builds the whole list, now
(len(w) for w in words)     # parens    → builds nothing; yields one item on demand
```

The list version puts every item in memory at once. Ten million words means ten
million items on the desk.

The generator is **a set of instructions**, not a result. It produces one item
each time something asks for the next. Memory holds one item, not ten million.

### When you can drop the brackets entirely

Functions that consume items one at a time — `set()`, `sum()`, `join()`,
`Counter()`, `max()`, `any()` — don't need a list:

```python
"".join(char.lower() for char in text if char.isalnum())
Counter(word.lower().strip(string.punctuation) for word in sentence.split())
```

**It's a preference, not a requirement.** Brackets would work too — they'd just
build the whole list first and throw it away. Same answer, more memory. On a
sentence it's irrelevant; on a large file it's the difference between running and
not running.

> **If the thing is consumed once, immediately, use a generator. If you need to
> keep it — index it, loop twice, check its length — build the list.**

Same reasoning as `for line in file` beating `readlines()` on Day 7.

---

## When NOT to use one

The deliberately bad version:

```python
result = [word.upper() for sentence in sentences if sentence.strip()
          for word in sentence.split() if len(word) > 3
          and word.lower() not in {"the", "and"}]
```

Versus the loop: six lines, readable top to bottom, and you can set a breakpoint
inside it.

Note also that the loops appear **left to right in the same order as the nested
version** — `for sentence` then `for word`. Most people expect the inner one
first. That mismatch is part of why nested comprehensions are hard to read even
when you know the rules.

**A working guideline:** one loop, at most one condition, fits comfortably on one
line. A second loop or a second condition → use the loop.

Comprehensions are for simple transformations, not for showing off.

---

## return vs print — the rule

This came up for the fourth and fifth time today, so here it is plainly:

> **Functions return. The top level of your script prints.**

```python
evens, squares = even_nums([4,5,6,7])
print(evens)
```

**Why:** the function doesn't know what you'll want later. Today you print it;
tomorrow you write it to a file, or feed it onward, or sum it. Returning keeps
every option open. Printing closes all but one.

**The exception:** functions whose entire purpose is display — `greeting`,
`print_report`. The test is the name: does it describe a *calculation* or an act
of *showing*?

**The mechanical check:** *could I feed this result into another function?*
If no, you've built a dead end.

Printing inside a function while debugging is normal. The rule is that it's
scaffolding, and scaffolding comes down before the thing is finished.

---

## Two bugs that "worked"

**The list-of-characters palindrome.** The cleaning comprehension was never
joined, so `cleaned` was `['a','m','a','n',...]` rather than a string. The
palindrome check *still returned the right answer*, because lists support `[::-1]`
and `==` exactly like strings. Correct answer, wrong type — the function returned
a list where its caller expected text.

**Shadowing a built-in.** `def squares(list):` hides the built-in `list` for the
entire function, so `list(...)` inside it would crash. Python allows it silently.
Same risk with `dict`, `str`, `set`, `sum`, `max`, `id`, `type`, `input`. Your
editor usually tints built-ins a different colour — that tint is the warning.

---

## Self-test

1. What are the three parts of the accumulator pattern, and where does each go?
2. What's the difference between `result = x` and `result.append(x)` in a loop?
3. Why does a `return` inside a loop usually break things?
4. In a comprehension, where does the transformation go and where does the filter?
5. What does `[...]` build that `(...)` does not?
6. When can you drop the brackets when passing a comprehension to a function?
7. Why does `{len(w) for w in words}` need no deduplication code?
8. What's your rule for when a comprehension is the wrong choice?
9. Why is `def squares(list):` a bad idea?
