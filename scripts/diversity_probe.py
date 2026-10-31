#!/usr/bin/env python3
"""Synthetic-data diversity probe: how repetitive is each model when asked for the same kind of item many times?

  with-secrets python3 -I scripts/diversity_probe.py reference/diversity/<date>   # writes raw.jsonl + metrics.json + metrics.md

Two tasks, both from a real synthetic-data job (Dictation-Format-Adapters, 2026-10-31):
  scenarios  3 independent calls, each "list 25 situations where someone dictates a shopping list". Measures
             near-duplicates within and across calls (the failure that wastes a synthetic-data budget).
  dictation  10 independent calls of the SAME prompt "write a raw dictated to-do list". Measures mode collapse:
             how alike 10 samples of one prompt are.
Same prompts, temperature 1.0, reasoning off where the endpoint allows it; Gemini, and any model that answers
400 "Reasoning is mandatory" (on 2026-10-31: claude-sonnet-5.5, glm-5.3, glm-5.3-flash, gpt-oss-120b), run at effort low
(recorded per row as `reasoning`). Sync calls: the
models are the same as their :batch ids, only the price differs.

Metrics (stdlib, no embeddings):
  jaccard3     mean pairwise word-trigram Jaccard between samples (lower = more varied)
  distinct2    unique word bigrams / all bigrams over the pooled samples (higher = more varied)
  dup_rate     share of scenario items with a near-duplicate (content-word Jaccard >= 0.5) elsewhere in the 75
  nn_sim       mean over scenario items of the highest content-word Jaccard to any other item (lower = more spread)
  top3_share   share of scenario items containing one of the model's 3 most used content words (topic clustering)
  opening_rep  share of dictation samples whose first 4 words match another sample's first 4 words
"""
import itertools, json, os, re, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

MODELS = [
    "anthropic/claude-haiku-5.5", "anthropic/claude-sonnet-5.5", "openai/gpt-6-luna", "openai/gpt-5.6-luna",
    "google/gemini-3.8-flash", "google/gemini-3.1-flash-lite", "deepseek/deepseek-v4.1-flash", "z-ai/glm-5.3-flash",
    "z-ai/glm-5.3", "openai/gpt-oss-120b", "qwen/qwen3.7-plus",
]
SCEN = ("List 25 varied, realistic situations in which one person dictates a shopping list by voice into a phone. "
        "Vary who, where, why and how organised they are. JSON array of 25 strings only, one sentence each.")
DICT = ("Write the raw speech-to-text transcript of someone dictating a to-do list into their phone in one take: "
        "punctuated, one block, natural speech with fillers and a false start. 60-120 words. Output only the transcript.")


MANDATORY = set()


def call(model, prompt, max_tokens):
    low = model.startswith("google/") or model in MANDATORY
    body = {"model": model, "max_tokens": max_tokens + (2000 if low else 0), "temperature": 1.0,
            "reasoning": {"effort": "low"} if low else {"enabled": False},
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
                                          "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=180))
            return {"text": (d["choices"][0]["message"].get("content") or "").strip(), "served": d.get("model"),
                    "reasoning": "low" if low else "off",
                    "provider": d.get("provider"), "cost": (d.get("usage") or {}).get("cost")}
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code} {e.read().decode()[:200]}"
            if "mandatory" in err and not low:
                MANDATORY.add(model)
                return call(model, prompt, max_tokens)
            time.sleep(3 * (attempt + 1))
        except Exception as e:  # noqa: BLE001
            err = str(e)
            time.sleep(3 * (attempt + 1))
    return {"text": "", "error": err}


words = lambda t: re.findall(r"[a-z']+", t.lower())
grams = lambda w, n: {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def jac(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


STOP = set("""a an the and or but of to in on at for with by from into onto while as is are was were be being been his her
their they them he she it its who whom this that these those one someone person people their own up out about after
before during because so then than what when where which how into while over under via your you i my me we our
dictates dictating dictate shopping list lists phone voice item items into while has have had""".split())


def metrics(texts, items):
    w = [words(t) for t in texts if t]
    tri = [grams(x, 3) for x in w]
    pairs = list(itertools.combinations(range(len(tri)), 2))
    bi_all = [g for x in w for g in zip(x, x[1:])]
    out = {"n": len(w), "jaccard3": round(sum(jac(tri[i], tri[j]) for i, j in pairs) / max(len(pairs), 1), 4),
           "distinct2": round(len(set(bi_all)) / max(len(bi_all), 1), 4)}
    if items is not None:
        uni = [set(words(s)) - STOP for s in items]
        nn = [max((jac(uni[i], uni[j]) for j in range(len(uni)) if j != i), default=0) for i in range(len(uni))]
        freq = {}
        for u in uni:
            for x in u:
                freq[x] = freq.get(x, 0) + 1
        top3 = set(sorted(freq, key=freq.get, reverse=True)[:3])
        out |= {"items": len(items), "dup_rate": round(sum(x >= 0.5 for x in nn) / max(len(nn), 1), 4),
                "nn_sim": round(sum(nn) / max(len(nn), 1), 4),
                "top3_share": round(sum(bool(u & top3) for u in uni) / max(len(uni), 1), 4), "top3": sorted(top3)}
    else:
        op = [" ".join(x[:4]) for x in w]
        out["opening_rep"] = round(sum(op.count(o) > 1 for o in op) / max(len(op), 1), 4)
    return out


def main(outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    raw = out / "raw.jsonl"
    have = {(r["model"], r["task"], r["k"]): r for r in map(json.loads, raw.read_text().splitlines())
            if r.get("text")} if raw.exists() else {}  # rerun only what failed
    jobs = [(m, "scenarios", k, SCEN, 2500) for m in MODELS for k in range(3)] + \
           [(m, "dictation", k, DICT, 600) for m in MODELS for k in range(10)]
    todo = [j for j in jobs if j[:3] not in have]
    with ThreadPoolExecutor(12) as ex:
        new = list(ex.map(lambda j: {"model": j[0], "task": j[1], "k": j[2]} | call(j[0], j[3], j[4]), todo))
    res = list(have.values()) + new
    raw.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in res))
    table = {}
    for m in MODELS:
        sc = [r for r in res if r["model"] == m and r["task"] == "scenarios"]
        items = []
        for r in sc:
            try:
                items += [s for s in json.loads(re.search(r"\[.*\]", r["text"], re.S).group()) if isinstance(s, str)]
            except (AttributeError, json.JSONDecodeError):
                pass
        dc = [r["text"] for r in res if r["model"] == m and r["task"] == "dictation"]
        table[m] = {"scenarios": metrics(items, items), "dictation": metrics(dc, None),
                    "cost_usd": round(sum(r.get("cost") or 0 for r in res if r["model"] == m), 5),
                    "served": sorted({r.get("served") for r in res if r["model"] == m and r.get("served")}),
                    "errors": sum(1 for r in res if r["model"] == m and not r["text"]),
                    "reasoning": "/".join(sorted({r.get("reasoning", "off") for r in res if r["model"] == m and r.get("text")})) or "-"}
    (out / "metrics.json").write_text(json.dumps(table, indent=1))
    rows = ["| Model | Reasoning | Scen. items | Scen. dup | Scen. nn_sim | Scen. top-3 share (words) | Dict. 3-gram J | Dict. distinct-2 | Same opening | Errors | Cost $ (13 calls) |",
            "|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|"]
    for m, t in sorted(table.items(), key=lambda kv: kv[1]["dictation"]["jaccard3"]):
        s, d = t["scenarios"], t["dictation"]
        rows.append(f"| `{m}` | {t['reasoning']} | {s.get('items', 0)} | {s.get('dup_rate', 0):.2f} | {s.get('nn_sim', 0):.3f} | "
                    f"{s.get('top3_share', 0):.2f} ({', '.join(s.get('top3', []))}) | {d['jaccard3']:.3f} | "
                    f"{d['distinct2']:.2f} | {d['opening_rep']:.1f} | {t['errors']} | {t['cost_usd']:.4f} |")
    (out / "metrics.md").write_text("\n".join(rows) + "\n")
    print("\n".join(rows))


if __name__ == "__main__":
    main(sys.argv[1])
