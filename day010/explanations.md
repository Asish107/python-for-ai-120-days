# Day 010 — CSV and Structured Data

Reference notes. Read these *after* trying to recall the answer yourself.

---

## The format, and why it's a minefield

A CSV is **plain text**. Each line is a record, commas separate fields. That's the
entire specification — which is exactly the problem.

Nothing stops a field from *containing* a comma. So the format has an escape
hatch: fields containing commas get wrapped in quotes. And then a field might
contain a quote. And a field might contain a **newline**, so one record can span
several physical lines.

> **Lines are not records.** That single fact breaks every hand-rolled parser.

---

## The spreadsheet is a rendering, not the data

Numbers and Excel show you a **grid**. The file on disk is text:

```
name,age,city
Asish,29,Des Moines
```

The spreadsheet reads that text and draws the grid; on save it converts the grid
back to text, adding quotes where needed. **The grid is a view; the text is the
data.**

This is why the first file had a leading comma and three trailing ones —
`,name,Age,City,,,` — a spreadsheet export artifact from columns that once held
something. Invisible in the app, seven fields to the reader.

**When a CSV misbehaves, open it as plain text first.** The spreadsheet actively
hides the thing you need to see.

---

## `csv.reader` vs `csv.DictReader`

| | gives you | access |
|---|---|---|
| `csv.reader` | each row as a **list** | `row[1]` — positional |
| `csv.DictReader` | each row as a **dict**, keyed by the header | `row["age"]` — by name |

`csv.reader` treats the header like any other row; `DictReader` consumes it as
column names.

**Prefer `DictReader`.** If someone reorders the columns, `row["age"]` still
works. `row[2]` doesn't — and it won't tell you. It'll just start reading cities
as ages.

### The trap: DictReader silently loses duplicate columns

The first read gave 7 fields from `csv.reader` and only 4 keys from `DictReader`.
Three columns vanished — all four junk columns had the **same** header (the empty
string), and dict keys must be unique, so each overwrote the last.

**Duplicate column names lose data, silently.** Not a reason to avoid
`DictReader` — a reason to look at the header row before trusting it.

---

## Everything comes back as a string

`'29'`, not `29`. Numbers, dates, booleans — all text. **Converting is your job.**

This is Day 5's `"29" + "32"` arriving from a real file:

```python
total = 0
for row in reader:
    try:
        total += int(row["age"])
    except ValueError:
        print(f"Invalid age: {row['age']}")
```

### Normalise headers on the way in

Real CSVs arrive with `Name `, `NAME`, `name` and ` Name` all meaning the same
thing. Lowercase and strip the header as soon as you read it, so the rest of your
code never has to care what the spreadsheet happened to look like.

(Mixed `name` / `Age` / `City` is exactly how you get a `KeyError` on
`row["age"]` and lose ten minutes.)

---

## `newline=""` and `encoding="utf-8"`

On a clean file, on your own machine, **these change nothing**. They are insurance
against files you haven't met yet.

**`encoding="utf-8"`** — for anything beyond plain ASCII: `José`, a curly quote
from Word, an emoji. Without it Python guesses from the operating system, and the
guess differs on Windows.

**`newline=""`** — for fields containing line breaks. Proven live:

```
csv.reader without newline="":  '123 Main St\nSpringfield'
DictReader  with  newline="":   '123 Main St\r\nSpringfield'
```

Same file, same record, **different data**. Python quietly rewrote the contents
of a field on the way in. No error, no warning. Compare that address against a
copy from elsewhere and it won't match, for no visible reason.

`\r\n` is the Windows line ending — carriage return plus line feed. Invisible in
a spreadsheet, invisible in most editors, entirely visible to your code.

---

## The demonstration: manual split vs `csv.reader`

Same file, same two people:

| | `csv.reader` | `line.split(",")` |
|---|---|---|
| Frank | `['Frank','34','123 Main St\nSpringfield']` | `['Frank','34','"123 Main St']` **and** `['Springfield"']` |
| Grace | `['Grace','28','Springfield, Illinois']` | `['Grace','28','"Springfield',' Illinois"']` |

Three things to take from this:

**1. The manual version produced garbage and didn't complain.** Frank became two
rows, one a fragment with a single field. Grace got four fields instead of three,
city cut in half, stray `"` characters left in the data. No exception.

**2. The row count became a lie.** 8 records in, 9 rows out. Asked "how many
records are in this file," you'd answer 9 — confidently, and wrongly.

**3. Nothing downstream can detect it.** `['Springfield"']` is a perfectly valid
list. A `try/except` around the age conversion would catch the failure, print
"invalid age," skip the row — and you'd conclude one row had bad data, never that
your parser broke the file.

> **Error handling can hide a bug instead of revealing it.**

**The rule: never split a CSV on commas.** The moment real data contains a comma,
a quote, or a newline — and it will — hand-rolled parsing silently corrupts it.

---

## Building a validating reader

### Detecting a wrong field count

`DictReader` does **not** crash on rows with the wrong number of fields:

- **Too many** → extras collected under `restkey` (default `None`)
- **Too few** → missing columns come back as `restval` (default `None`)

So checking field count means checking for those, not comparing lengths.

### Line numbers

`enumerate` over the reader gives you **record** numbers; `reader.line_num` gives
**physical line** numbers. They diverge on multi-line records like Frank's.
Record numbers are usually more useful to a human.

### Shape

Two accumulators created before the loop — good rows and rejections — both
returned at the end. The Day 8 pattern, doubled.

Write the checks as **flat guard clauses**: check, record the rejection,
`continue`. If you find yourself nesting `if` inside `if` inside `if`, that's the
`bigger_max` shape from Day 4, and it gets unreadable fast.

A rejection needs the line number and the reason — and ideally the raw row, so
when someone asks "why was record 47 dropped," you can show them.

### The check that keeps you honest

```
good + rejected == number of data records in the file
```

Count the records by hand first — **records, not lines**. Frank's two physical
lines are one record.

If the numbers don't match, stop. Either the parser is silently dropping
something or counting one record as two. Neither will announce itself.

Two things that commonly break it:

- **Blank lines** — `DictReader` may skip them or hand you a row of `None`s.
  Decide whether a blank line is a rejection or nothing at all, and be consistent.
- **The trailing newline** at the end of a file — check whether it produces a
  phantom empty record.

---

## Housekeeping

Running `/usr/local/bin/python3.13` means the **global** interpreter, not the
project venv. Use `uv run solution.py`, or activate the environment. This is the
Day 1 lesson, and the whole reason Day 1 exists.

---

## Self-test

1. Why is "lines" not the same as "records" in a CSV?
2. Why prefer `DictReader` over `csv.reader`?
3. How can `DictReader` silently lose an entire column?
4. What type does every CSV field come back as, and why does that matter?
5. What does `newline=""` protect, and what does its absence do to your data?
6. Why does splitting on commas fail without raising an error?
7. How does `DictReader` signal too many / too few fields?
8. Why must `good + rejected` equal the record count, and what does a mismatch mean?
9. How can a `try/except` hide a parser bug rather than reveal it?
