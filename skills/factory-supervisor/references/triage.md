# Triage

How the supervisor judges a candidate before admitting it, and what it does when
the answer is no.

Read this at the INTAKE step, together with [intake.md](intake.md).

## The read-only guarantee

**Intake never writes to the source.** Not a label, not a comment, not a
transition, not a thumbs-up. This holds for GitHub and Wrike alike, and it holds
whether the judgment feels obvious or not.

Two reasons, and they are separate:

1. **A heuristic must not produce an outward-facing side effect.** Triage is a
   classifier reading a ticket body. If it is wrong — and it will be wrong
   sometimes — the cost of that mistake must land in the supervisor's own ledger,
   not in a stranger's inbox.
2. **The supervisor is not yet trusted with it.** Write-back is a capability
   that has to be earned by demonstrated accuracy over time. Until the captain
   says otherwise, the answer is no.

So the supervisor classifies, records what it found, and reports upward. The
captain — or a separate task-breakdown workflow — acts on the source if action
is warranted. Saying "this issue is missing acceptance criteria" is triage.
Applying `needs-info` to it is not.

This is not a temporary awkwardness to be engineered away. It is the contract.

## Label taxonomy

The labels below are a **read contract**: the vocabulary the supervisor
classifies against and reports in. They are not applied by this skill.

Keep exactly one category and one state label per item. Applying a state label
clears `needs-triage`.

| Canonical role | Label | Meaning |
|---|---|---|
| needs-triage | `needs-triage` | Present but not evaluated yet |
| needs-info | `needs-info` | Waiting on the reporter — including missing acceptance criteria |
| too-large | `size:3` or larger (or an explicit `factory-too-large`) | Out of factory scope; needs decomposition first |
| needs-human | `needs-human` | Requires a design decision or a secret the supervisor cannot supply |
| ready-for-agent | `agent-ready` | The dispatch gate. Unchanged. |
| wontfix | `wontfix` | Terminal; never admitted |

`agent-ready` is the only label that admits work. The rest explain a rejection.

**This taxonomy only becomes a live label protocol if the captain authorises
write-back.** Until then it is documentation plus classification logic, and the
label column is what a human would need to apply by hand to make the same
judgment.

## Rejection reasons

Every rejection records **exactly one** reason from this list. No freeform
strings: a fixed vocabulary is countable, greppable, and cannot be
re-litigated with slightly different wording every wake.

| Reason | Meaning | Who resolves it |
|---|---|---|
| `needs-info` | Body lacks explicit acceptance criteria, a reproduction, or the detail required to verify | The reporter, then the captain re-labels `agent-ready` |
| `too-large` | Too big for one child to implement and verify; likely `size:3`+ | The breakdown workflow |
| `needs-breakdown` | Admissible in principle, but must be split into bounded pieces first | The breakdown workflow |
| `needs-human` | A design decision, credential, or external access the supervisor cannot supply | The captain |
| `duplicate-suspected` | Similarity match against existing open work | The captain confirms or dismisses |
| `not-verifiable` | No observable end state — the work cannot be proven done | The captain, or the reporter |

Record it in the ledger and surface it batched in ESCALATE:

```bash
python3 "$SKILL_DIR/scripts/factory-state.py" append task.escalated \
  "<factory>/gh-<number>" \
  --data '{"question":"Candidate rejected at intake","reason":"needs-info"}'
```

Never set `awaiting-captain` without either a `task.outcome` carrying a `prUrl`
or a `task.escalated`. See the SUPERVISE step of `SKILL.md`.

## The breakdown seam

`too-large` and `needs-breakdown` are the handoff to the captain's separate
task-breakdown workflow. The division of labour is deliberate:

- **This skill** decides that a candidate *needs* decomposition, names why, and
  stops. It does not decompose anything.
- **The breakdown workflow** (owned separately, not part of this skill) turns one
  large candidate into several bounded, verifiable ones, each of which can come
  back through intake carrying `agent-ready`.

The supervisor must not attempt the breakdown itself, even when the split looks
obvious, and must not run it from the intake path. That keeps the factory's only
job — dispatch — free of planning machinery.

Document the workflow's location in `decisions.md` once it exists so the next
supervisor points candidates at the right place instead of re-deciding.

## Dedup

Never dispatch the same work twice. Three checks, all read-only, in this order:

1. **Ledger.** `factory-state.py list` shows every known task and its state. A
   task in `admitted`, `dispatched`, `working`, `reviewing`, `publishing`, or
   `awaiting-captain` is already in flight — skip it.
2. **Open PRs and branches.** `gh pr list --state open` for the repo. A matching
   PR means the work already exists; skip it, and record the PR against the
   ledger entry if it is missing.
3. **Recently closed.** A task in `published`, `abandoned`, or `failed` was
   already attempted. Re-admitting needs new evidence that the situation
   changed; note that evidence in the admission event.

Match the source reference (issue number, Wrike ID) first. Title similarity is a
**flag only**: it may set `duplicate-suspected` for a human, never auto-skip.
Similarity across a diverse backlog produces false positives, and a silently
skipped real task is worse than a duplicate the captain dismisses in five
seconds.

There is no dedup ledger file. The main ledger, plus open PRs, is enough, and a
second store would be one more thing to drift out of sync.

## What the supervisor must not do

- Apply, remove, or propose labels on the source.
- Comment on, close, or reopen a source item.
- Auto-close a suspected duplicate. Ever.
- Split a large task itself.
- Widen the query beyond `agent-ready` to "help" the queue.
- Silently skip a candidate. A rejection that is not recorded is invisible work
  the captain cannot act on, and is the one failure mode worse than a false
  rejection.