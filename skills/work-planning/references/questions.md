# The Direction Gate

Questions to ask before planning, so the plan is aimed at the right problem.
Read this when starting any plan.

## Why this exists

The most expensive planning failure is not a bad estimate — it is a
well-estimated plan for the wrong thing. A plan that is 20% off is recoverable.
A plan built on an unstated assumption about scope, audience, or deadline is
wasted work and it will look confident the whole way.

## The four blocking answers

Do not produce chunks or numbers until all four are answered. They are not
optional and they cannot be inferred reliably.

| # | Question | Why it blocks |
|---|----------|---------------|
| 1 | **What is the end state?** What exists when this is done that does not exist now? | Without it you plan activity, not outcome. |
| 2 | **How will we know it's done?** What check, demo, or observation proves it? | Without it chunks have no testable edge (fails INVEST `T`). |
| 3 | **What is explicitly out of scope?** | Without it the boundary expands during execution and the estimate is meaningless. |
| 4 | **Who is doing the work, and how much time per week?** | Without it effort cannot become a date, and totals are fiction. |

If the user cannot answer #2 or #3, that itself is the finding — say so. "We
can't currently define done or the boundary" is a real planning risk and
belongs in the plan document.

## The opening batch

Send these as one numbered message. Lead with your assumed default for each so
the user can confirm or correct rather than author from scratch.

**Goal and shape**

1. **End state** — the observable result. *(assume: <your reading>)*
2. **Definition of done** — what proves it. Test? Demo? Deployed and used?
   *(assume: <your reading>)*
3. **Primary beneficiary** — end user, internal team, future maintainers? This
   changes what "valuable" means in INVEST. *(assume: <your reading>)*
4. **Why now** — the deadline, event, or pressure driving this? *(assume: none)*

**Boundary**

5. **Out of scope** — what are we deliberately not doing? *(assume: <your reading>)*
6. **Existing work** — is anything already built, in flight, or partially
   shipped that this must build on or replace? *(assume: none)*
7. **Hard constraints** — mandated stack, platform, API, licensing, or
   compatibility that chunks must respect. *(assume: existing repo conventions)*

**Capacity and horizon**

8. **Who and how much** — how many people, and realistic effective days per
   week each? *(assume: one person, ~3 effective days/week)*
9. **Horizon** — how far out should detail go before it becomes themes?
   *(assume: one quarter, detailed for the first ~6 weeks)*
10. **Texture of estimate** — quick directional, or three-point for a
    commitment? *(assume: quick with ranges)*

**Unknowns**

11. **Biggest unknowns** — what are you least sure about? These become spikes.
    *(assume: <your reading>)*
12. **External dependencies** — third parties, approvals, other teams, lead
    times? *(assume: none)*

## Investigate first

Before sending the batch, resolve everything the environment can answer:

- repository layout, stack, and conventions → read the code, `compose.yaml`,
  `package.json`, CI config
- existing plans and backlog → `docs/plans/`, `.pi/plans/`, `.pi/todos.json`,
  issue tracker if reachable
- prior art and velocity → git history for comparable work, ticket cycle times
- current state of the feature → search the codebase

Delete any question you answered yourself. A batch that asks what
`package.json` says wastes the user's attention and signals you did not look.

## When to stop

Stop asking when an answer would no longer change **chunks, sequence, or
estimates**. Test each candidate question against that: if any answer produces
the same plan, drop the question.

Signs you are over-asking:

- more than one round of follow-up questions on a small plan
- questions about implementation detail that chunks are supposed to leave open
  ("negotiable" in INVEST — do not over-specify)
- questions whose answers you could state as an assumption instead
- asking about work that belongs to a later horizon

Signs you are under-asking:

- you cannot write the "Out of scope" line
- every chunk is estimated from absolute judgment with no anchor
- you are guessing at capacity
- the plan has no spikes despite the user clearly being unsure

## Handling non-answers

- **User says "just rough it"** → skip the gate, proceed, and list every
  assumption in the plan's `## Risks & assumptions` table. Label confidence low.
- **User doesn't know** → that is the answer. Convert it to a spike chunk and
  record the open question in the plan.
- **User gives a contradictory answer** (e.g. a date impossible at the stated
  capacity) → surface the conflict with the arithmetic before planning. Do not
  quietly absorb it into a padded estimate.
- **Two rounds and still stuck** → pick the most likely interpretation, state
  it prominently at the top of the plan, and plan it. Iterating beats waiting.

## Confirming the finished plan

After planning, close the loop with one short message — not another
questionnaire:

> Goal: X. Done when: Y. Out of scope: Z. **7 chunks, ~18 days expected
> (80% by 24), one spike on <unknown>.** Critical path is B→D→F. Plan at
> `<path>`.

That is a direction check. The user either confirms or redirects, and either
outcome is cheap at that point.
