# Day 005 — Dictionaries (and Sets)

Reference notes. Read these *after* trying to recall the answer yourself.

---

## The one-line difference

- A **list** answers *"what's at position 3?"*
- A **dictionary** answers *"what's the value for this key?"*

Most real programming is the second question.

---

## The mechanism: hashing

This explains everything else about dictionaries, so learn it first.

### How a list finds something

Python starts at the front and checks each item until it matches. A thousand
items means up to a thousand comparisons. A million items, up to a million.
**A list searches.**

### How a dictionary finds something

A **hash function** is a calculation that turns a key into a number. The same
input always produces the same number.

Store `"tree" → 3`:

1. Run `"tree"` through the hash function → some big number, say 8,431,772
2. Divide by the number of available slots, take the remainder → slot 47
3. Put the value in slot 47

Look up `"tree"` later:

1. Run the **same** calculation → the **same** number → slot 47
2. Go straight there

No searching. **A dictionary calculates.**

### Why size doesn't matter

Ten entries or ten million — it's the same arithmetic and one jump. That is why
dictionaries dominate real code, and it's the answer to "why doesn't lookup get
slower as it grows?"

### Why keys must be immutable

Store a value under a list key; the calculation puts it in slot 47. Now someone
appends to that list. The contents changed, so the hash now computes slot 12.
The value is still sitting in 47 and **nothing will ever look there again**.
Lost silently, no error.

So Python only permits immutable keys: **strings, numbers, tuples**. Lists and
dicts cannot be keys.

> Day 2 and Day 5 are the same lesson. Mutability isn't a quirk of lists — it's
> the property that decides whether something can be a dictionary key at all.

**Sets work identically.** A set is essentially a dictionary with keys and no
values, which is why `x in some_set` is fast and `x in some_list` is slow, and
why a set can't contain a list.

---

## Keys should be meaningful

First attempt used `"name1" → "Asish"`, `"name2" → "Ash"`. That is a list with
extra typing — numbered slots are exactly what lists are for.

The power of a dict is that the **key is the question you want to ask**:
`"Asish" → 29` lets you ask *how old is Asish?* rather than *what's in slot 3?*

---

## The operations

| operation | what it does |
|---|---|
| `d["key"]` | look up — **raises `KeyError`** if absent |
| `d.get("key", fallback)` | look up — returns the fallback if absent |
| `d["key"] = value` | add if new, overwrite if it exists |
| `del d["key"]` | remove; returns nothing; crashes if absent |
| `d.pop("key")` | remove **and return the value**; accepts a default |
| `"key" in d` | does this key exist? |

### Brackets vs `.get` — a real decision

- Use **`d["key"]`** when a missing key means something is genuinely broken. You
  *want* the crash, loudly, at the source.
- Use **`.get(key, default)`** when absence is normal and expected.

`.get(key)` with no second argument returns `None` — and `None` propagates into
a crash one step away from the cause (Day 4). **Always supply the fallback.**

### `del` vs `pop`

Both remove. `pop` hands the value back on the way out; `del` discards it. `pop`
also takes a default so it won't crash on a missing key.

---

## Looping

```python
for key, value in d.items():
```

`.items()` gives both at once. There is also `.keys()` and `.values()`.

Looping over keys and then looking up each value inside the loop works, but it
does the lookup twice for no reason. `.items()` is the idiom.

---

## The counting pattern

The most common dictionary pattern in existence.

The problem: the first time you meet a word, its key doesn't exist yet, so
`d[word] + 1` crashes.

Three ways to solve it, in order of sophistication:

```python
# 1. explicit — write this first, so you understand the problem
if word in counts:
    counts[word] = counts[word] + 1
else:
    counts[word] = 1

# 2. .get with a default — collapses it to one line
counts[word] = counts.get(word, 0) + 1

# 3. the standard library does the whole job
from collections import Counter
counts = Counter(words)
```

Build it by hand before reaching for `Counter`. That order matters — now you know
what `Counter` is doing rather than treating it as magic.

---

## Text is filthy — the real lesson of problem 4

The counting logic was correct on the first attempt. The **input** was not.

`sentence.split()` produced `elephant.`, `right?`, `true.`, `joke!` — punctuation
attached. So `"true."` and `"true"` count as two different words, and `"joke!"`
will never match `"joke"`.

Two cleaning steps:

- `.lower()` — so `"This"` and `"this"` are the same word
- `.strip(string.punctuation)` — removes punctuation **from the ends only**,
  which correctly leaves `that's` intact

> The counting is the easy part. Cleaning the input is the work. This is true of
> essentially all data work, and it's most of what data cleaning means.

---

## Types matter: numbers stored as text

Ages written as `"29"`, `"32"` are **strings**, not numbers.

`"29" + "32"` gives `"2932"` — string concatenation glues them together instead
of adding. Sum the ages or find the oldest person and you get nonsense, not an
error.

**This is a whole category of real bug:** numbers arriving as text. Everything
looks fine until arithmetic silently produces garbage. Watch for it every time
data comes from a file, a form, or an API.

Also avoid mixing types in one dictionary's values — some ages as `"29"` and one
as `30` means every operation over that data has to handle both.

---

## Nesting is JSON

```python
people = {
    "Maya": {
        "age": 28,
        "city": "Chicago",
        "hobbies": ["reading", "painting", "hiking"]
    },
}
```

`people["Maya"]["hobbies"][1]` → `"painting"`

Read the chain left to right: `people` is a dict → give me Maya's dict → give me
her hobbies list → give me index 1.

**This shape is JSON**, and JSON is how every API and config file on earth talks
to you. Every AI API call you ever make returns exactly this. Being fluent with
the bracket chain is a load-bearing skill.

---

## Deduplicating while keeping order

```python
seen = set()
unique = []
for value in original:
    if value not in seen:
        seen.add(value)
        unique.append(value)
```

Two containers doing two different jobs:

- `seen` is a **set** — used only for the fast *"have I met this before?"* check
- `unique` is a **list** — because order matters and sets have no order

Using a list for `seen` would work and would be slow: every check would scan the
whole list. On big data that's the difference between seconds and hours.

**Choosing the right container for the question you're asking is the skill.**

---

## Self-test

1. Why doesn't dictionary lookup get slower as the dictionary grows?
2. What does a hash function do, in one sentence?
3. Why can't a list be a dictionary key?
4. When should you use `d["key"]` instead of `d.get("key")`?
5. What does `.get("key")` return when the key is missing, and why is that risky?
6. What's the difference between `del` and `pop`?
7. Why is `x in some_set` fast but `x in some_list` slow?
8. What goes wrong if ages are stored as `"29"` instead of `29`?
9. Why did the first word-count produce both `true` and `true.`?
