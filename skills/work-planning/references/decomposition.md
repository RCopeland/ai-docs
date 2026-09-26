# Decomposition

How to cut work into chunks that ship. Read when the plan has more than a few
chunks, or when a chunk resists being split.

## Vertical, not horizontal

A chunk is **vertical** when it passes through every layer needed to produce an
observable result: storage, logic, interface, and the test that proves it.

Horizontal slicing (one chunk per layer) is the single most common
decomposition error. It produces chunks that cannot be demonstrated, no
feedback until the last one lands, and a diff that only becomes reviewable at
the end.

| Horizontal (avoid) | Vertical (prefer) |
|---|---|
| Add `users` table + migration | Register a new user and see them in the list |
| Build settings API | Change display name from the settings page |
| Build settings UI | (same chunk) |

If a layer genuinely must land first because nothing can use it yet, name the
**thin end-to-end path** that consumes it and make that the chunk.

## Splitting patterns

Work these in order; stop at the first that yields shippable chunks. This is
Richard Lawrence's pattern set, which remains the standard.

1. **Workflow steps** — split a multi-step process into the steps (create →
   review → publish). Each step ships and is usable.
2. **Operations** — a "manage X" chunk is really create / read / update /
   delete. Each is separately valuable.
3. **Business rule variations** — start with the simplest rule; add variations
   (roles, tiers, limits, jurisdictions) as later chunks.
4. **Data variations** — one format/entity/type first, then the others. e.g.
   "import CSV" before "import XLSX and EPUB".
5. **Data entry methods** — web form first, then mobile, then bulk import.
6. **Deferred performance** — ship the naive-but-correct version, then a chunk
   for the optimization once real load exists.
7. **Break out a spike** — when you cannot split because you do not understand
   the problem, the chunk is investigation, not delivery.
8. **Simple to complex** — happy path first, then error handling, then edge
   cases, each as its own chunk.
9. **Major effort** — if none of the above applies, the chunk is a project:
   re-scope it or accept a larger multi-week chunk and say so explicitly.

Pattern 7 is the escape hatch. A spike is legitimate work with a real
deliverable (an answer, a measured number, a decision) and a hard timebox.

## When the size rule breaks

The 1–3 day target exists so that progress is measurable, delays surface early,
and ownership is unambiguous. It is a heuristic, not a law. Three cases where
deviating is correct:

**Cannot split without losing integrity.** A schema migration plus its
backfill, a security fix that must ship atomically, or a protocol change with
no compatible intermediate state. Splitting would create a broken state. Let it
run to ~5 days and say in the plan *why* it is indivisible — that is different
from not having tried.

**Genuinely atomic and small.** A config change, a version bump, a one-line
fix. Padding it to a synthetic "day" makes the plan lie about its own shape.
Bucket these as a single chunk ("small fixes and configs, ~2 days") rather than
listing twelve trivial rows.

**Long-lead and external.** A vendor negotiation, a legal review, a hardware
order. The duration is real but the work is not yours and cannot be
parallelized or split. Track it as a dependency with a lead time, not as a
sized chunk — mixing calendar lead time into an effort estimate corrupts both.

What is *not* a valid reason to exceed the target: "it's easier to keep as one
story", "the ticket already exists", "splitting it feels bureaucratic".

When a chunk must stay large, split it **internally**: list the sub-steps, flag
the first point at which something is demoable, and set an interim checkpoint.
A five-day chunk with a named day-2 checkpoint survives; a five-day chunk with
no checkpoints is a two-week chunk that hasn't admitted it yet.

## Run INVEST on each chunk

- **I**ndependent — can it land without waiting on a sibling chunk?
- **N**egotiable — is the implementation open, or have you over-specified?
- **V**aluable — does something observable improve when it lands?
- **E**stimable — can you name the anchor you're estimating from?
- **S**mall — 1–3 days for one person?
- **T**estable — is there a check that goes red then green?

A chunk failing **V** or **T** will need re-splitting even if its size looks
right. A chunk failing **I** is fine if the dependency is stated in the plan —
just do not pretend it is parallelizable.

## Anti-patterns

- **Monolithic chunk** — one ticket titled "Add user profile page" that is
  really five features. Splitter's job is to catch this before a worker does.
- **Layer cake** — chunks that only make sense together.
- **Rename-only chunks** — a chunk whose deliverable is invisible to everyone
  buys no feedback. Fold it into the change that needed it.
- **Estimate laundering** — splitting a 10-day job into four 2.5-day chunks
  without changing scope. Splitting must change what can ship, not just count.
- **Fake independence** — chunks all blocked on one "foundation" chunk. Either
  make the foundation part of chunk 1 and cut it vertically, or sequence them
  honestly.
- **Spike inflation** — a "spike" with no question, no timebox, and no expected
  decision is just unestimated work wearing a disguise.
- **Done-without-evidence** — "chunk complete when the sync engine works" is
  not testable. Name the command, test, or observation.

## Sequencing

1. Order by dependency first.
2. Within unblocked chunks, order by **risk retired per day** — unknowns and
   the longest-lead-time external dependencies go early.
3. Identify the **critical path** — the chain that determines the end date.
   Report totals for that chain, not for every chunk added together.
4. Mark the **first shippable increment**: the earliest point at which the
   user can see something real. Plan that as early as honest.
