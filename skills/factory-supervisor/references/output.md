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

## Reviewer assignment

The supervisor never assigns a reviewer. Every PR it produces waits for the
captain to assign one by hand, or for a separate automation to do it. There is
no lane file, no routing table, and nothing for a repository to adopt.

That makes the queue depth the only thing standing between the factory and an
unreviewed merge, which is why the cap is not optional and why the size budget
matters more here than it would with automated routing. If you are assigning
reviewers yourself, the two numbers that set your load are how many PRs are
waiting and how big each one is.

### Tier your own attention, not the router

Reviewing every PR with equal care does not scale, and reviewing them all
casually defeats the purpose. Since assignment is manual, the useful judgment is
yours to make at assignment time, not something to encode in a file:

- **Cheap to verify, low blast radius** — dependency bumps, docs, copy, generated
  clients, another instance of a pattern you have already approved. If CI is
  green and the diff matches the pattern, these can clear quickly.
- **Ordinary single-module work with strong tests** — read the evidence: what
  changed, what proves it. Read the code when the evidence is thin.
- **Crosses a boundary** — public APIs, shared libraries, performance-sensitive
  paths, anything touching more than one module. Read the code.
- **Worth real care** — authentication, authorisation, payments, migrations,
  secrets, CI configuration. Read the code closely, and ideally not alone.

Two habits keep this honest. First, let a change class earn a cheaper treatment
over a run of clean merges, and drop it back the moment one reverts or escapes a
defect — a class that gets cheap treatment in a busy week is how unreviewed
merges start. Second, keep the size budget tight, because a small PR is what
makes the cheaper treatment defensible in the first place.

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
anything, track these, weekly:

| Metric | Definition | Act when |
|---|---|---|
| Arrival rate | Non-draft PRs opened per working day | Exceeds review throughput two weeks running |
| Review throughput | PRs reaching merge or close after review, per working day | Falls while arrivals hold steady |
| Queue depth | Open non-draft PRs with no approval — what the gate counts | Sits at the cap more than two days |
| Time to first review | Opened to first human review, median and p90 | Median exceeds half a working day |
| Time in review | Opened to merge, median and p90 | p90 exceeds target by 50% |
| PR size | Changed lines excluding lockfiles and snapshots, median | Median rises two weeks running |
| Unreviewed merges | Share of merges with no human review | Any merge the captain did not review |

Keep PR size next to time in review. They correct each other: a team measured on
time in review alone will split changes past the point of usefulness.

## What the supervisor must never do

- Merge anything. The captain is the merge authority, always, and no auto-merge
  tier exists. The reviewer's `APPROVED` and the publisher's PR are inputs to
  that decision, not substitutes for it.
- Choose a reviewer.
- Relax the standard or raise the cap to clear a queue. Lower concurrency
  instead.
- Let a child re-queue into a failing merge queue.