#!/usr/bin/env python3
"""Sort a batch-models CSV snapshot into price tiers (US$ per million tokens, batch prices).

Rubric (written 2026-10-31 against the 2026-10-31 snapshot, 71 :batch ids):
  Output tier, the primary axis (batch output $/M):
    1 Cheap      < 3      1a <= 1.00, 1b 1.00-3.00
    2 Mid        3 - 20   2a 3.00-8.00, 2b 8.00-20
    3 Expensive  >= 20    3a 20-50, 3b >= 50 ("-pro" reasoning models)
  Input band, secondary (batch input $/M): cheap < 0.60, mid 0.60-3.00, expensive >= 3.00.
  A model whose input band differs from its output tier is flagged: it moves tier for
  input-heavy jobs.
  Job cost: the notebook's reference job, 4.5M input + 0.5M output tokens (9:1).

Boundaries sit in the widest gaps of the price ladder (2.50 -> 3.75, 7.50 -> 10, 15 -> 25,
37.5 -> 60), so small price changes should not move models across them.

Usage: python3 -I price_tiers.py <snapshot.csv> <out-prefix>
Writes <out-prefix>.csv and <out-prefix>.md. Written by Claude Opus 5.5, 2026-10-31.
"""
import csv
import sys

TIERS = [  # (sub-band, upper bound exclusive on output $/M, tier name)
    ("1a", 1.0001, "Cheap"), ("1b", 3, "Cheap"),
    ("2a", 8, "Mid"), ("2b", 20, "Mid"),
    ("3a", 50, "Expensive"), ("3b", float("inf"), "Expensive"),
]
INPUT_BANDS = [(0.6, "Cheap"), (3, "Mid"), (float("inf"), "Expensive")]
JOB_IN, JOB_OUT = 4.5, 0.5  # million tokens


def main(src, prefix):
    rows = []
    for r in csv.DictReader(open(src, newline="")):
        i, o = float(r["batch_input_usd_per_m"]), float(r["batch_output_usd_per_m"])
        sub, _, tier = next(t for t in TIERS if o < t[1])
        in_band = next(b for lim, b in INPUT_BANDS if i < lim)
        rows.append({
            "tier": tier, "sub_band": sub, "model": r["model"],
            "batch_input_usd_per_m": i, "batch_output_usd_per_m": o,
            "out_in_ratio": round(o / i, 1), "input_band": in_band,
            "input_mismatch": in_band != tier,
            "job_usd": round(i * JOB_IN + o * JOB_OUT, 2),
        })
    rows.sort(key=lambda x: (x["batch_output_usd_per_m"], x["batch_input_usd_per_m"], x["model"]))

    with open(prefix + ".csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    md = [f"| Band | Model | Batch in / out | Out÷in | Input band | Job |",
          "| --- | --- | --- | --- | --- | --- |"]
    for x in rows:
        flag = f"**{x['input_band']}**" if x["input_mismatch"] else x["input_band"]
        md.append(f"| {x['sub_band']} | `{x['model']}` | {x['batch_input_usd_per_m']:g} / "
                  f"{x['batch_output_usd_per_m']:g} | {x['out_in_ratio']:g} | {flag} | ${x['job_usd']:.2f} |")
    open(prefix + ".md", "w").write("\n".join(md) + "\n")

    for sub, _, tier in TIERS:
        g = [x for x in rows if x["sub_band"] == sub]
        if g:
            print(f"{sub} {tier:9} n={len(g):2}  out {g[0]['batch_output_usd_per_m']:g}-"
                  f"{g[-1]['batch_output_usd_per_m']:g}  job ${min(x['job_usd'] for x in g):.2f}-"
                  f"${max(x['job_usd'] for x in g):.2f}")
    print("input mismatches:", [x["model"] for x in rows if x["input_mismatch"]])


if __name__ == "__main__":
    main(*sys.argv[1:3])
