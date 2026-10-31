#!/usr/bin/env python3
"""Build one snapshot CSV for the HF dataset danielrosehill/OR-Batch-Inference-Models.

Joins three inputs for the same snapshot date:
  1. reference/batch-models/<date>_batch-models.csv  (API-retrieved prices and providers)
  2. reference/batch-models/<date>_price-tiers.csv   (scripts/price_tiers.py output)
  3. reference/batch-models/<date>_api-records.json  (full /api/v1/models records for :batch ids)
and adds the endpoint-stability label. Column order and meaning are fixed by
hf/dataset/data_dictionary.json; the script fails if the two disagree.

Stability rule (enriched, written 2026-10-31):
  stable_endpoint = False when the id is a dynamic alias: starts with "~" or contains "latest"
                    (OpenRouter describes these as "always redirects to the latest model").
  stable_endpoint = False when canonical_slug carries no date stamp and the model is not open
                    weights (no hugging_face_id): the upstream name is a provider alias that can be
                    repointed to a new snapshot (e.g. OpenAI's gpt-4o).
  stable_endpoint = True otherwise: dated canonical_slug, or open weights with a fixed HF repo.

Cache pricing (enriched, written 2026-10-31):
  offers_cache_pricing = True when the record has pricing.input_cache_read.
  cache_pricing        = compact JSON of the API cache prices in US$/M, base tier plus any
                         long-context override that carries cache prices; "" when none.
                         write_usd_per_m is null when no input_cache_write is published.

Usage: python3 -I build_hf_dataset.py <date> <repo-root>
Writes <repo-root>/hf/dataset/data/batch_models_<date>.csv. Written by Claude Opus 5.5, 2026-10-31.
"""
import csv
import json
import re
import sys
from pathlib import Path

DATE_IN_SLUG = re.compile(r"-(\d{8}|\d{4}-\d{2}-\d{2})$")
TIER_RANK = {"Cheap": 1, "Mid": 2, "Expensive": 3}


def stability(base_id, rec):
    slug = rec.get("canonical_slug") or ""
    if base_id.startswith("~") or "latest" in base_id:
        return False, "dynamic alias id (~ prefix or 'latest')"
    if DATE_IN_SLUG.search(slug):
        return True, "dated canonical_slug"
    if rec.get("hugging_face_id"):
        return True, "open weights, fixed Hugging Face repo"
    return False, "undated canonical_slug, closed weights: provider alias that can be repointed"


def per_m(v):
    return None if v in (None, "") else round(float(v) * 1e6, 6)


def cache(rec):
    p = rec.get("pricing") or {}
    if not p.get("input_cache_read"):
        return False, ""
    obj = {"read_usd_per_m": per_m(p["input_cache_read"]), "write_usd_per_m": per_m(p.get("input_cache_write"))}
    for o in p.get("overrides") or []:
        if o.get("input_cache_read"):
            obj["long_context"] = {"min_prompt_tokens": o.get("min_prompt_tokens"),
                                   "read_usd_per_m": per_m(o["input_cache_read"]),
                                   "write_usd_per_m": per_m(o.get("input_cache_write"))}
    return True, json.dumps(obj, separators=(",", ":"))


def main(date, root):
    root = Path(root)
    ref = root / "reference" / "batch-models"
    dictionary = json.load(open(root / "hf" / "dataset" / "data_dictionary.json"))
    columns = [c["name"] for c in dictionary["columns"]]

    snap = list(csv.DictReader(open(ref / f"{date}_batch-models.csv", newline="")))
    tiers = {r["model"]: r for r in csv.DictReader(open(ref / f"{date}_price-tiers.csv", newline=""))}
    recs = {r["id"].removesuffix(":batch"): r for r in json.load(open(ref / f"{date}_api-records.json"))["batch_models"]}

    rows = []
    for r in snap:
        t, rec = tiers[r["model"]], recs[r["model"]]
        stable, basis = stability(r["model"], rec)
        has_cache, cache_json = cache(rec)
        rows.append({
            "snapshot_date": date, **r,
            "canonical_slug": rec.get("canonical_slug") or "",
            "hugging_face_id": rec.get("hugging_face_id") or "",
            "expiration_date": rec.get("expiration_date") or "",
            "tier": t["tier"], "tier_rank": TIER_RANK[t["tier"]], "sub_band": t["sub_band"],
            "input_band": t["input_band"], "input_mismatch": t["input_mismatch"],
            "out_in_ratio": t["out_in_ratio"], "reference_job_usd": t["job_usd"],
            "stable_endpoint": stable, "stability_basis": basis,
            "offers_cache_pricing": has_cache, "cache_pricing": cache_json,
        })
    if list(rows[0]) != columns:
        sys.exit(f"columns differ from data_dictionary.json:\n built {list(rows[0])}\n dict  {columns}")
    rows.sort(key=lambda x: (float(x["batch_output_usd_per_m"]), float(x["batch_input_usd_per_m"]), x["model"]))

    out = root / "hf" / "dataset" / "data" / f"batch_models_{date}.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        w.writerows(rows)
    print(out, len(rows), "rows")
    for x in rows:
        if not x["stable_endpoint"]:
            print("  unstable:", x["model"], "|", x["canonical_slug"], "|", x["stability_basis"])


if __name__ == "__main__":
    main(*sys.argv[1:3])
