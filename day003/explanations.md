# Day 003 — Control Flow

Reference notes. Read these *after* trying to recall the answer yourself.
Code lives in `solution.py`; this file explains the *why*.

---

## The core mechanism

A program is a list of instructions. The computer keeps a finger on the current
line, runs it, and moves the finger down. That is all a program is.

**Control flow** is the small set of ways you move the finger somewhere other
than the next line down. There are only three:

1. **Skip lines** — a condition (`if`). The finger jumps past a block when the
   question is false.
2. **Go back up** — a loop (`for`, `while`). The finger returns to the top of a
   block and runs it again.
3. **Jump away and return** — a function call. The finger leaves, runs the
   function's lines, then resumes exactly where it left off.

Everything below is a detail of one of those three.

---

## 1. Indentation is structure, not formatting

Most languages mark a block with braces. Python uses the indentation itself.

A line indented under a loop is **inside** it and runs once per round.
A line at the outer level is **outside** it and runs once, after the loop ends.

Moving one line by four spaces changed the output from *one* trailing message to
*ten* interleaved ones. Nothing else in the file changed. That is proof the
whitespace is the actual structure of the program, not decoration.

**Question to ask of any line:** how many times does this run, and what tells the
computer that?

---

## 2. `if` / `elif` / `else` — exactly one branch runs

The first version had a bug: an `if` with a bare `print` underneath it. The
second print was guarded by nothing, so it always ran. Even numbers got labelled
both even *and* odd. It looked correct only because the first test input was odd.

`else` means "when the question above was false." That makes it **one decision
with two outcomes**, not two independent statements.

`elif` extends this to more outcomes. In an `if` / `elif` / `else` chain, Python
checks each condition in order, runs the first true one, and **skips the rest
entirely**. Exactly one branch runs, always.

Zero is the case people get wrong in a negative/zero/positive check, because it
sits on the boundary between the other two. Test boundaries deliberately.

**The habit:** the first test input you reach for is usually the one that makes
the code look right. Test the case you think will break it.

---

## 3. `for` vs `while`

- **`for`** — "for each of these things." You hand it a collection; it walks
  through one item at a time and stops automatically when the items run out.
  You never write the stopping logic.
- **`while`** — "for as long as this stays true." No collection. It asks a
  question, runs the block, asks again — until the answer becomes false.

Use `for` when you know what you are walking through.
Use `while` when you only know the condition to stop on.

(Recursion is a different idea entirely — a function that calls itself. It has
nothing to do with `for`. Not covered yet.)

### The three parts of every `while` loop

You must write all three yourself:

1. **Before the loop** — create the thing you are tracking (a counter, set to 1).
2. **The condition** — a question that is true now and will eventually become
   false (`counter <= 5`).
3. **Inside the loop** — *change* the thing you are tracking (`counter += 1`).

Omit part 3 and the condition never changes, so the answer stays true forever.
That is the infinite loop. The computer is not confused — it is doing exactly
what it was told, faithfully, until you press Ctrl+C.

This is the most common `while` bug there is.

### Why `i += 1` inside a `for` does nothing

`for` reassigns the loop name at the top of every round. Any change you make to
it inside the body is overwritten immediately on the next pass.

---

## 4. `break` vs `continue`

- **`break`** — leave the loop entirely. Remaining items are never looked at.
- **`continue`** — abandon only the current round; jump back to the top and
  carry on with the next item.

Stop searching → `break`. Skip this one but keep going → `continue`.

---

## 5. Find-the-largest — the first real algorithm

Not a Python feature. A procedure that works in any language, on paper, in your
head.

**The analogy:** someone hands you cards one at a time, face down, and each one
disappears after you look at it. At the end you must name the biggest number.
You keep one number in your head — *the biggest seen so far*. Each new card, you
compare. Bigger? Replace what's in your head. Not bigger? Ignore it. At the end,
the number in your head is the answer.

**The shape:**

1. Before the loop — hold the **first item of the list**
2. The loop — for each number, if it beats what you hold, replace what you hold
3. After the loop — return what you hold

### Why the starting value must be the first item

Starting at `0` is the obvious-looking choice and it is a bug. Give it
`[-5, -12, -3]`: nothing beats zero, so it answers `0` — a number that was never
in the list.

Starting with the first item guarantees the answer is always a value that
actually existed in the data. Comparing the first item against itself on round
one is harmless.

**The general lesson:** a starting value that isn't drawn from the data can
invent an answer. This class of bug produces a plausible number instead of a
crash, which is why it survives.

### The empty-list guard

`if not numbers` reads as "if numbers is empty." Python treats certain values as
false in a question: empty list, empty string, empty dict, `0`, `None`. That is
**truthiness**.

The guard is needed because an empty list has no first item, so reaching for
`numbers[0]` would crash.

Returning `None` for an empty list is a real design decision, and a debatable
one. The caller now receives `None` where they expected a number; if they do
arithmetic with it, they crash somewhere far away from the real cause. The
alternative is raising an error immediately, which fails loudly at the source.
Neither is wrong — but choose deliberately. (Revisit when we cover error
handling.)

---

## Carried over from Day 2, used again today

- **`is` vs `==`** — `is` asks "same object, same pigeonhole?"; `==` asks "same
  value?". Use `==` for numbers and strings. `is` is essentially only for `None`.
  `is 0` appears to work because Python caches small integers (about -5 to 256),
  but it breaks silently on larger numbers. Correct for small inputs, wrong for
  large ones — the worst failure mode.
- **`def` binds a name to a function object.** Defining `even_or_odd` twice means
  the second definition replaces the first — the same label-moving behaviour as
  any other name. Functions are objects too.
- **A name that lies is worse than no name.** A function called `even_or_odd`
  that reports sign will mislead you in six weeks. Name things for what they do.

---

## Bug caught today

`num_range_check` was defined but `even_or_odd` was called. The new function
never ran, and the output showed even/odd twice with no sign check at all.

The code was correct. The wiring wasn't. Always read the output and confirm it
matches what you expected to see — not just that *something* printed.
