#!/usr/bin/env python3
"""Charts for the benchmark-value report (entry 09), as SVG.

Usage: uv run --no-project --with pandas --with matplotlib python -I scripts/report_charts.py \
           reference/benchmarks/<date>_value.csv <out-dir>
Writes synth.svg (headline scatter), workloads.svg (8 small multiples) and coverage.svg.
Palette: dataviz reference categorical slots 1-3 (validated all-pairs, light mode); tier is also
encoded by marker shape because aqua sits below 3:1 contrast. Written by Claude Opus 5.5, 2026-10-31.
"""
import os
import sys

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

TIER = {"Cheap": ("#2a78d6", "o"), "Mid": ("#eb6834", "s"), "Expensive": ("#1baf7a", "D")}
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
ORDER = ["classify", "extract", "summarise", "doc_qa", "judge", "translate", "synth", "reason"]
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 8, "text.color": INK,
                     "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "svg.fonttype": "none"})


def short(m):
    return m.split("/", 1)[1]


def panel(ax, g, labels, title=None):
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xscale("log")
    f = g[g.pareto].sort_values("usd_per_1k_no_cache")
    ax.step(f.usd_per_1k_no_cache, f.quality, where="post", color=INK2, lw=1, ls="--", zorder=1)
    for t, (c, mk) in TIER.items():
        d = g[g.tier == t]
        ax.scatter(d.usd_per_1k_no_cache, d.quality, s=22 if labels else 12, c=c, marker=mk,
                   edgecolors=SURF, linewidths=1, zorder=2, label=t)
    star = g[g.good_enough_pick]
    ax.scatter(star.usd_per_1k_no_cache, star.quality, s=120 if labels else 60, marker="*",
               facecolors="none", edgecolors=INK, linewidths=0.9, zorder=3)
    if labels:
        for i, r in enumerate(f.itertuples()):  # alternate above/below to avoid collisions
            ax.annotate(short(r.model) + (" †" if r.reasoning_variant else ""),
                        (r.usd_per_1k_no_cache, r.quality), xytext=(9, 3 if i % 2 else -10),
                        textcoords="offset points", fontsize=7, color=INK)
    if title:
        ax.set_title(title, fontsize=8.5, loc="left", color=INK)


def main(csv, out):
    os.makedirs(out, exist_ok=True)
    df = pd.read_csv(csv)
    df = df[df.quality.notna()]

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    panel(ax, df[df.workload == "synth"], labels=True)
    ax.set_xlabel("US$ per 1,000 requests (log scale, no cache)")
    ax.set_ylabel("Quality (0.5 = median batch model)")
    ax.legend(title="Price tier", frameon=False, loc="lower right", fontsize=7, title_fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "synth.svg"))

    fig, axes = plt.subplots(2, 4, figsize=(9.6, 4.6), sharey=True)
    for ax, wl in zip(axes.flat, ORDER):
        g = df[df.workload == wl]
        panel(ax, g, labels=False, title=f"{wl}  (n={len(g)})")
    for ax in axes[1]:
        ax.set_xlabel("US$ / 1k requests (log)")
    for ax in axes[:, 0]:
        ax.set_ylabel("Quality")
    h, lab = axes.flat[0].get_legend_handles_labels()
    fig.legend(h, lab, title="Price tier", frameon=False, loc="upper right", ncol=3, fontsize=7,
               title_fontsize=7)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(os.path.join(out, "workloads.svg"))

    n = df.groupby("workload").size().reindex(ORDER)
    fig, ax = plt.subplots(figsize=(7.2, 2.2))
    ax.barh(n.index[::-1], n.values[::-1], color="#2a78d6", height=0.6)
    ax.axvline(71, color=INK2, lw=0.8, ls=":")
    ax.text(71, 7.6, " 71 batch ids", color=INK2, fontsize=7, va="center")
    for y, v in enumerate(n.values[::-1]):
        ax.text(v + 0.8, y, str(v), va="center", fontsize=7, color=INK)
    ax.set_xlim(0, 80)
    ax.set_xlabel("Models with a quality score")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "coverage.svg"))


if __name__ == "__main__":
    main(*sys.argv[1:])
