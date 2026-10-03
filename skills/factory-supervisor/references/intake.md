# Intake

How the supervisor finds work, decides what it may take, and avoids doing the
same task twice. Read this at the INTAKE step of every wake.

## Sources

An intake source is anything the supervisor can query read-only and turn into a
task ID of the form `<factory>/<source>-<ref>`.

### GitHub

```bash
gh repo view --json nameWithOwner -q .nameWithOwner   # confirm the repo
gh issue list \
  --repo <owner>/<repo> \
  --label agent-ready \
  --state open \
  --json number,title,body,labels,assignees,url \
  --limit 50
```

Follow the existing `github-issues` skill for auth and repo resolution; it is
the source of truth for `gh` usage. The `agent-ready` label is the contract: a
human applied it, so the issue is in scope for autonomous work. Do not widen
the query to unlabeled issues on your own.

Task ID: `<factory>/gh-<number>` — for example `home/gh-412`.

### Wrike

Load the existing `wrike` (wrike-ai-safe) skill and use its read-only discovery
to list candidate items. Do not create, update, comment on, or approve anything
during intake — those are write actions and they belong to the publisher, behind
its confirmation gate.

Task ID: `<factory>/wrike-<id>` — for example `work/wrike-88231`.

### Other sources

Any source works if it can be queried read-only and yields a stable reference.
Keep the ID convention `<factory>/<source>-<ref>`. Add the source to this file
when you add it to a factory, so the next supervisor does not have to rediscover
the query.

## Scope filter

Admit a task only when it is **small and well-specified**. This is not
conservatism for its own sake — it is measured. Small, well-specified changes
succeed far more often than architecture work, because the child can satisfy
concrete acceptance criteria and verify its own result. Open-ended or
architectural tasks produce work that cannot be verified, and unverifiable work
is where autonomous pipelines fail.

Admit the task when all of these hold:

- **Bounded** — the change touches a known area and the issue names it.
- **Verifiable** — there is an observable result: a test, a behavior, a fixed
  error. "Refactor the auth layer" fails this; "return 401 instead of 500 when
  the token is expired" passes.
- **Specified** — the issue states explicit acceptance criteria. Do not infer
  them. Absent or vague criteria means escalate or file back, never admit.
- **Sized `size:1` or `size:2`** — the issue carries a size label and it is
  small. Anything `size:3` or larger is out of scope for the factory and is
  filed back with a note. No label means not admitted.
- **Independent** — it does not require a design decision the supervisor cannot
  make. If it does, that is an escalation, not an admission.

Reject or defer when any of these fail:

- architecture or system design;
- cross-cutting refactors with no observable end state;
- tasks that require new secrets, credentials, or infrastructure the supervisor
  cannot provision;
- tasks whose acceptance criteria are genuinely ambiguous.

This filter is intentionally strict. A small queue of tasks that ship beats a
large queue of tasks that stall.

## Dedup rules

Never dispatch the same work twice. Before admitting, check all three:

1. **Open tasks in the ledger.** `factory-state.py list` gives every known task
   and its state. A task in `admitted`, `dispatched`, `working`, `reviewing`,
   `publishing`, or `awaiting-captain` is already in flight — skip it.
2. **Open PRs and branches.** Search the repo for an open PR or branch that
   already addresses the issue (`gh pr list --repo <owner>/<repo> --state open
   --json number,title,headRefName,url`). A matching PR means the work exists;
   skip it, and link the PR to the ledger entry if one is missing.
3. **Recently closed tasks.** A task in `published` or `abandoned` was already
   attempted. Re-admitting requires new evidence that the situation changed —
   note that evidence in the admission event.

Match on the source reference (issue number, Wrike ID) first. Fall back to title
similarity only to flag a possible duplicate for a human, never to auto-skip.

## Filing work that is not ready

Intake is **read-only**. The supervisor never edits, labels, comments on, or
otherwise mutates the source during INTAKE. A mislabel on a human's real issue
would be an outward-facing side effect produced by a heuristic judgment, so it is
not allowed from the intake path. This keeps GitHub and Wrike symmetric: neither
is written to before the captain confirms.

Never silently skip a candidate. Instead, satisfy the guarantee without
mutating the source: record the rejection in the ledger with its reason, and the
ESCALATE step surfaces it batched.

```bash
python3 "$SKILL_DIR/scripts/factory-state.py" append task.escalated \
  "<factory>/gh-<number>" \
  --data '{"question":"Candidate rejected at intake","reason":"<which scope rule failed>"}'
```

The supervisor presents these in the ESCALATE message as a short list:
"candidates I rejected and why" — title, source link, and the failed rule. The
captain then decides whether to relabel it `agent-ready`, split it, or leave it.

Do **not** run `gh issue edit` or `gh issue comment` from intake. If the captain
explicitly authorizes relabeling later, it is a separate confirmed action that
mirrors the Wrike rule: present the proposed change, wait for confirmation, then
write. Until that authorization exists, the ledger record is the response.

Record durable policy judgments in `decisions.md` ("this class of work is out of
scope for this factory") so the same candidate is not re-evaluated every wake.