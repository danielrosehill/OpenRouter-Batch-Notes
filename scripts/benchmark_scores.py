#!/usr/bin/env python3
"""Benchmark-weighted quality and quality-per-cost for each batch workload.

Joins public benchmark scores onto the workload costs from entry 08 and reports, per workload,
a quality score, its cost, whether the model is on the cost/quality Pareto frontier, and the
cheapest model within 90% of the best quality. Method and weights:
reference/benchmarks/workload-benchmarks.json. Name mapping: reference/benchmarks/model-map.json.

Sources (download with --fetch <dir>, or pass a dir that already holds them):
  <dir>/text.parquet      LMArena text arena, HF lmarena-ai/leaderboard-dataset text/latest
  <dir>/document.parquet  LMArena document arena, same dataset, document/latest
  <dir>/vectara.md        github.com/vectara/hallucination-leaderboard README.md

Usage:
  uv run --with pandas --with pyarrow python -I scripts/benchmark_scores.py \
      [--fetch] <source-dir> <workload-costs.csv> <out-prefix>
Writes <out-prefix>_signals.csv (every matched score, all variants), <out-prefix>_value.csv
(one row per model x workload) and <out-prefix>_value.md. Written by Claude Opus 5.5, 2026-10-31.
"""
import json
import os
import re
import sys
import urllib.request

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "reference", "benchmarks")
URLS = {
    "text.parquet": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset/resolve/main/text/latest-00000-of-00001.parquet",
    "document.parquet": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset/resolve/main/document/latest-00000-of-00001.parquet",
    "vectara.md": "https://raw.githubusercontent.com/vectara/hallucination-leaderboard/main/README.md",
}
# Reasoning-effort rank parsed from a variant name. Untagged = 0 (not proof of no reasoning).
EFFORT = [("minimal", 1), ("instant", 1), ("low", 2), ("medium", 3), ("thinking", 4),
          ("xhigh", 5), ("high", 4), ("max", 6)]


def effort(name):
    n = name.lower()
    for tag, rank in EFFORT:
        if re.search(rf"(^|[\s(\-,]){tag}([\s),\-]|$)", n):
            return rank
    return 0


def load_vectara(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[2].endswith("%") and cells[0] != "Model":
            rows.append({"name": cells[0], "score": float(cells[2].rstrip(" %"))})
    return pd.DataFrame(rows)


def signals(src, mapping):
    text = pd.read_parquet(os.path.join(src, "text.parquet"))
    doc = pd.read_parquet(os.path.join(src, "document.parquet"))
    vec = load_vectara(os.path.join(src, "vectara.md"))
    out = []
    for model, names in mapping.items():
        for n in names.get("lmarena_text", []):
            for r in text[text.model_name == n].itertuples():
                out.append((model, f"lmarena_text:{r.category}", n, r.rating, r.vote_count, r.leaderboard_publish_date))
        for n in names.get("lmarena_document", []):
            for r in doc[(doc.model_name == n) & (doc.category == "overall")].itertuples():
                out.append((model, "lmarena_document", n, r.rating, r.vote_count, r.leaderboard_publish_date))
        for n in names.get("vectara", []):
            for r in vec[vec.name == n].itertuples():
                out.append((model, "vectara_fcr", n, r.score, None, None))
    df = pd.DataFrame(out, columns=["model", "signal", "variant", "score", "votes", "published"])
    df["effort"] = df.variant.map(effort)
    return df


def normalise(sig):
    """Per signal, over batch models only (one value per model: its best variant), to 0-1."""
    q = []
    for s, g in sig.groupby("signal"):
        ref = g.groupby("model").score.max()
        if s == "vectara_fcr":
            lo, hi = ref.min(), ref.max()
            q.append(0.1 + 0.8 * (g.score - lo) / (hi - lo))
        else:
            q.append(1 / (1 + 10 ** ((ref.median() - g.score) / 400)))
    sig["q"] = pd.concat(q)
    return sig


def pick(g, workload):
    """One variant per model and signal: highest effort for reason, lowest otherwise."""
    g = g.sort_values(["effort", "score"], ascending=[workload != "reason", False])
    return g.iloc[0]


def main(argv):
    fetch = "--fetch" in argv
    argv = [a for a in argv if a != "--fetch"]
    src, costs_csv, prefix = argv
    if fetch:
        os.makedirs(src, exist_ok=True)
        for f, u in URLS.items():
            urllib.request.urlretrieve(u, os.path.join(src, f))
    mapping = json.load(open(os.path.join(REF, "model-map.json")))["models"]
    cfg = json.load(open(os.path.join(REF, "workload-benchmarks.json")))["workloads"]
    sig = normalise(signals(src, mapping))
    sig.to_csv(f"{prefix}_signals.csv", index=False, float_format="%.4f")

    costs = pd.read_csv(costs_csv)
    rows = []
    for wl, spec in cfg.items():
        w = spec["signals"]
        for m in costs[costs.profile == wl].itertuples():
            have = sig[(sig.model == m.model) & (sig.signal.isin(w))]
            chosen = [pick(g, wl) for _, g in have.groupby("signal")]
            cov = sum(w[c.signal] for c in chosen)
            qual = sum(w[c.signal] * c.q for c in chosen) / cov if cov >= 0.5 else None
            rows.append({
                "snapshot_date": m.snapshot_date, "workload": wl, "model": m.model, "tier": m.tier,
                "quality": qual, "coverage": round(cov, 2),
                "usd_per_1k_no_cache": m.usd_per_1k_requests_no_cache,
                "usd_per_1k_cached": m.usd_per_1k_requests_cached,
                "variants_used": "; ".join(f"{c.signal}={c.variant}" for c in chosen),
                "reasoning_variant": any(c.effort >= 3 for c in chosen) and wl != "reason",
            })
    df = pd.DataFrame(rows)
    df["pareto"] = False
    df["good_enough_pick"] = False
    for wl, g in df[df.quality.notna()].groupby("workload"):
        g = g.sort_values(["usd_per_1k_no_cache", "quality"], ascending=[True, False])
        best = -1
        for i, r in g.iterrows():
            if r.quality > best:
                df.at[i, "pareto"] = True
                best = r.quality
        floor = 0.9 * g.quality.max()
        df.at[g[g.quality >= floor].index[0], "good_enough_pick"] = True
    df = df.sort_values(["workload", "quality"], ascending=[True, False])
    df.to_csv(f"{prefix}_value.csv", index=False, float_format="%.4f")
    write_md(df, cfg, f"{prefix}_value.md")


def write_md(df, cfg, path):
    L = ["# Benchmark-weighted value by workload",
         "",
         "*Generated by `scripts/benchmark_scores.py` (Claude Opus 5.5, 2026-10-31). Quality 0-1, 0.5 = median batch model. "
         "Cost = US$ per 1,000 requests, no cache, from entry 08. Only Pareto-frontier models are listed: none of them is beaten on both quality and cost. "
         "★ = cheapest model within 90% of the best quality. † = score came from a reasoning variant while the cost assumes reasoning off.*", ""]
    for wl in cfg:
        g = df[(df.workload == wl) & df.pareto].sort_values("usd_per_1k_no_cache")
        scored = df[(df.workload == wl) & df.quality.notna()]
        L += [f"## `{wl}`", "", f"Signals: {', '.join(f'{k} ×{v}' for k, v in cfg[wl]['signals'].items())}. "
              f"Scored: {len(scored)} of {len(df[df.workload == wl])} models.", "",
              "| Model | Tier | Quality | US$/1k | |", "| --- | --- | ---: | ---: | --- |"]
        for r in g.itertuples():
            mark = ("★" if r.good_enough_pick else "") + ("†" if r.reasoning_variant else "")
            L.append(f"| {r.model} | {r.tier} | {r.quality:.3f} | {r.usd_per_1k_no_cache:.4g} | {mark} |")
        L.append("")
    open(path, "w").write("\n".join(L))


if __name__ == "__main__":
    main(sys.argv[1:])
