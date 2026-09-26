---
name: work-planning
description: Plan upcoming project work by decomposing it into right-sized, independently deliverable chunks with estimates, ranges, and a sequenced plan. Use for roadmaps, feature breakdowns, milestone plans, effort estimates, "how long will this take", or sizing a backlog.
---

# Work Planning

Turn an intent ("we should add offline sync", "plan Q3 for the API") into a
**sequenced set of deliverable chunks, each with an estimate and a stated
uncertainty range**.

## Ask before you plan

A plan is only as good as the direction under it. Before writing chunks or
numbers, run the **Direction Gate** in
[references/questions.md](references/questions.md). Read that file now — it
holds the question set, how many to ask, and when to stop asking.

Rules:

- **Ask the whole opening batch in one message, not one question at a time.**
  Batch 6–10 questions, numbered, each with your assumed default so the user
  can reply "3 and 7 are wrong, rest fine" instead of composing essays.
- **Do not start planning until the four blocking answers exist:** goal/end
  state, definition of done, scope boundary, and capacity (who + how much time).
  Missing any of these means you are writing fiction. Ask; do not assume.
- **Ask again mid-plan when a chunk reveals a fork you cannot resolve from
  evidence** — especially "is this in scope?", a choice of approach, or a
  deadline constraint that would change sequencing.
- **Stop asking when answers stop changing the plan.** If a question's answer
  would not alter chunks, sequence, or estimates, it is curiosity, not
  planning — drop it. Never pad a plan review with questions to look thorough.
- **Investigate before you ask.** Check the repo, docs, existing plans, and
  git history first. "What database are you using?" is lazy when `compose.yaml`
  answers it. Spend the user's attention only on what the codebase cannot tell you.
- **Then confirm the finished plan back once**, as a short restatement of goal,
  scope boundary, chunk count, and total — a direction check, not a question list.

If the user says "just give me a rough idea" or "don't ask, my best guess",
skip the gate, state every assumption you made explicitly in the plan under
`## Risks & assumptions`, and label it low-confidence. Never silently invent
scope on a planning task.

## Outcome contract

A plan is done when it contains, in writing:

1. **Goal + definition of done** — the observable end state, not the activity.
2. **Explicit scope boundary** — what is *out* of scope. A plan with no
   boundary is not a plan.
3. **Deliverable chunks** — each independently shippable, sized in days.
4. **Estimate + range** per chunk (optimistic / likely / pessimistic).
5. **Dependencies and critical path** — ordered, with parallelism called out.
6. **Unknowns as spikes** — anything unestimable is a stated spike, not a guess.
7. **Assumptions and risks** with the trigger that invalidates the plan.

If the user wants this as todos, convert the chunks with the `write-todos`
skill — that contract is stricter (2–5 minute worker todos) and is a
*different* granularity from plan chunks. Plan first, then split to todos.

## Sizing rule

**One chunk = one to three days for one person.** This is the target, not a law:
a chunk that cannot be split without losing testability may run to ~5 days, and
a genuinely atomic mechanical change may be hours. See
[references/decomposition.md](references/decomposition.md) for when the rule
breaks and how to handle it.

Red flags that a "chunk" is really a project: it spans more than one role, it
has the word "and" twice in its title, its estimate is "a few weeks", or you
cannot describe the evidence that proves it done in one sentence.

## How to decompose

Split **vertically** — a thin path through data, logic, and UI that a user or
caller can actually exercise — not by architectural layer. "Add the DB table",
then "add the API", then "add the UI" produces three cannot-ship chunks and no
feedback until the end.

Work the checklist in [references/decomposition.md](references/decomposition.md)
for the splitting patterns (workflow step, operations, business rules, data
variations), the INVEST test to run on each resulting chunk, and the
anti-patterns to avoid. Read it whenever the plan has more than ~5 chunks or the
user pushes back that a chunk is too big.

Always break out **spikes** for unknowns: a timeboxed investigation whose
deliverable is an answer, not code. A plan with uncertain chunks and no spikes
is hiding the uncertainty.

## Estimating

Estimate the chunk, then state the range. Two acceptable modes:

- **Quick (default):** per chunk give `likely ± spread` in days, e.g. `3d
  (2–6)`. Use when the user wants a fast directional plan.
- **Three-point:** give O/M/P per chunk and compute expected value and a
  confidence range. Use when the total feeds a commitment, a date, or a budget.

```bash
# Expected duration, std dev, and a confidence band for a plan of chunks
python3 scripts/estimate.py --unit days <<'EOF'
chunk,optimistic,likely,pessimistic
auth-token-refresh,1,2,4
sync-queue-worker,3,5,10
conflict-resolution-ui,2,4,9
EOF
```

The script uses PERT weighting `(O + 4M + P) / 6` with variance
`((P - O) / 6)²`, summed for the critical path, and reports the probability the
plan lands under a given target. It refuses inconsistent input (O > M > P).

**Never present a single number as the estimate when uncertainty is real.** An
estimate is a range plus a confidence level; a bare number is a commitment
someone will hold you to. Calibrate expectations with the reference material on
the cone of uncertainty in
[references/estimation.md](references/estimation.md) — estimates early in a
project are legitimately wide, and they should narrow as spikes close.

Estimating anchors to consider, in order of reliability:

1. **Measured history** — how long comparable work actually took here, from git
   log, ticket cycle time, or the user's memory.
2. **Reference stories** — "this is about the size of <thing we already did>".
3. **Absolute days** — weakest, but honest when nothing else exists.

Say which anchor you used. If only (3) is available, widen the range and label
the plan as low-confidence.

## Output shape

Write the plan to a file when it is more than a paragraph. Default location
`docs/plans/<date>-<slug>.md` in the target repo, unless the user names a path
or the project has its own convention (check `.pi/plans/` first). Structure:

```markdown
# <Plan title>

**Goal:** <observable end state>
**Done when:** <checkable evidence>
**Out of scope:** <explicit exclusions>
**Confidence:** <high|medium|low> — based on <anchor>

## Chunks

| # | Chunk | Deliverable (user-visible outcome) | Depends on | Est (days) | Range |
|---|-------|-----------------------------------|-----------|-----------|-------|

## Spikes

| # | Question to answer | Timebox | Blocks |
|---|-------------------|---------|--------|

## Sequence

<critical path, what runs in parallel, first shippable increment>

## Totals

<expected, p50/p80, stated assumptions>

## Risks & assumptions

| Risk | Trigger | Mitigation |
|------|---------|-----------|
```

## Rules

- **Do not estimate work you have not scoped.** If a chunk cannot be estimated,
  it becomes a spike. Guessing is worse than stating the unknown.
- **Do not inflate a total by padding every chunk.** Put buffer where the risk
  is, named. PERT's pessimistic case already carries weight; do not double-add.
- **Do not plan past the horizon you can see.** Beyond ~1–2 quarters, plan
  outcomes and themes, not chunks and days. Accuracy collapses.
- **Do not silently assume availability.** State the assumed capacity
  (people × days/week) the totals rest on; a plan without capacity is a wish.
- **Do not report a point estimate as a date.** Convert to a date only by
  dividing by committed capacity, and label the result as probabilistic.
- **Respect existing plans.** Read `docs/plans/`, `.pi/plans/`, and the backlog
  before creating a competing artifact.
- **Do not plan against a direction the user has not confirmed.** The Direction
  Gate exists to prevent confidently-estimated work on the wrong problem.
- **Do not interrogate.** Questioning is a means to a plan. If you have asked
  twice and still lack an answer that only the user holds, plan the most likely
  interpretation, flag it loudly, and let them correct you.

## Reporting back

Lead with: chunk count, expected total with range, confidence level, the
critical path, and the top unknowns. Mention the plan file path. Do not paste
the whole table into chat — summarise and link.
