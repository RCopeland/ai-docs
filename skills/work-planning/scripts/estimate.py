#!/usr/bin/env python3
"""Estimate a plan of chunks with three-point (PERT) estimates.

Reads chunks as CSV from stdin (or a file) with columns:
    name,optimistic,likely,pessimistic
A header row is optional and recognised by the word "optimistic".
If the name is omitted (3 numeric columns), the chunk is unnamed but still
counted. Weights are ignored; pass a single total for the critical path only.

Outputs per-chunk expected duration and std dev, the summed expected total,
a confidence band, and the probability of finishing within --target.

Example:
    printf 'auth,1,2,4\\nsync,3,5,10\\n' | estimate.py --unit days
    estimate.py plan.csv --target 20 --unit days
"""
from __future__ import annotations

import argparse
import csv
import math
import sys

def parse_rows(stream, unit):
    reader = csv.reader(stream)
    rows = []
    for lineno, raw in enumerate(reader, start=1):
        cells = [c.strip() for c in raw]
        if not cells or all(not c for c in cells):
            continue
        if len(cells) == 3:
            cells = [f"chunk-{lineno}", *cells]
        if len(cells) < 4:
            raise SystemExit(
                f"line {lineno}: expected 4 columns (name,optimistic,likely,pessimistic), got {len(cells)}"
            )
        name = cells[0]
        if name.lower().startswith("name") or cells[1].lower().startswith("optimistic"):
            continue  # header
        try:
            o, m, p = (float(cells[1]), float(cells[2]), float(cells[3]))
        except ValueError:
            raise SystemExit(f"line {lineno}: non-numeric estimate in {cells[1:4]!r}")
        if not (o <= m <= p):
            raise SystemExit(
                f"line {lineno} ({name}): require optimistic <= likely <= pessimistic, got {o}, {m}, {p}. "
                "Fix the estimate rather than reordering it silently."
            )
        if o < 0:
            raise SystemExit(f"line {lineno} ({name}): negative estimate")
        rows.append((name, o, m, p))
    if not rows:
        raise SystemExit("no chunks provided")
    return rows

def norm_cdf(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

def main(argv=None):
    ap = argparse.ArgumentParser(description="Three-point (PERT) plan estimator")
    ap.add_argument("csvfile", nargs="?", help="CSV file; stdin if omitted")
    ap.add_argument("--unit", default="days", help="unit label for output (default: days)")
    ap.add_argument("--target", type=float, default=None, help="target total to compute confidence against")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = ap.parse_args(argv)

    if args.csvfile:
        with open(args.csvfile, newline="", encoding="utf-8") as fh:
            rows = parse_rows(fh, args.unit)
    else:
        rows = parse_rows(sys.stdin, args.unit)

    results = []
    expect_total = 0.0
    var_total = 0.0
    o_total = m_total = p_total = 0.0

    for name, o, m, p in rows:
        expect = (o + 4 * m + p) / 6.0
        sd = (p - o) / 6.0
        expect_total += expect
        var_total += sd * sd
        o_total += o
        m_total += m
        p_total += p
        results.append(
            dict(name=name, o=o, m=m, p=p, expected=expect, sd=sd,
             p10=expect - 1.2816 * sd, p90=expect + 1.2816 * sd)
        )

    sd_total = math.sqrt(var_total)
    p80 = expect_total + 0.8416 * sd_total
    p95 = expect_total + 1.6449 * sd_total
    p50 = expect_total

    target_prob = None
    if args.target is not None:
        if sd_total == 0:
            target_prob = 1.0 if args.target >= expect_total else 0.0
        else:
            target_prob = norm_cdf((args.target - expect_total) / sd_total)

    unit = args.unit
    if args.json:
        import json
        print(json.dumps({
            "unit": unit,
            "chunks": results,
            "totals": {
                "optimistic": o_total,
                "likely": m_total,
                "pessimistic": p_total,
                "expected": expect_total,
                "sd": sd_total,
                "p50": p50,
                "p80": p80,
                "p95": p95,
                "target": args.target,
                "target_probability": target_prob,
            },
        }, indent=2))
        return 0

    w = max(len(r["name"]) for r in results)
    w = max(w, 5)
    print(f"{'chunk'.ljust(w)}  {'O':>6} {'M':>6} {'P':>6} {'E[chunk]':>9} {'sd':>6}  ±1sd")
    print("-" * (w + 44))
    for r in results:
        spread = f"{r['expected'] - r['sd']:.1f}–{r['expected'] + r['sd']:.1f}"
        print(
            f"{r['name'].ljust(w)}  {r['o']:>6.1f} {r['m']:>6.1f} {r['p']:>6.1f} "
            f"{r['expected']:>9.2f} {r['sd']:>6.2f}  {spread}"
        )
    print("-" * (w + 44))
    print(f"sum of pessimistic  : {p_total:.1f} {unit}  (this is NOT a schedule — critical path only)")
    print(f"sum of most likely  : {m_total:.1f} {unit}")
    print()
    print(f"expected (PERT)     : {expect_total:.1f} {unit}  (sd {sd_total:.2f})")
    print(f"  50% confidence    : {p50:.1f} {unit}")
    print(f"  80% confidence    : {p80:.1f} {unit}")
    print(f"  95% confidence    : {p95:.1f} {unit}")
    if target_prob is not None:
        print(f"P(finish <= {args.target:g} {unit}) : {target_prob * 100:.0f}%")
    if len(results) > 1:
        print()
        print("Note: totals assume all chunks are on the critical path. Remove work that")
        print("genuinely runs in parallel before quoting a total.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
