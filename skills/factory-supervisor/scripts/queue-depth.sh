#!/usr/bin/env bash
# queue-depth.sh - review-queue depth gate for the factory supervisor.
#
# Answers one question: may the supervisor dispatch more work right now?
#
# The factory produces PRs. It does not produce reviewers. If it dispatches
# faster than the captain can review, the review queue grows without bound and
# the end state is unreviewed merges. This gate is the brake: one number,
# checked before every dispatch.
#
# The cap comes from Little's law:  WIP = throughput x target time in review.
# Read the measured review throughput, pick the time in review you want, and
# that product is the cap. Default 12; override with --cap or $REVIEW_WIP_CAP.
#
# The gate blocks DISPATCH, never PR creation. An agent that cannot open a PR
# leaves a branch nobody can see, which is the same inventory hidden somewhere
# worse. Blocking dispatch keeps the work in the source, where it is visible
# and where the captain can reprioritise it.
#
# Read-only. This script never writes to GitHub.
#
# Usage:
#   queue-depth.sh --repo <owner>/<repo> [--cap N]
#
# Exit codes:
#   0  dispatch allowed
#   1  queue full
#   2  usage error
#   3  could not determine queue depth (gh failed) - the gate did NOT run
#
# Code 3 is deliberately distinct. A failed gh call is not evidence that the
# queue is full, and treating it as such would stall the factory behind a
# misleading reason. Callers must treat 3 as "unknown", not as "full".

set -euo pipefail

REPO=""
CAP="${REVIEW_WIP_CAP:-12}"

usage() {
  cat >&2 <<'EOF'
usage: queue-depth.sh --repo <owner>/<repo> [--cap N]

Counts open, non-draft, not-yet-approved pull requests and decides whether the
factory may dispatch more work. Exits 0 when dispatch is allowed, 1 when the
review queue is full, 3 when the depth could not be determined at all.

Options:
  --repo <owner>/<repo>   Repository to inspect. Required.
  --cap N                 Review queue cap. Default $REVIEW_WIP_CAP or 12.
  -h, --help              Show this message.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --repo)
      [ $# -ge 2 ] || { echo "queue-depth: --repo needs a value" >&2; usage; exit 2; }
      REPO="$2"; shift 2 ;;
    --cap)
      [ $# -ge 2 ] || { echo "queue-depth: --cap needs a value" >&2; usage; exit 2; }
      CAP="$2"; shift 2 ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "queue-depth: unexpected argument $1" >&2; usage; exit 2 ;;
  esac
done

if [ -z "$REPO" ]; then
  echo "queue-depth: --repo is required" >&2
  usage
  exit 2
fi

if ! [[ "$CAP" =~ ^[0-9]+$ ]]; then
  echo "queue-depth: --cap must be a non-negative integer, got '$CAP'" >&2
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "queue-depth: gh CLI not found. See the github-issues skill." >&2
  exit 2
fi

# Count what the cap is actually about: PRs still waiting on a reader.
#   draft:false        - a draft is not yet asking for review
#   -review:approved   - an approved PR no longer needs a reviewer
open="$(gh pr list \
  --repo "$REPO" \
  --state open \
  --search "draft:false -review:approved" \
  --limit 200 \
  --json number \
  --jq 'length')" || {
  echo "queue-depth: could not read the review queue for $REPO (gh failed)." >&2
  echo "This is NOT a full queue. Report it and treat depth as unknown." >&2
  exit 3
}

# Guard against a non-numeric result so the comparison cannot misbehave.
if ! [[ "$open" =~ ^[0-9]+$ ]]; then
  echo "queue-depth: unexpected gh output for $REPO: '$open'" >&2
  exit 3
fi

if [ "$open" -ge "$CAP" ]; then
  echo "Review queue full: $open open PRs awaiting review (cap $CAP)." >&2
  echo "Review before dispatching more; the factory must not outrun its reviewer." >&2
  exit 1
fi

echo "Review queue $open/$CAP: dispatch allowed."