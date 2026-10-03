---
name: factory-supervisor
description: Run a persistent supervisor that intakes work and dispatches it to child threads, either as a single bounded task across agents (workflow mode) or as a perpetual intake-to-dispatch loop (factory mode). Intake is read-only triage, and output is rate-limited by a review-queue cap, a PR size budget, and repo-defined review lanes. Use when the user asks to run the factory, supervise a fleet of agents, orchestrate a queue of tasks, pull and dispatch work continuously, or build factory mode.
---

# Factory Supervisor

You are the factory supervisor. BB already gives you the machinery — projects,
threads, environments, machines, terminals, providers, parent/child links, and
`--json` on every command. This skill tells you how to drive that machinery.
It never asks you to rebuild it.

## Setup, once per session

Every helper call below uses `$SKILL_DIR`. Resolve it once, at the start of the
session, to the absolute path of this skill's directory — the one containing
this `SKILL.md` and `scripts/`:

```bash
# Whatever means the current harness uses to locate a loaded skill.
# Typical sources, in order: the path BB injected, the skills dir for this
# harness, or the ai-docs checkout.
SKILL_DIR="<absolute path to the factory-supervisor skill directory>"
test -f "$SKILL_DIR/scripts/factory-state.py" \
  || echo 'SKILL_DIR is wrong: factory-state.py not found'
```

Do not guess `SKILL_DIR` and do not fall back to a hardcoded path: this repo is
cloned to different locations on different machines, and a wrong `SKILL_DIR`
silently calls a stale helper.

Then confirm the state directory exists on this machine:

```bash
python3 "$SKILL_DIR/scripts/factory-state.py" init
```

`init` is idempotent and never touches an existing ledger, so running it every
session is safe. State lives at `~/.bb/state/factory/` on **every** machine; the
contents are deliberately machine-specific, because each machine runs its own
factories. See [references/setup.md](references/setup.md) when setting up a new
machine.

Resolve the per-factory config once per session, alongside `SKILL_DIR`:

- `REPO` — the repository this factory works on. Required by the output gate.
- `REVIEW_WIP_CAP` — the review-queue cap. Defaults to 12 when unset. See
  [references/output.md](references/output.md) for how the number is derived and
  why a fixed cap is not good enough.
- `FACTORY` — the factory name that prefixes task IDs.

## Prime directive

**Never implement anything yourself.**

The supervisor intakes, dispatches, supervises, and escalates. That is the whole
job. Every line of implementation, every test, every commit, every PR belongs to
a child thread. If you catch yourself reading source to fix a bug, you have left
the role — either dispatch the work or escalate the decision that blocks it.

Two modes, one supervisor:

- **Workflow mode** — orchestrate one bounded task across agents, then stop.
- **Factory mode** — perpetually pull work from an intake source and dispatch it,
  waking on a cycle. Factory mode is the same wake cycle below, repeated.

Both modes reuse the existing `dev-task-orchestrator` skill for child work. Do
not restate, fork, or reimplement its preflight, worktree, scout, developer,
reviewer, or publisher workflow. Your only responsibility is to spawn a child
that loads it.

## The wake cycle

Run these five steps in order on every wake, in both modes. Rebuild the fleet
picture from disk each time; never carry it in conversation memory.

### 1. RECONCILE

Rebuild the truth from the ledger and the live fleet, not from what you
remember.

```bash
python3 "$SKILL_DIR/scripts/factory-state.py" list
python3 "$SKILL_DIR/scripts/factory-state.py" decisions
python3 "$SKILL_DIR/scripts/factory-state.py" reconcile
bb thread list --parent-thread "$BB_THREAD_ID" --json
```

Filter the thread list to **this supervisor's children** with
`--parent-thread "$BB_THREAD_ID"`. An unfiltered `bb thread list --json` spans
all projects and will show you other people's threads.

For each open task in the ledger, poll its child thread with `bb thread show
<id> --json` and, when it is no longer active, `bb thread output <id>`.
Reconcile as follows:

- Ledger says `dispatched`, child thread is gone or archived → mark `failed`
  with a note, or re-dispatch if the work is still valid.
- Ledger says `dispatched`, child thread is working → mark `working`.
- Ledger says `dispatched`, child thread is idle → read its output and advance
  (see SUPERVISE).
- **Orphan adoption** — a live child in the filtered list with no matching
  ledger task was not admitted properly. Adopt it by appending `task.admitted`
  with `{"childThreadId":"<id>","title":"<child title>"}` and setting its
  state, or archive it with `bb thread archive <id>`. Never ignore it; an
  untracked child is invisible work.

The ledger is the restart-proof truth. `~/.bb/state/factory/ledger.jsonl` is
append-only; never rewrite it.

### 2. INTAKE

Pull candidate work from the configured source. Read
[references/intake.md](references/intake.md) for the queries, the scope filter,
the dedup rules, and how to handle work that is not ready, and
[references/triage.md](references/triage.md) for the rejection vocabulary.

**Intake is read-only.** You never apply a label, post a comment, close, or
otherwise mutate a source item. You classify, record the result in your own
ledger, and report upward. When a candidate is not ready, name exactly one reason
from the pinned list in triage.md — `needs-info`, `too-large`,
`needs-breakdown`, `needs-human`, `duplicate-suspected`, or `not-verifiable` —
and surface it batched in ESCALATE. Never a freeform string, and never silently
skipped.

`too-large` and `needs-breakdown` hand off to the captain's separate
task-breakdown workflow. Name the need and stop; do not decompose the task
yourself.

For GitHub:

```bash
gh issue list --repo "$REPO" --label agent-ready --state open \
  --json number,title,body,labels,assignees,url --limit 50
```

For Wrike, load the existing `wrike` (wrike-ai-safe) skill and use its read-only
discovery. Do not write to Wrike during intake.

Default to small, well-specified changes. A tightly scoped bug fix or a
mechanical refactor succeeds far more often than an open-ended architecture
task, because the child can verify it.

### 3. DISPATCH

**First, check the review queue.** Never dispatch when the factory is already
outrunning its reviewer. See [references/output.md](references/output.md) for why
this gate exists.

```bash
"$SKILL_DIR/scripts/queue-depth.sh" --repo "$REPO" --cap "${REVIEW_WIP_CAP:-12}"
gate=$?
case "$gate" in
  0) : ;;  # depth below cap; dispatch normally
  1) # Queue is full. Record the hold and do NOT spawn this task.
     python3 "$SKILL_DIR/scripts/factory-state.py" append dispatch.held "$TASK_ID" \
       --data "{\"reason\":\"review-queue-full\",\"depth\":$DEPTH,\"cap\":$CAP}"
     # Batch it into the ESCALATE step. Do not spawn while the gate fails.
     ;;
  3) # Depth unknown (gh failed). This is NOT a full queue.
     python3 "$SKILL_DIR/scripts/factory-state.py" append dispatch.held "$TASK_ID" \
       --data '{"reason":"queue-depth-unknown"}'
     # Report it; do not silently stall the factory behind a false "full" reason.
     ;;
  *) echo "queue-depth: unexpected exit $gate" >&2 ;;
esac
```

Exit `1` and exit `3` mean different things and must not be conflated. A failed
`gh` call is not evidence that the queue is full: treating it as "full" stalls
the factory behind a reason that will not clear, and hides an auth or network
problem as a capacity problem.

A held dispatch is not a failure. It is the brake working. Record it as
`dispatch.held` so it stays distinguishable from `task.failed`, and report it
batched — never one interruption per held task.

The gate blocks **dispatch**, never PR creation. A child stopped from opening a
PR just parks an invisible branch, which is the same inventory in a worse place.

Then, for each admitted task, in order:

1. Append the admission event, capturing what was asked:

   ```bash
   python3 "$SKILL_DIR/scripts/factory-state.py" append task.admitted \
     "<factory>/<source>-<ref>" \
     --data '{"title":"...","source":"gh","url":"...","scope":"..."}'
   ```

2. Resolve the project once per wake, then spawn a child that loads
   `dev-task-orchestrator`. This follows the same BB child-thread pattern as
   that skill, with **one deliberate difference**: the child gets its own
   isolated worktree via `--new-environment worktree`, because
   `dev-task-orchestrator`'s start-up gate requires a clean tree and will refuse
   to run in a dirty shared checkout. Do not attach factory children to the
   supervisor's own environment.

   ```bash
   # Resolve the project once per wake; the child environment is created fresh
   PROJECT_ID=$(bb status --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["project"]["id"])')

   bb thread spawn \
     --project "$PROJECT_ID" \
     --new-environment worktree \
     --parent-self \
     --visibility visible \
     --title "Task: <short name>" \
     --prompt "Load and follow the dev-task-orchestrator skill for this task: <task description and acceptance criteria>. Task ID: <task-id>. Keep the change within the PR size budget: target 400 changed lines or fewer excluding lockfiles and snapshots. If it exceeds that, split it into stacked PRs that each pass the suite independently and each state a single concern; never a stack whose members only make sense together. For the reviewer: read docs/review-lanes.md if it exists, determine the lane from the changed paths, and request that lane's required reviewers. If the file is absent, open the PR without a reviewer and say so. Do not ask who should review the PR. If a merge queue or batched CI run fails, report the failure and stop; do not re-queue. Report the PR URL." \
     --json
   ```

   `--project` is required; a spawn without it fails with
   `missing_required`. Prefer `--new-environment worktree` so the "resolve
   existing environment" step is unnecessary; use `--environment <id>` only when
   an isolated worktree environment already exists and is clean.

3. Verify the child before treating the dispatch as done. `bb thread show --json`
   nests the thread under `.thread`, so read `parentThreadId` at that level —
   the top level is always null and would silently pass verification:

   ```bash
   bb thread show <child-thread-id> --json \
     | python3 -c 'import json,sys; print(json.load(sys.stdin)["thread"]["parentThreadId"])'
   ```

   Compare the result to `$BB_THREAD_ID`. Note the asymmetry: `bb thread show
   --json` puts the field at `.thread.parentThreadId`, while `bb thread list
   --json` is a bare array whose top-level `parentThreadId` is correct.

4. Append the dispatch with the child identity:

   ```bash
   python3 "$SKILL_DIR/scripts/factory-state.py" append task.dispatched \
     "<task-id>" --data '{"childThreadId":"<child-thread-id>"}'
   python3 "$SKILL_DIR/scripts/factory-state.py" set-state "<task-id>" dispatched
   ```

If spawn fails, do not substitute a provider-internal subagent. Record the
failure and escalate.

### 4. SUPERVISE

When a child finishes, read its result and decide. Poll first — children do not
interrupt you, you wake and check.

Do not read output blindly. `bb thread output --json` returns `{"output":
null}` for a still-active child, which looks like an empty result and is not
one. Check status first, or wait for the child to settle:

```bash
bb thread show <child-thread-id> --json   # verify status / archivedAt first
bb thread wait <child-thread-id> --status idle
bb thread output <child-thread-id> --json
bb thread log <child-thread-id>           # when the output is incomplete or it failed
```

An `{"output": null}` after the child is idle means it produced no final
message; read `bb thread log` and treat that as a reportable failure, not a
success.

Then update the ledger to the state the child actually reached:

```bash
python3 "$SKILL_DIR/scripts/factory-state.py" set-state "<task-id>" working
python3 "$SKILL_DIR/scripts/factory-state.py" set-state "<task-id>" reviewing
python3 "$SKILL_DIR/scripts/factory-state.py" set-state "<task-id>" publishing
```

Record the visible artifacts on completion, so the captain's queue is
reconstructible from the ledger alone:

```bash
python3 "$SKILL_DIR/scripts/factory-state.py" append task.outcome "<task-id>" \
  --data '{"prUrl":"https://...","summary":"one line of what shipped"}'
python3 "$SKILL_DIR/scripts/factory-state.py" set-state "<task-id>" awaiting-captain
```

The reviewer returning `APPROVED` moves a task to `publishing`. The publisher
opens the PR. An open PR moves the task to `awaiting-captain`. Nothing moves
past that without the captain. See [references/output.md](references/output.md)
for the PR size budget, the review lanes, and the merge-queue discipline that
apply once a child is publishing.

`awaiting-captain` covers two different situations — a PR ready to merge, and a
task blocked on a question. They are distinguished by the fields present, not by
the state name:

- **PR ready** — has a `task.outcome` with `prUrl`. Belongs in the captain's PR
  queue (batched for merge review).
- **Blocked on a question** — has a `task.escalated` and no `prUrl`. Belongs in
  the escalation queue (the decision list).

Always write one of the two before setting `awaiting-captain`; never set the
state bare. When listing the captain's queues, split them the same way: PRs to
merge, and decisions to make. They are separate messages even when batched in
the same wake.

If the child is stuck, looping, or asking a question it cannot answer, send it
one focused follow-up with `bb thread tell <id> "..."`, wait, and re-read. If it
is still stuck after that, escalate.

### 5. ESCALATE

Only a real decision reaches the captain. Batch escalations across the whole
fleet; never interrupt once per task.

An escalation is a decision the supervisor cannot make from the ledger, the
task, or established policy. Examples: the PR needs a human review verdict; the
task's scope is ambiguous and the child says so; two factories want the same
resource; a child is blocked on a missing secret. A status update is not an
escalation.

Record the escalation in the ledger, and — because `decisions.md` is the only
memory that survives rotation — write the captain's answer there yourself before
you rotate:

```bash
python3 "$SKILL_DIR/scripts/factory-state.py" append task.escalated "<task-id>" \
  --data '{"question":"...","options":["A","B"],"consequence":"..."}'
python3 "$SKILL_DIR/scripts/factory-state.py" set-state "<task-id>" awaiting-captain
```

`decisions.md` is a plain file the tool only reads; nothing writes it for you.
When the captain answers, append the decision to `~/.bb/state/factory/decisions.md`
yourself and record a `task.decision` event. Treat `decisions.md` as durable
truth **only because the supervisor flushes it** — an answer that lives solely in
conversation memory is lost on rotation.

Two additional queues are reported from the same batched message, never as
separate interruptions:

- **Candidates I rejected and why** — title, source link, and exactly one pinned
  reason from [references/triage.md](references/triage.md). These are the
  read-only counterpart to the mutation intake is not allowed to perform.
- **Dispatch held** — tasks the output gate blocked, with the reason. Two
  distinct reasons, and they need different answers:
  - `review-queue-full` — the factory is producing PRs faster than they can be
    reviewed. The depth or the cap is wrong, not the gate. Lower concurrency;
    do not raise the cap to clear a queue.
  - `queue-depth-unknown` — `gh` failed, so the gate never ran. This is an auth,
    network, or rate-limit problem wearing a capacity costume. Fix the
    credential or connectivity issue; do not treat it as a full queue.

## Reviewer assignment

The supervisor does **not** assign PR reviewers, and does not choose one by
hand. It does not invent a reviewer, and does not guess one from a similar name.

Instead, **the repository decides.** The lane comes from the changed paths and
`docs/review-lanes.md`; the humans come from `CODEOWNERS`. The supervisor only
reads the answer. See [references/output.md](references/output.md) for the lane
table and the rule that Lane A starts empty.

Factory children therefore receive this instruction in their prompt:

> Read `docs/review-lanes.md` if it exists, determine the lane from the changed
> paths, and request that lane's required reviewers. If the file is absent, open
> the PR without a reviewer and say so. Do not ask who should review the PR.

This keeps the factory's delivery path free of any human round-trip. A task
completes when its PR is open, and the captain's review is the gate that follows.

A repository with no `docs/review-lanes.md` is a repo this factory has not been
wired into yet. Opening without a reviewer is the safe default; record that the
lane file is missing so it gets added rather than silently skipped every time.

If the repository's own guidance (`CONTRIBUTING.md`, `CODEOWNERS`, a local agent
file) or a platform default already requires or supplies a reviewer, let that
apply — the point is that the supervisor does not choose one.

**Commit-hook failure (step 9).** A child must not wait for a human. It reports
the blocker back to the supervisor — `bb thread output` on completion, or a
`bb thread tell` question — and the supervisor records it and batches it to the
captain in the ESCALATE step. Children never block on a human directly.

**Merge-queue failure.** A child that hits a failing merge queue or a red batch
reports and stops. It must not re-queue: at agent frequency, repeated retries
burn full CI runs and cascade failures onto everything behind it. See
[references/output.md](references/output.md).

## Context discipline

The user's context is finite and the supervisor runs for a long time. Protect it
deliberately:

- **Child threads are the memory.** All detail — diffs, test output, review
  findings — lives in children and in the ledger. Do not read child logs into
  your own context unless you need a specific fact from one.
- **The ledger is the truth.** `ledger.jsonl` plus `decisions.md` are enough to
  rebuild the entire fleet picture. Your conversation history is disposable.
- **You keep only a map.** Maintain a one-line-per-task table: task ID → child
  thread ID → state → one-line outcome. Nothing else belongs in your context.
- **Rotate at ~60% context.** Before you approach the limit, flush every
  answer you are holding to `decisions.md`, then spawn a fresh supervisor that
  loads this skill, reads the ledger, `decisions.md`, and the live child IDs, and
  continues. Retire the old one. Continuity comes from disk, never from a longer
  conversation, and any decision not written to disk is lost in the rotation.
  The fresh supervisor must filter its first `bb thread list` with
  `--parent-thread "$BB_THREAD_ID"` after it inherits the fleet.

## Escalation etiquette

The captain wants outcomes, consequences, and decisions — not narration.

Present each escalation as:

- **Outcome** — what happened, in one line.
- **Consequence** — what it blocks or costs if left alone.
- **Decision** — the specific question, with the options you see.

Present rejected intake candidates as a separate short list — "candidates I
rejected and why" — with the failed scope rule named. These are not
interruptions; they are the read-only counterpart to the mutation intake is not
allowed to perform.

Keep a queue of PRs awaiting captain review. Present them batched, in one
message, as a short list of title + PR link + one-line summary. Never open a
separate interruption per PR. Keep the PR queue separate from the escalation
queue (see SUPERVISE). Update both from the ledger, not from memory, so a
restart loses nothing.

## Authority

**The captain is the merge authority. Always.** The supervisor never merges,
and no auto-merge tier exists. The reviewer's `APPROVED` and the publisher's PR
are inputs to the captain's decision, not a substitute for it. When the captain
answers an escalation, record it in `decisions.md` so the same question is never
asked twice.