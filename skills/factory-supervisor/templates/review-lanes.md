# Review lanes

Copy this file to `docs/review-lanes.md` in the repository and commit it next to
`CODEOWNERS`. The paths decide which lane a pull request is in, so the lane
rules must live in the repo, not in an agent's prompt.

Fill in the paths for *this* repository. The table below is a starting point.

## Lanes

| Lane | What falls in it | Gate before merge | Who signs off |
|---|---|---|---|
| **A** Green pipeline | Dependency patch bumps, documentation, copy changes, generated clients, changes matching a pattern already approved many times | Types, tests, lint, and the PR size budget pass; the automated reviewer raises no blocking finding | The pipeline. The tech lead samples a few each week. |
| **B** Automated + sampled human | Ordinary feature and bug-fix work inside one module, with strong tests | The Lane A gates, plus a human reads the evidence bundle and reads code only when the evidence is thin | One reviewer, assigned by load |
| **C** Code owner | Public APIs, shared libraries, performance-sensitive paths, anything crossing module boundaries | Lanes A and B, plus a code owner's approval | The owning team, via `CODEOWNERS` |
| **D** Two humans, code read | Authentication and authorisation, payments, migrations, secrets, CI configuration, `.github/` | All of the above, plus **two** approvals | Two humans |

Replace the placeholders with real paths:

| Path | Lane |
|---|---|
| `docs/**` | A |
| `**/*.md` | A |
| `<generated-client-dir>/**` | A |
| `src/<module>/**` | B |
| `src/public-api/**` | C |
| `src/shared/**` | C |
| `src/auth/**` | D |
| `src/billing/**` | D |
| `db/migrations/**` | D |
| `.github/**` | D |

## Lane A starts empty

A class of change earns its way into Lane A only after a run of merges with no
reverts and no escaped defects. It falls back out to Lane B after a single
revert or escaped defect.

Start with Lane A unpopulated and let entries prove themselves. A lane that
begins populated is a permission granted in a busy week, not a judgment that was
earned.

## How a change is routed

A pull request is in the **highest** lane any of its changed paths maps to. Mixed
changes take the stricter lane, never the average.

## PR size budget

Target **<= 400 changed lines**, excluding lockfiles and snapshots.

A split only counts if each pull request passes the test suite on its own and
states a single concern. A stack whose members only make sense together is one
large pull request with extra overhead, and is rejected as such.

## Notes

- `CODEOWNERS` supplies the humans. The lane table decides which of them are
  required.
- Investigate any large PR slipping through a lane with no review — the
  unreviewed-merge metric exists to catch exactly that.
- Review lane membership as a table on a schedule, not only after an incident.