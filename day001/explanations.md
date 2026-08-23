# Day 001 — Environments, Dependencies, and Why They Exist

Reference notes. Read these *after* trying to recall the answer yourself.

---

## The analogy

Your computer is a house. Installing coding tools globally is like dumping every
project's clothes, tools and paint on the **living room floor**. Start a second
project needing different tools and the two projects begin breaking each other.

A virtual environment is a **dedicated workshop room** for one project.

---

## The problem that exists before any of this

Python has one global place where packages get installed.

Project A was built last year and needs version 1.2 of some library. Project B is
new and needs version 3.0, which changed how things work. Install 3.0 → A breaks.
Install 1.2 → B breaks. **There is no arrangement where both work**, because
there is one shelf and two incompatible things want the same slot.

That is the whole problem. Everything below is a solution to it.

---

## Solution 1: isolation (the virtual environment)

`uv venv` creates a hidden `.venv` folder holding an independent Python setup for
this project alone. Anything installed for this project stays trapped inside it.

`source .venv/bin/activate` flips a switch in your terminal: *from now on, when I
say `python` or install something, use the workshop copy, not the living-room
copy.* Your prompt changes to show you're inside.

**How you prove it:** `sys.executable` prints the path of the interpreter
actually running your script. Inside the venv it points into `.venv/`. Outside it
points at the global install. Different paths = different shelves. That was the
point of Question 1.

Isolation solves **your** machine. It does not solve anyone else's.

---

## Solution 2: reproducibility (the lockfile)

You build something that works. You send it to a colleague. They install the
packages — but they install them *today*, and a library shipped a new version
last week that behaves differently. Your code breaks on their machine and neither
of you knows why.

So you need a file recording not just *which* packages, but **exactly which
versions** — including the versions of the packages your packages depend on.
That is a **lockfile**.

The difference between "install the coffee library" and "install precisely this
build of the coffee library and the exact 14 things it pulls in."

---

## Why this matters in production

On your laptop a broken environment costs an afternoon. In production:

- **The deploy that can't be repeated.** A service built six months ago needs a
  one-line hotfix. You rebuild; dependencies resolve to today's versions; the
  container won't start. You can't ship the fix and you can't reproduce the
  working version, because nothing recorded what "working" was made of.
- **The rollback that isn't a rollback.** You revert to the previous commit, but
  the commit only says "install this library" — not which version. You rolled
  back your code and not your dependencies. The bug persists.
- **"Works on my machine" as an organisational tax.** Tests pass locally, fail in
  CI. The team adds retries and shrugs. The real cost is a team that has stopped
  trusting its own signals.
- **Supply chain security.** Every package is code from a stranger running with
  your permissions. Real attacks: a maintainer's account is compromised and a
  malicious version ships; a package is registered one typo from a popular name;
  a public package shares a name with your internal one and the installer picks
  the public one because its version number is higher (*dependency confusion* —
  used to breach many large companies).
- **Audit and compliance.** You must be able to state exactly what is running,
  under what licences, with what known vulnerabilities. The term is **SBOM**
  (software bill of materials).

**A lockfile with cryptographic hashes is the defence.** It says: install exactly
this content, and if the bytes don't match, stop. Without one, "install the
latest" is a standing invitation for anyone upstream to run code on your servers.

---

## Where each tool came from

Each was a response to the previous one's failure.

- **No packaging.** Download source, copy it into place.
- **Distutils → setuptools → PyPI.** A standard way to describe and share
  packages, plus a public registry. But installing meant *executing* the
  package's setup script — arbitrary code on your machine at install time. Slow,
  non-deterministic, a security hole.
- **pip.** Made installing pleasant. Did not isolate, did not record.
- **virtualenv → `venv`.** Solved isolation. Still the foundation of everything
  today, uv included.
- **`requirements.txt` + `pip freeze`.** First stab at reproducibility, with
  three serious flaws: it's a *snapshot of a machine*, not a statement of intent;
  it can't distinguish what you asked for from what came along; and early pip had
  **no real dependency resolver** — conflicting requirements were installed one
  over the other and reported as success. Pip only gained a proper resolver in
  2020.
- **Wheels.** Pre-built packages, so installing stopped meaning "run the
  stranger's build script." Why installing a large numerical library takes
  seconds instead of compiling C for twenty minutes.
- **conda.** From the scientific world. Scientific Python is thin Python wrappers
  over C, C++ and Fortran, needing compilers and system libraries. pip manages
  only Python packages; conda manages the layer beneath too. Hence its decade of
  dominance in data science.
- **Pipenv → Poetry.** First serious "one tool for the whole project" attempts:
  intent + lockfile + environment. Poetry got the model right; resolution could
  take minutes.
- **PEP 518 / `pyproject.toml`.** One standard config file for a Python project.
  The crucial enabling step — it let a new tool be *compatible* instead of
  another island.
- **uv.** Rust, from the Ruff authors. Bet: the fragmentation was the problem and
  the slowness was solvable. Unifies environments, installing, resolving,
  locking, running and Python-version management, one to two orders of magnitude
  faster.

**Why speed is not a luxury:** when rebuilding an environment costs a second
instead of two minutes, you stop working around your tools. You rebuild clean
instead of patching a broken environment. Fast tools change behaviour.

---

## Question 1 — why `uv run` didn't show a different path

Running `deactivate` and then `uv run solution.py` still pointed at `.venv`.

`uv run` **autodetects**: it scans the working directory and its parents for a
`.venv` and forces the script to execute there, ignoring whether you manually
activated. Deliberate — your code never accidentally runs against global
packages.

To see the paths differ you must drop the `uv` prefix and let the terminal decide:
`python solution.py` in `(base)` vs. the same command after `source
.venv/bin/activate`.

**Takeaway:** use plain `python` when you want to manage environments by hand;
use `uv run` day to day and let uv handle it.

---

## Question 2 — the two files, and what each is for

`uv pip install pandas` is uv's **pip-compatibility mode**: it installs into the
environment and records nothing at the project level. `uv add pandas` is the
project workflow — it records intent *and* writes a lockfile.

### `pyproject.toml` — intent

```toml
[project]
name = "main"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pandas>=3.0.5",
]
```

A **range**: what you're willing to accept. Note this lives under `[project]` —
there is no separate `[dependencies]` section.

### `uv.lock` — resolution

Exact versions of everything, direct and transitive, with a `sha256` hash per
downloadable file. What that intent resolved to *today*, and the hashes make it
verifiable.

**Two different jobs.** `requirements.txt` from a freeze could only ever express
the second, and couldn't tell you it was the second.

### Direct vs transitive

`uv add pandas` installed four packages. Only `pandas` was asked for; `numpy`,
`python-dateutil` and `six` came along because pandas needs them (and dateutil
needs six). A freeze lists all four undifferentiated — you can't tell six months
later which ones you actually wanted.

### The wheels

Dozens of entries under numpy: `macosx`, `manylinux`, `win32`, `arm64`, `cp312`,
`cp313`, `cp314`. That's the pre-built-package idea made concrete — one file per
platform and Python version. Each carries a `sha256`: install this exact content
or refuse.

---

## Question 3 — the tzdata lesson (the real answer)

`uv.lock` contains a package the freeze did not:

```toml
{ name = "tzdata", marker = "sys_platform == 'emscripten' or sys_platform == 'win32'" }
```

**What tzdata is:** the world's timezone rules — every zone, every UTC offset,
every daylight-saving transition and its historical changes, because governments
alter these constantly. Pandas needs it for anything timezone-aware. It's data,
not code.

**Why the marker:** macOS and Linux ship this database as part of the OS, so
Python just reads it. Windows has its own incompatible timezone system.
Emscripten (Python in a browser) has no OS filesystem to read it from. So the
package is redundant on a Mac and mandatory on Windows.

**Why this is the whole point:** `uv pip freeze` photographed *this* machine — a
Mac, so no tzdata. Hand that `requirements.txt` to a Windows colleague and their
install succeeds cleanly, no errors. Then their code hits a timezone operation in
production and dies, with a traceback pointing at pandas internals rather than
anything either of you wrote.

`uv.lock` has no such failure mode: it describes the graph for *every* platform,
conditions attached.

> **A freeze records one machine's outcome. A lockfile records the rules that
> produce the right outcome on any machine.**

---

## Why this bites AI engineering hardest

- **Dependencies are enormous and binary.** A deep learning framework is a
  compiled numerical runtime tied to specific GPU driver and CUDA versions. Wrong
  combination = no error, just silent CPU fallback running a hundred times
  slower.
- **Pinning is a correctness issue, not just stability.** A minor version change
  in a numerical library can shift floating-point behaviour. Your model's outputs
  move. Nothing errors. Your evaluation numbers drift and you look at dependency
  versions last.
- **Reproducibility is the foundation of the discipline.** The core loop is
  *change one thing, measure whether it improved.* If the environment is also
  changing, you cannot attribute the difference to your change. Every experiment
  becomes uninterpretable. The lockfile is what makes measurement mean anything.
- **The ecosystem moves violently fast.** "Latest" is a target that moves weekly.
- **Training and serving are different environments.** Subtle differences between
  them cause training/serving skew — a model that scored well in training
  behaving differently in production.

---

## The correction worth remembering

Pinning does **not** mean "upgrades no longer matter." It means upgrades don't
happen *to you by surprise*. You've traded surprise breakage for a new
responsibility: nothing improves unless you deliberately update — including
security patches. A pinned project nobody touches for two years is stable *and*
quietly full of known vulnerabilities.

**Pinning moves the risk. It doesn't delete it.**
