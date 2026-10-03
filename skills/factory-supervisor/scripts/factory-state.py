#!/usr/bin/env python3
"""factory-state.py - typed accessors over the factory ledger.

The ledger is append-only JSONL at $FACTORY_STATE_DIR/ledger.jsonl.
This module never rewrites history; it only appends events and derives
current state. Derived state is disposable and rebuildable.

Usage:
  factory-state.py init
  factory-state.py append <type> <task-id> [--data '<json object>']
  factory-state.py set-state <task-id> <state> [--note '<text>']
  factory-state.py get <task-id>
  factory-state.py list [--factory <name>] [--state <state>]
  factory-state.py reconcile
  factory-state.py decisions

State location is the same on every machine: ~/.bb/state/factory/. Contents are
machine-specific, because each machine runs its own factories. Override with
FACTORY_STATE_DIR only for testing.

Exit codes: 0 ok, 1 usage error, 2 not found.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path(os.environ.get("FACTORY_STATE_DIR", Path.home() / ".bb/state/factory"))
LEDGER = STATE_DIR / "ledger.jsonl"
TASKS_DIR = STATE_DIR / "tasks"
DECISIONS = STATE_DIR / "decisions.md"

# The state machine. A task moves through these; anything else is rejected so a
# typo cannot create a phantom state the supervisor will not recognise.
STATES = (
    "admitted",
    "dispatched",
    "working",
    "reviewing",
    "publishing",
    "awaiting-captain",
    "published",
    "abandoned",
    "failed",
)

EVENT_TYPES = (
    "task.admitted",
    "task.dispatched",
    "task.state",
    "task.escalated",
    "task.decision",
    "task.outcome",
)


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def factory_of(task_id: str) -> str:
    """Task IDs are <factory>/<source>-<ref>; the part before the slash."""
    return task_id.split("/", 1)[0] if "/" in task_id else "default"


def die(msg: str, code: int = 1) -> None:
    print(f"factory-state: {msg}", file=sys.stderr)
    sys.exit(code)


def cache_path(task_id: str) -> Path:
    return TASKS_DIR / (task_id.replace("/", "_") + ".json")


def read_ledger() -> list[dict]:
    """Read every event. Skips unparseable lines but reports them, because a
    silently short ledger is worse than a noisy one."""
    if not LEDGER.exists():
        return []
    events, bad = [], 0
    with LEDGER.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                bad += 1
    if bad:
        print(f"factory-state: warning: skipped {bad} malformed ledger line(s)",
              file=sys.stderr)
    return events


def fold(events: list[dict], task_id: str) -> dict | None:
    """Fold one task's events into current state. Last write wins per field."""
    mine = [e for e in events if e.get("taskId") == task_id]
    if not mine:
        return None

    def last_field(key: str):
        vals = [e[key] for e in mine if e.get(key) is not None]
        return vals[-1] if vals else None

    def last_of_type(t: str):
        vals = [e for e in mine if e.get("type") == t]
        return vals[-1] if vals else None

    state_events = [e for e in mine if e.get("type") == "task.state"]
    outcome = last_of_type("task.outcome")

    return {
        "taskId": task_id,
        "factory": mine[-1].get("factory", factory_of(task_id)),
        "state": state_events[-1]["state"] if state_events else "admitted",
        "title": last_field("title"),
        "source": last_field("source"),
        "childThreadId": last_field("childThreadId"),
        "prUrl": last_field("prUrl"),
        "note": last_field("note"),
        "escalation": last_of_type("task.escalated"),
        "outcome": outcome,
        "events": len(mine),
        "updatedAt": mine[-1]["ts"],
        "lastEvent": mine[-1]["type"],
    }


def all_tasks(events: list[dict]) -> list[dict]:
    ids = []
    for e in events:
        tid = e.get("taskId")
        if tid and tid not in ids:
            ids.append(tid)
    out = [fold(events, tid) for tid in ids]
    return [t for t in out if t]


def write_cache(task: dict) -> None:
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    cache_path(task["taskId"]).write_text(json.dumps(task, indent=2) + "\n")


def emit(obj) -> None:
    print(json.dumps(obj, indent=2))


def parse_flags(argv: list[str], allowed: tuple[str, ...]) -> dict:
    flags, i = {}, 0
    while i < len(argv):
        tok = argv[i]
        if not tok.startswith("--"):
            die(f"unexpected argument {tok!r}")
        name = tok[2:]
        if name not in allowed:
            die(f"unknown option --{name}")
        if i + 1 >= len(argv):
            die(f"option --{name} needs a value")
        flags[name] = argv[i + 1]
        i += 2
    return flags


def append_event(event_type: str, task_id: str, data: dict) -> dict:
    if event_type not in EVENT_TYPES:
        die(f"unknown event type {event_type!r}; expected one of {', '.join(EVENT_TYPES)}")

    event = {"ts": utcnow(), "type": event_type,
             "taskId": task_id, "factory": factory_of(task_id)}
    event.update(data)

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as fh:
        fh.write(json.dumps(event, separators=(",", ":")) + "\n")

    # Refresh the derived cache. Cheap, and keeps the cache always warm.
    write_cache(fold(read_ledger(), task_id) or event)
    return event


def cmd_append(argv: list[str]) -> None:
    if len(argv) < 2:
        die("append needs <type> <task-id>")
    event_type, task_id = argv[0], argv[1]
    flags = parse_flags(argv[2:], ("data",))
    data = {}
    if "data" in flags:
        try:
            data = json.loads(flags["data"])
        except json.JSONDecodeError as exc:
            die(f"--data is not valid JSON: {exc}")
        if not isinstance(data, dict):
            die("--data must be a JSON object")
    emit(append_event(event_type, task_id, data))


def cmd_set_state(argv: list[str]) -> None:
    if len(argv) < 2:
        die("set-state needs <task-id> <state>")
    task_id, state = argv[0], argv[1]
    if state not in STATES:
        die(f"unknown state {state!r}; expected one of {', '.join(STATES)}")
    flags = parse_flags(argv[2:], ("note",))
    data = {"state": state}
    if "note" in flags:
        data["note"] = flags["note"]
    append_event("task.state", task_id, data)
    emit(fold(read_ledger(), task_id))


def cmd_get(argv: list[str]) -> None:
    if not argv:
        die("get needs <task-id>")
    task = fold(read_ledger(), argv[0])
    if not task:
        die(f"no events for task {argv[0]}", 2)
    write_cache(task)
    emit(task)


def cmd_list(argv: list[str]) -> None:
    flags = parse_flags(argv, ("factory", "state"))
    tasks = all_tasks(read_ledger())
    if "factory" in flags:
        tasks = [t for t in tasks if t["factory"] == flags["factory"]]
    if "state" in flags:
        tasks = [t for t in tasks if t["state"] == flags["state"]]
    tasks.sort(key=lambda t: t["updatedAt"])
    emit(tasks)


def cmd_reconcile(argv: list[str]) -> None:
    parse_flags(argv, ())
    tasks = all_tasks(read_ledger())
    for task in tasks:
        write_cache(task)
    print(f"factory-state: reconciled {len(tasks)} task(s)")


def cmd_init(argv: list[str]) -> None:
    """Bootstrap the state directory on a new machine.

    Idempotent: creates only what is missing, and never touches an existing
    ledger. Safe to run on a machine that already has a factory.
    """
    parse_flags(argv, ())
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    created = []
    if not DECISIONS.exists():
        DECISIONS.write_text(
            "# Factory decisions\n\n"
            "Standing answers to questions the supervisor would otherwise re-ask.\n"
            "Read at every wake. Written by the supervisor when the captain\n"
            "answers an escalation, and editable by hand.\n\n"
            "Format: one entry per decision, as a heading and a short answer.\n"
            "Example:\n\n"
            "## Branch base for <repo>\n\n"
            "Use origin/develop, not main.\n"
        )
        created.append(str(DECISIONS))
    print(f"factory-state: state dir {STATE_DIR}")
    print(f"factory-state: ledger {'exists' if LEDGER.exists() else 'not yet created (first append will make it)'}")
    for path in created:
        print(f"factory-state: created {path}")
    if not created:
        print("factory-state: nothing to create; already initialised")


def cmd_decisions(argv: list[str]) -> None:
    parse_flags(argv, ())
    if DECISIONS.exists():
        sys.stdout.write(DECISIONS.read_text())
    else:
        print("factory-state: no decisions recorded yet", file=sys.stderr)


def main() -> None:
    argv = sys.argv[1:]
    if not argv:
        die(__doc__ or "usage", 1)
    cmd, rest = argv[0], argv[1:]
    handlers = {
        "init": cmd_init,
        "append": cmd_append,
        "set-state": cmd_set_state,
        "get": cmd_get,
        "list": cmd_list,
        "reconcile": cmd_reconcile,
        "decisions": cmd_decisions,
    }
    if cmd not in handlers:
        die(f"unknown command {cmd!r}; expected one of {', '.join(handlers)}")
    handlers[cmd](rest)


if __name__ == "__main__":
    main()
