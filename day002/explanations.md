# Day 002 — Names, Objects, and Mutability

Reference notes. Read these *after* trying to recall the answer yourself.

---

## First: what "memory" even means

Your computer keeps things in two places.

**Storage** (the hard drive) is the filing cabinet. Big, slow-ish, survives being
switched off. Your `solution.py` file lives here.

**Memory** (RAM) is the desk. Smaller, much faster, and **wiped clean every time
a program ends**. This is where a program does its actual work.

Run your script and Python reads the file from the cabinet, then builds
everything — every list, string, number — on the desk. Program ends, desk
cleared. That's why data disappears unless you deliberately write it back to a
file.

### The pigeonhole picture

Picture memory as an enormous wall of numbered pigeonholes. Millions of them.

When you write `list_a = [1,2,3]`, **two separate things** happen:

1. Python finds an empty hole, builds the list, puts it there — say hole
   `4305783104`.
2. Python writes down: *the name `list_a` refers to hole `4305783104`*.

**`id()` shows you the hole number.** That's all it is.

Proof this desk is wiped between runs: the ids were `4305783104` on one run and
`4373678400` on the next. Same code, different holes, fresh memory.

---

## The core model

**A name is a sticky note, not a box.**

The object lives in a pigeonhole. The name is a label stuck to it. Name and
object are two different things.

**`b = a` does not copy anything.** It writes a second sticky note and puts it on
the *same* object. One object, two notes. Same `id()` proves it.

---

## The crux: two operations, easily confused

This is the actual lesson of the day.

- **Mutate** (`list_b.append(911)`) — reach into the object and change its
  contents. No note moves. Every name attached to that hole sees the change.
- **Rebind** (`list_b = something`) — peel the label off and stick it on a
  *different* object. The old object is untouched; other names stay on it.

> **The operation decides the outcome. The type decides which operations are
> available.**

Lists, dicts and sets can be mutated. Strings, numbers and tuples cannot — so
rebinding is your only option with them.

That is the *only* reason strings looked different from lists. Not a separate
rule — the same rule with one option unavailable.

### The experiment that proves it

Take a list and use `list_b = list_b + [911]` instead of `.append()`. You get the
**string result**: `list_a` untouched, `list_b` on a new id. Same type, opposite
outcome. The type was never the deciding factor.

### The bug that hid this

The first attempt had both lines:

```
list_b = list_b + [911]   # rebinds — link severed here
list_b.append(911)        # appends to the NEW list
```

The rebind broke the connection before the mutation happened, so `list_a` looked
untouched and the demonstration failed.

### Watch out for `+=`

It looks like plain assignment but doesn't always behave like it. On a list it
mutates in place; on a string it rebinds. When it eventually confuses you, this
is why.

---

## The three copying cases

| | outer object | inner objects |
|---|---|---|
| `b = a` (shared reference) | same | same |
| `b = a.copy()` (shallow) | **new** | same |
| `b = copy.deepcopy(a)` (deep) | **new** | **new** |

**Shallow means one level deep and no further.** Copying a list of lists builds a
new outer list, but it copies the *references* — the new outer list points at the
same inner pigeonholes. Mutate an inner list through the copy and the original
changes.

The two ids to check:

- `id(list_1)` vs `id(list_2)` — the outer objects
- `id(list_1[1])` vs `id(list_2[1])` — the inner objects

If those two answers differ from each other, you're looking at a shallow copy.
Both `False` means a genuine deep copy.

---

## Functions receive names, not copies

Passing an object into a function is **just assignment**. The parameter becomes
one more sticky note on the same hole.

So a function that appends to its parameter is appending to *your* list. No
`return` needed, no reassignment — the caller's data changed.

Not a bug in itself; sometimes it's exactly what you want. But it should be a
**decision, not an accident**.

> The habit worth building: for every function you call, know whether it
> *modifies your data* or *returns new data*.

---

## The mutable default trap

```python
def add_to_inventory(inventory=[]):   # BROKEN
```

**Timing is the whole explanation.** Python evaluates the default **once, when it
reads the `def` line** and creates the function object. One empty list, one
pigeonhole, stapled to the function — which lives as long as the program does.

`inventory` is never a fresh list. It's a note pointing at that one list. Every
call appends to the same hole. It was never going to reset, because nothing ever
creates a second list.

### The fix

```python
def add_to_inventory(inventory=None):
    if inventory is None:
        inventory = []
    inventory.append("item")
    return inventory
```

Three reasoning steps:

1. **The default can't be a list at all** — any list there has the same problem.
   `None` is not a list; nothing can accumulate in it.
2. **But the parameter still needs a default,** so use a placeholder meaning
   *"the caller gave me nothing."* It must be immutable and something nobody
   would pass legitimately. `None` exists for exactly this.
3. **Build the real list in the body.** Code in the body runs on **every call**,
   unlike the default which ran once. So a list created there is genuinely fresh.

Trace it: each call sees `inventory is None` → true → a *different* new list in a
*different* hole. Three calls, three separate `['item']`.

### Why it matters more than it looks

Your script runs for half a second. Real software doesn't.

A server **starts once and stays running for weeks**. The `def` executes at
startup, creating one list. A cart function with this bug means:

- Monday 9:00 — a customer adds a laptop.
- Monday 9:05 — a different customer opens their cart. **A stranger's laptop is
  in it.**
- By Friday, ten thousand items from every visitor.

Two disasters from one line: **data leaking between users** (a privacy breach)
and a **memory leak** — the list only grows, nothing empties it, and days later
the server runs out of memory. The crash log points at whatever allocated last,
not at the cause. People lose weeks to this.

**The bug's severity depends entirely on how long the program lives.** Harmless
in a script, catastrophic in a service. Which is why you fix it everywhere — you
don't get to know in advance which functions end up inside something
long-running.

---

## `is` vs `==`

- **`is`** — *the same object? the same pigeonhole?*
- **`==`** — *the same value?*

Use `==` for numbers, strings, anything with contents. `is` is essentially only
used with `None`, and `inventory is None` is correct precisely because there is
exactly one `None` object in a running program — identity genuinely *is* the
question.

**Why `is 0` appears to work:** Python caches small integer objects, roughly −5
to 256, because tiny numbers are used constantly. Every `0` is literally the same
object, so `is` accidentally comes out true. Past the cache it collapses — two
computed values of 1000 are separate objects and `is` returns `False` despite
equal values.

Correct for small inputs, silently wrong for large ones. The worst failure mode
there is. Modern Python emits a `SyntaxWarning` for `is` with a literal.

---

## Truthiness

Python treats certain values as false when used as a question: empty list, empty
string, empty dict, `0`, `None`. Anything non-empty is true.

So `if not numbers:` reads as *"if numbers is empty."*

---

## Floating point: why `0.1 + 0.2` isn't `0.3`

Output: `0.30000000000000004`.

Computers store numbers in binary (base 2), per the IEEE 754 standard. Decimals
like 0.1 and 0.2 **repeat infinitely in binary** — the same way 1/3 repeats
forever as 0.333… in base 10. The computer truncates to fit a fixed number of
bits, and those tiny rounding errors surface when you do arithmetic.

**Why a bank cannot use this:** losing a fraction of a cent per transaction,
across millions of automated transactions, produces real imbalances that don't
reconcile.

**The fix:** the `decimal` module, which does base-10 fixed-point arithmetic.
Pass the numbers **as strings** — `Decimal('0.1')` — because `Decimal(0.1)` would
hand it a float that's already wrong.

---

## Why any of this matters

Most bugs crash. You get a traceback, a line number, a cheap fix.

**This class doesn't crash.** Your code runs, produces numbers, and the numbers
are wrong. Nothing tells you.

Where it shows up in AI work:

- **Keeping a "before" copy of your data.** Hold the raw dataset, clean a copy,
  compare. If the copy is shallow, cleaning modifies the raw data too — you're
  comparing something against itself. It matches perfectly and tells you nothing.
- **Experiment configs.** A base config copied per experiment. If the copies are
  shallow and the settings nested, changing one changes all. You run five
  experiments that are secretly identical, get near-identical results, and
  conclude the setting doesn't matter. Completely wrong, from clean-looking
  output.
- **Functions that quietly mutate.** A preprocessing function that modifies in
  place instead of returning new data means the second function receives data
  that's already been transformed. Results drift with no visible cause.
- **Checkpoints.** A snapshot taken before something risky, so you can roll back.
  If it's shallow it isn't a snapshot — it points at the live state and changes
  as you go. Roll back and you restore the broken version. The safety net was
  never attached to anything.

You're already staring at numbers you can't verify by eye — is 0.87 accuracy
right? You have no independent way to know. That's why a bug which silently
shifts your numbers can survive for months.

---

## Self-test

1. What does `b = a` actually do?
2. Two names on one list; I append through one. Does the other change? Why?
3. Two names on one string; I add text through one. Does the other change? Why?
4. Which decides the outcome — the operation or the data type?
5. Why is this dangerous when passing data to a function?
6. When is a default argument created, and where does it live?
7. Why is `is 0` wrong but `is None` right?
