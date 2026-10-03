# Output

The factory's other half. Intake decides what enters; this decides what leaves,
and how fast.

The failure this file exists to prevent is not bad code. It is *unreviewed*
code. Generation got cheap and reading did not, so a factory with no output
controls does not produce more shipped work — it produces a review backlog, and
a backlog large enough that the captain starts approving without reading. Every
control below protects the captain's attention, which is the actual constraint.

Read this at DISPATCH and SUPERVISE.

## The WIP cap

The factory produces PRs. It does not produce reviewers.

Little's law gives the cap directly:

```
WIP = review throughput  x  target time in review
```

Measure how many PRs you actually finish reviewing per working day. Pick the
time in review you are willing to tolerate. The product is the cap.

Default **12**, set by `REVIEW_WIP_CAP`. With throughput around 12/day and a
target of one working day, 12 is the number. Revisit it every two weeks: it is
derived from throughput, so it moves when throughput moves. A cap you set once
and never revise is decoration.

Checked with [`../scripts/queue-depth.sh`](../scripts/queue-depth.sh), which
counts open, non-draft, not-yet-approved PRs. Approved-but-unmerged PRs do not
count — they are no longer waiting on a reader. It exits `0` when dispatch is
allowed, `1` when the queue is full, and `3` when it could not read the queue at
all. Treat `3` as unknown, never as full.

**The cap blocks dispatch, never PR creation.** If the factory stops an agent
from *opening* a PR, the work does not disappear; it sits in a branch nobody can
see, which is the same inventory in a worse place. Blocking dispatch keeps the
work visible in the source, where it can be reprioritised or dropped.

So the gate goes in front of the spawn, not in front of the publish. A held
dispatch is recorded as a `dispatch.held` event, distinct from `task.failed`,
and reported batched in ESCALATE.

### The math has a cliff

Waiting time does not grow linearly as utilisation approaches 1. It explodes. A
team whose reviewers are fully loaded waits a long time even when the arithmetic
says the queue should drain. Plan for review to be busy roughly three quarters
of the time; treat more than that as a queue about to jam. When it jams, lower
concurrency — do not lower the bar.

## PR size budget

Small PRs are the cheapest review capacity available: faster to read, easier to
pin a fault in, and clean to revert.

**Target <= 400 changed lines**, excluding lockfiles and snapshots. That is the
no-history default. The real number is the size below which roughly three
quarters of your human-reviewed PRs already fall — measure it once you have
history.

CI enforces it, with an escape hatch the captain controls. Never a hard wall
with no override, and never an override the child can grant itself.

The failure mode to reject explicitly: **four 390-line PRs that only make sense
together are one 1,560-line PR with extra overhead.** A split only counts if
each PR passes the suite on its own and states a single concern. A stack that
fails that test is rejected and returns as one large PR — which the captain then
sees, rather than a pile of interdependent fragments.

## Review lanes

Not every PR deserves the same reader. The lanes decide *which* PRs reach a human
at all, and the table lives in the repo — `docs/review-lanes.md`, committed next
to `CODEOWNERS` — so the paths decide, not the supervisor.

Copy [`../templates/review-lanes.md`](../templates/review-lanes.md) into the
repository and fill it in. The four lanes:

| Lane | Contents | Gate before merge | Who signs off |
|---|---|---|---|
| **A** Green pipeline | Dependency bumps, docs, copy, generated clients, changes matching an already-approved pattern | Types, tests, lint, size budget pass; automated reviewer raises no blocking finding | The pipeline; captain samples a few weekly |
| **B** Automated + sampled human | Ordinary feature and bug-fix work inside one module, strong tests | Lane A gates plus a human reading the evidence bundle; code read only when the evidence is thin | One reviewer, assigned by load |
| **C** Code owner | Public APIs, shared libraries, performance-sensitive paths, anything crossing module boundaries | Lanes A and B plus a code owner's approval | The owning team via `CODEOWNERS` |
| **D** Two humans, code read | Authentication and authorisation, payments, migrations, secrets, CI configuration, `.github/` | All of the above plus **two** approvals | Two humans |

### Lane A starts empty

This is the rule that makes lanes safe. A class of change earns its way into
Lane A only after a run of merges with no reverts and no escaped defects, and
falls back out to Lane B after a single revert or escaped defect.

A lane that starts populated is just a permission you granted yourself in a busy
week. Keep lane membership in the committed table, and keep it under review.

### Why lanes solve the reviewer problem

The supervisor is forbidden from assigning a reviewer, because choosing one
would mean inventing a name. Lanes dissolve that: **the repository decides**.
The changed paths determine the lane, `CODEOWNERS` supplies the humans, and the
supervisor only reads the answer.

If `docs/review-lanes.md` is absent from a repository, the child opens the PR
without a reviewer and says so — it does not guess a lane.

## Merge-queue discipline

The merge queue is repository infrastructure, not something this skill runs, but
it shapes what the factory should do.

**Batching is the throughput lever.** Testing N PRs in one CI run buys roughly N
times the throughput. This is where capacity actually comes from.

**Flake cascade is the most expensive event in the system.** One red test
invalidates the speculative state every queued PR was tested against, and the
queue restarts from the failure. Its frequency is set by the flake rate, not by
code quality.

**Agents must not retry into oblivion.** A human who sees a spurious failure
sighs, re-runs, and mentions it in chat. An agent told to get the PR merged
re-queues the same change repeatedly, burning a full CI run each time and
re-triggering the cascade for everything behind it. Retries that were mildly
wasteful at human frequency become a denial of service at agent frequency.

So children get one explicit instruction: **on a merge-queue or batch failure,
report the failure to the supervisor and stop. Do not re-queue.** The supervisor
batches it into ESCALATE and the captain decides.

## Metrics worth keeping

Throughput counts are easy to game and say nothing about the queue. If you track
anything, track these, weekly, split by lane:

| Metric | Definition | Act when |
|---|---|---|
| Arrival rate | Non-draft PRs opened per working day | Exceeds review throughput two weeks running |
| Review throughput | PRs reaching merge or close after review, per working day | Falls while arrivals hold steady |
| Queue depth | Open non-draft PRs with no approval — what the gate counts | Sits at the cap more than two days |
| Time to first review | Opened to first human review, median and p90 | Median exceeds half a working day |
| Time in review | Opened to merge, median and p90 | p90 exceeds target by 50% |
| PR size | Changed lines excluding lockfiles and snapshots, median | Median rises two weeks running |
| Unreviewed merges | Share of merges with no human review outside Lane A | Any merge outside Lane A has no review |

Keep PR size next to time in review. They correct each other: a team measured on
time in review alone will split changes past the point of usefulness.

## What the supervisor must never do

- Merge anything. The captain is the merge authority, always, and no auto-merge
  tier exists. The reviewer's `APPROVED` and the publisher's PR are inputs to
  that decision, not substitutes for it.
- Choose a reviewer.
- Relax a lane or raise the cap to clear a queue. Lower concurrency instead.
- Let a child re-queue into a failing merge queue.