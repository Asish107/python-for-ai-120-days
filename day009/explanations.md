# Day 009 — Errors and Exceptions

Reference notes. Read these *after* trying to recall the answer yourself.

---

## The mechanism

When something fails, Python creates an **exception object** and starts travelling
**back up the chain of function calls**, looking for someone who agreed to handle
that kind of failure.

`bigger_max` calls `find_largest`, which raises. If `find_largest` doesn't handle
it, the exception goes back to `bigger_max`. If `bigger_max` doesn't handle it,
it goes to whoever called *that* — until it reaches the top and the program stops.

**The consequence that matters:** an error does not have to be handled where it
happens. It can be caught anywhere up the chain — and the right place is usually
**where you know what to do about it**, not where it occurred.

### Reading a traceback

The traceback is a map of the path the exception took, printed with the deepest
call **last**.

> Read it bottom-up. The last line is what actually broke. The lines above it are
> how you got there.

---

## Built-in exceptions have meanings

| exception | when |
|---|---|
| `ZeroDivisionError` | divide by zero |
| `IndexError` | list index past the end |
| `ValueError` | right type, unacceptable value — `int("abc")` |
| `TypeError` | wrong type entirely — `int(None)` |
| `KeyError` | dictionary key doesn't exist |
| `FileNotFoundError` | file isn't there |
| `NameError` | name doesn't exist — usually a typo |

**Choosing the right one is how callers know what happened without reading your
source.** An empty list passed to `find_largest` is a `ValueError`, not a
`TypeError` — it's genuinely a list, its *value* is just unusable.

Note `int("12.5")` raises `ValueError`: `int()` won't accept a decimal string.
Use `float()` if that's what you meant.

---

## `try` / `except` / `else` / `finally`

```python
try:
    ...           # the risky thing
except ValueError:
    ...           # runs only for this specific failure
except TypeError:
    ...           # a different failure, handled differently
else:
    ...           # runs only if NOTHING went wrong
finally:
    ...           # runs ALWAYS — success, failure, even on the way out
```

`finally` is the cleanup slot: close the connection, release the lock, log that
we finished. It runs whether the code succeeded, failed, or raised something you
didn't catch.

**This is exactly what `with` does for you** — it's `finally: file.close()` built
into the language, which is why `with` survives a crash mid-block.

---

## Catch specific exceptions — always

`except Exception` (or a bare `except:`) catches **everything**, including your
own typos.

### The demonstration worth remembering

```python
try:
    result = int(user_input)      # user_input doesn't exist — a typo
except ValueError:
    print("Please enter a valid number.")
```

This raises `NameError`, which the `except ValueError` does **not** catch. The
program crashes and shows you the traceback. **Your bug was reported to you.**
The specific `except` caught only what it promised and let the real problem
through.

Now the bad version:

```python
try:
    result = int(user_input)
except:
    pass
```

**Nothing happens.** No crash, no message, no traceback. The program exits
successfully having done nothing. You broke your code and switched off the thing
that would have told you.

> Reading "swallowing exceptions is bad" teaches you a sentence. Watching your own
> typo vanish teaches you a reflex.

`except: pass` is everywhere in real code, usually added by someone trying to
make the errors stop — which it does in the same sense that removing the smoke
alarm stops the beeping.

**The rule:** catch the errors you can actually do something about. Let everything
else crash, loudly, where it happened.

---

## `raise` — the answer to the recurring question

Four separate times the same question came up: when something goes wrong, do I
return `None`, return a message, or crash?

### The three options

| approach | problem |
|---|---|
| `return None` | caller must remember to check; forgetting means a crash **far from the cause** (Day 4: `find_largest([])` broke `bigger_max` one layer up) |
| `return "Sorry, file not found"` | caller cannot distinguish failure from real content — the function is **lying about what happened** |
| `raise` | fails loudly, at the source, with a message and a traceback |

### The principle

> A function that can't do its job should **say so**, not invent a plausible
> answer.

`find_largest` doesn't know what an empty list *means* for your program. It isn't
its decision. It reports the problem; the caller — which has a second list to fall
back on — decides.

```python
def find_largest(numbers):
    if not numbers:
        raise ValueError("Cannot find the largest number in an empty list.")
    ...

def bigger_max(list_1, list_2):
    try:
        a = find_largest(list_1)
        b = find_largest(list_2)
        ...
    except ValueError:
        ...   # the caller decides, because the caller knows
```

**Write messages for 2am.** `"empty"` is useless in a traceback with no context.
Name what was expected and what arrived.

### When returning `None` is fine

When absence is **normal and expected**, and the caller obviously has to check —
like `dict.get()`. The distinction is whether "not found" is a routine outcome or
a broken assumption.

---

## Custom exceptions

```python
class InvalidRecordError(Exception):
    pass
```

That's the whole definition — a new type inheriting from `Exception`. Then:

```python
raise InvalidRecordError("age must be between 0 and 120, got 200")
```

```python
except InvalidRecordError:
```

**Why bother:** callers can catch *your specific failure* and let everything else
through. With `except Exception` they can't distinguish anything.

**Use them for rules only your program knows** — a record missing a field, an age
out of range, a malformed ID. Not for things Python already covers;
division by zero has an exception already.

### The trap that came up

```python
except Exception as InvalidRecordError:      # WRONG
```

`as X` gives the **caught object** a name. This catches an ordinary
`ZeroDivisionError` and calls it `InvalidRecordError` — **overwriting the class
you just defined**. Nothing was raised, nothing custom was caught.

- The name **after `except`** is the *type you're catching*.
- `as e` is only for inspecting the exception object, and you'd call it `e`, not
  the class's own name.

---

## An uncaught raise stops everything below it

```python
result = read_file("somefile.txt")   # raises, uncaught → the script dies here
```

Everything after that line never runs. If problems 4, 5 and 6 appear to do
nothing, check whether an earlier line killed the program.

---

## Self-test

1. Where does an exception go if the function it happened in doesn't catch it?
2. Which line of a traceback is what actually broke?
3. Why is an empty list a `ValueError` and not a `TypeError`?
4. What's wrong with returning `"Sorry, that file does not exist."`?
5. Why should `find_largest` raise rather than decide what to do?
6. What does `finally` guarantee, and which familiar keyword is built on it?
7. What does `except: pass` do to your own typos?
8. What does `as` mean after an exception type — and why is `as InvalidRecordError` a bug?
9. When is returning `None` on failure actually fine?
