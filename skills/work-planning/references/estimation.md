# Estimation

How to produce an estimate someone can trust and act on. Read when the numbers
matter — commitment, budget, date, or prioritization.

## An estimate is a distribution

Never emit a bare number for work with real uncertainty. Emit a range and a
confidence level: "5 days, 80% confident it lands in 3–9". That is defensible;
"5 days" is a commitment that will be treated as a promise.

## Cone of uncertainty

Estimation error is largest at the start and shrinks as the project proceeds.
Roughly, before the problem is understood at all, estimates can be off by a
multiplicative factor; once requirements are settled and the design is known,
they narrow to a small band. Two consequences:

- **Wide early ranges are correct, not sloppy.** An early "20–80 days" is more
  honest than an early "40 days".
- **Do not commit to a date before the cone narrows.** Use spikes to retire the
  biggest unknowns first, then re-estimate. Say in the plan which spikes will
  narrow which numbers.

## Picking an anchor

Ordered most to least reliable:

1. **Historical data** — what comparable work actually took, measured. Prefer
   this. Sources: git log timestamps for similar features, ticket cycle time,
   the user's own recollection of a similar effort.
2. **Reference story** — "this is about the size of <already-shipped chunk>,
   which took N days." Adequate, and fast for a team that shares context.
3. **Absolute judgment** — "feels like a week." Weakest. Acceptable only when
   (1) and (2) are unavailable, and must widen the range.

State the anchor in the plan. When only (3) is available, label the whole plan
low-confidence. Anchoring on another person's optimistic guess, or on the
number a stakeholder wanted to hear, is not an anchor.

Anchoring bias is real: the first number spoken pulls the rest. Estimate
chunks independently before summing, and do not let a known target date
("we need this in three weeks") leak into the per-chunk numbers.

## Three-point estimates

For anything that feeds a commitment, give optimistic / most likely /
pessimistic per chunk.

- **Optimistic (O)** — everything goes right; no surprises. Not a target.
- **Most likely (M)** — the realistic single value.
- **Pessimistic (P)** — the plausible bad case, not the catastrophe. Should
  happen roughly 1 time in 20, not 1 in 1000. If P is 5× M, the chunk is
  probably still unestimated — spike it.

PERT expected value: `E = (O + 4M + P) / 6`. Standard deviation:
`sd = (P − O) / 6`. Variances add across the critical path:
`sd_total = sqrt(sum(sd_i²))`.

`scripts/estimate.py` does this and reports 50/80/95% confidence totals.

Why not just sum M? Summing most-likely values systematically understates
totals — it assumes every chunk hits its best realistic case at once. The
PERT weighting and variance adding give a distribution instead of a fantasy.

## Buffer

Do not pad every chunk. Padding hides where the risk is and gets stripped when
the total looks too big.

Put buffer where the risk is, named:

- **Spike budget** — explicit timeboxed investigation for unknowns.
- **Integration buffer** — chunks never compose as cleanly as they look.
- **External dependency buffer** — third-party APIs, reviews, approvals.

PERT's pessimistic term already carries statistical weight; do not stack a
percentage buffer on top of it and call the result an estimate. If you add a
contingency, state it as a separate line so it can be argued with.

## Capacity and dates

An effort estimate is not a date. To get a date you need capacity:

```
duration ≈ expected_effort / (people × effective_days_per_week)
```

Then apply availability reality: meetings, support, review time, and hand-offs
typically leave well under 5 effective days per week per person. State the
assumed capacity in the plan — a total with no capacity assumption is a wish.

Converting to a date is a forecast, not a commitment. Phrase it as: "80%
chance of completion by <date>, assuming <capacity>".

## Lightweight alternatives

When the work is repetitive and comparable (a stream of similar tickets),
estimating each chunk is wasted effort. Instead forecast from **throughput**:
measure how many comparable items complete per week and divide the backlog by
that rate. This reference-class approach is often more accurate than per-item
estimates because it uses what actually happened rather than what people
believe will happen.

Choose per: unknown, novel, or one-off work → three-point estimate. Repetitive
comparable work → throughput forecast.

## Reporting

Always state, alongside any number:

- the unit (days of effort, not calendar days, unless stated)
- the confidence level
- the capacity assumption
- whether it is the critical path or the sum of all chunks
- the biggest single contributor to uncertainty

Never present the optimistic case as the plan.
