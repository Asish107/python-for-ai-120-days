# Day 004 — Functions

Reference notes. Read these *after* trying to recall the answer yourself.

---

## What a function actually is

The third way control flow moves: the finger **jumps away**, runs a block of
lines, then **returns to exactly where it left off**.

`def` does not run anything. It creates a function object and binds a name to it
— the same label-on-an-object move as `x = 5`. The code inside only runs when you
**call** it.

(Which is why defining `even_or_odd` twice on Day 3 replaced the first one:
functions are objects, and `def` is a name binding.)

**Why functions exist:** write a piece of logic once, name it, use it everywhere.
When it's wrong, you fix it in one place.

---

## Parameters vs arguments

- **Parameters** — the names in the `def` line. Placeholders.
- **Arguments** — the values you pass at the call site.

Calling binds each argument to its matching parameter name. That is **just
assignment**, which is why Day 2's whole model applies: the parameter becomes one
more sticky note on the caller's object.

---

## `return` vs `print` — the lesson of the day

- **`print`** shows something to a **human**. The value is gone the moment it's
  displayed.
- **`return`** hands a value back to the **code that called the function**, so it
  can be stored, passed on, or used in a calculation.

**A function that prints gives you nothing to work with. A function that returns
is a building block.**

### The mechanism behind it: implicit `None`

A function with no `return` still returns something — it returns **`None`**.
Python always hands back a value; unspecified means `None`.

So `add_num` didn't "fail to give an answer." It gave `None`, which then poisoned
the multiplication:

```
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

**Learn to read that error.** It nearly always means *something returned nothing
and you tried to use it.* And note where it surfaces — at the multiplication, not
at the function that failed to return. The error appears one step away from the
actual cause. That's what makes `None` bugs annoying to track down.

### `return` also exits immediately

Anything after a `return` never runs — the `print("Hello")` in problem 2 is dead
code.

This is why a guard clause has to `return`, not just `print`. In `bigger_max`,
printing "Both lists are empty" and carrying on meant the function **still
crashed two lines later**. Print doesn't halt anything; it's an ordinary line.

---

## Scope

Names created inside a function exist only during that call. When the function
ends, they're discarded — the sticky notes are thrown away.

```
NameError: name 'xyz' is not defined
```

Read it precisely: not *hidden*, not *private* — **gone**. It never existed
outside that call.

This is also why call 2 of `add_to_inventory` (Day 2) couldn't see call 1's list.
Local names don't survive. The *default argument* did survive — because it lived
on the function object, not in the call.

---

## Default and keyword arguments

```python
def greeting(name, greet="Hello"):
```

Three ways to call it:

| call | style |
|---|---|
| `greeting("X")` | positional, default used for `greet` |
| `greeting("X", "Y")` | positional, both supplied |
| `greeting(greet="X", name="Y")` | **keyword arguments** — order no longer matters |

Keyword arguments make call sites readable. `process(data, True, False)` tells
you nothing; `process(data, verbose=True, cache=False)` tells you everything.

**Reminder from Day 2:** never use a mutable object (`[]`, `{}`) as a default.
Defaults are created once, at `def` time. Use `None` and build the real object in
the body.

---

## Composition — why return values matter

`bigger_max` calls `find_largest` twice and uses the returned values. That's
**composition**: your code using your own code.

It only works because `find_largest` **returns**. Had it printed, `bigger_max`
would have received `None` and been unable to do anything with it.

Everything you build from here is this, stacked.

---

## The `None` chain — three ways it bit today

1. **Missing return.** `add_num` printed, so `res_1` was `None`, so `res_1 * 10`
   crashed.
2. **A guard returning `None`.** `find_largest([])` returns `None` by design. Feed
   an empty list into `bigger_max` and the comparison `None > 3` crashes — the
   `None` arrives from **your own function, one layer down**.
3. **A guard that only printed.** The message appeared and execution continued
   into the crash anyway.

This is the Day 3 open question made concrete: *return `None`, or raise an
error?* Returning `None` pushes the problem onto the caller and the crash surfaces
somewhere far from the cause. Raising fails loudly at the source. Neither is
universally right — but it should be a **decision**. (Revisit on error-handling
day.)

---

## Two habits flagged today

**The print reflex.** Problem 4 was specified as *returns a new list* and was
written with `print`. This is the most common beginner habit in Python and it
takes deliberate effort to break.

> Print is how you *look* at something while developing.
> Return is how a function *does its job*.

The test: can the result be fed into another function? If not, it isn't a
building block.

**Repetition is a smell.** The final `bigger_max` has four `print` lines saying
almost the same sentence inside nested `if`s. Repeated near-identical lines
usually mean the shape can be simpler — compute the answer first, print once at
the end. Noticing the smell matters more than fixing it today.

**Dead code:** `else: continue` at the end of a loop body does nothing. The loop
moves to the next item anyway when the block ends.

---

## Also correct today

`check_even` builds a **new** list and leaves the original untouched — a "returns
new data" function, the opposite of the mutating functions from Day 2. Knowing
which kind you're writing is the practical form of the whole mutability lesson.

---

## Self-test

1. What does a function return if it has no `return` statement?
2. What does `TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'`
   usually mean happened?
3. Why does a guard clause need `return` and not just `print`?
4. What's the difference between a parameter and an argument?
5. Why can't you print a name that was created inside a function?
6. Why is a function that prints its answer useless as a building block?
7. `bigger_max([], [1,2,3])` crashed before the guard was fixed — where did the
   `None` come from?
