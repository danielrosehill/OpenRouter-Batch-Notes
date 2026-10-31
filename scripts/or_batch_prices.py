#!/usr/bin/env python3
"""List OpenRouter :batch models with batch vs sync prices (US$ per million tokens).

Uses the public https://openrouter.ai/api/v1/models endpoint; no API key needed.
Written by Claude Opus 5.5, 2026-10-31.

Usage: python3 or_batch_prices.py [--json]
"""
import json
import sys
import urllib.request

URL = "https://openrouter.ai/api/v1/models"


def per_m(p, key):
    try:
        return float(p.get(key) or 0) * 1e6
    except ValueError:
        return float("nan")


def main():
    with urllib.request.urlopen(URL, timeout=30) as r:
        models = {m["id"]: m for m in json.load(r)["data"]}
    rows = []
    for mid, m in models.items():
        if not mid.endswith(":batch"):
            continue
        base = mid[: -len(":batch")]
        sync = models.get(base, {}).get("pricing", {})
        rows.append({
            "id": mid,
            "batch_in": per_m(m["pricing"], "prompt"),
            "batch_out": per_m(m["pricing"], "completion"),
            "sync_in": per_m(sync, "prompt") if sync else None,
            "sync_out": per_m(sync, "completion") if sync else None,
        })
    rows.sort(key=lambda r: r["batch_in"] + r["batch_out"])
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=2))
        return
    print(f"{len(rows)} :batch ids of {len(models)} models\n")
    print(f"{'model':55} {'batch in/out':>17} {'sync in/out':>17}  note")
    for r in rows:
        s = (f"{r['sync_in']:.3f}/{r['sync_out']:.3f}" if r["sync_in"] is not None else "n/a")
        note = ""
        if r["sync_in"] is not None and (r["batch_in"] > r["sync_in"] or r["batch_out"] > r["sync_out"]):
            note = "batch dearer on in or out"
        print(f"{r['id']:55} {r['batch_in']:8.3f}/{r['batch_out']:<8.3f} {s:>17}  {note}")


if __name__ == "__main__":
    main()
