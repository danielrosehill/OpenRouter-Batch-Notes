# 09 · Benchmark-weighted value per workload

*Written by Claude Opus 5.5 · 2026-10-31 · benchmarks fetched 2026-10-31, costs from [08](08-workload-profiles.md)*

Entry 08 gives what each workload costs on each model. This entry adds an estimate of how good
each model is at that workload, taken from public benchmarks, and finds the models worth paying
for. The method is deliberately small: two open sources, one to three signals per workload.

- Signals and weights: [`reference/benchmarks/workload-benchmarks.json`](../reference/benchmarks/workload-benchmarks.json)
- OpenRouter id → benchmark name mapping (hand-made): [`reference/benchmarks/model-map.json`](../reference/benchmarks/model-map.json)
- Every matched score, all variants: [`reference/benchmarks/2026-10-31_signals.csv`](../reference/benchmarks/2026-10-31_signals.csv)
- Per model × workload (568 rows): [`reference/benchmarks/2026-10-31_value.csv`](../reference/benchmarks/2026-10-31_value.csv)
- Pareto tables: [`reference/benchmarks/2026-10-31_value.md`](../reference/benchmarks/2026-10-31_value.md)
- Regenerate: `uv run --no-project --with pandas --with pyarrow python -I scripts/benchmark_scores.py --fetch /tmp/bench-src reference/workloads/<date>_workload-costs.csv reference/benchmarks/<date>`

## Is there a batch-inference benchmark?

No. A search on 2026-10-31 found no public leaderboard that measures quality against cost on
high-volume jobs (labelling, extraction, synthetic data). Everything below is a proxy. The
real measure is a labelled pilot of your own: cost per correct output.

## Sources used

| Source | What | Coverage of the 71 batch ids | Access |
| --- | --- | ---: | --- |
| LMArena text | Elo by category (instruction following, creative writing, hard prompts, expert, non-English, longer query, maths, coding), published 2026-10-28 | 58 | HF `lmarena-ai/leaderboard-dataset`, config `text`, CC-BY-4.0 |
| LMArena document | Elo for questions about an uploaded document, published 2026-09-13 | 24 | same dataset, config `document` |
| Vectara hallucination leaderboard | Factual consistency rate when summarising, updated 2026-10-22 | 33 | GitHub `vectara/hallucination-leaderboard` README table |

Not covered by LMArena: all nine `-pro` ids and `gpt-6.1-terra`. `gpt-5.4-pro` has only a Vectara score.

**Not used: Artificial Analysis.** It has the better-fitting evals (IFBench, AA-LCR long
context, GPQA, HLE, tau2), but its API needs a free key (`x-api-key`, 1,000 requests a day,
attribution required) and its terms forbid scraping the site. There was no key in Infisical or
1Password on 2026-10-31. With a key, AA-LCR should replace the document arena for `doc_qa` and
IFBench should join instruction following for `classify`, `extract` and `synth`.

**Considered and rejected as stale or leaderboard-less:** JSONSchemaBench (last updated
2025-03), StructEval (2025-09), RewardBench 2 (2025-12), AgoraBench (2024-12), NoveltyBench (no
leaderboard), and LiveBench categories (2025-04).

## Signals per workload

| Workload | Signals (weight) |
| --- | --- |
| `classify` | instruction_following 1.0 |
| `extract` | instruction_following 0.6, hard_prompts 0.4 |
| `summarise` | Vectara factual consistency 0.4, document arena 0.4, longer_query 0.2 |
| `doc_qa` | document arena 0.7, longer_query 0.3 |
| `judge` | expert 0.5, hard_prompts 0.5 |
| `translate` | non_english 1.0. There is no Hebrew category, so Hebrew is not measured. |
| `synth` | creative_writing 0.5, instruction_following 0.5 |
| `reason` | math 0.5, coding 0.5 |

The weights are judgement calls, not fitted.

## Scoring

```
Elo signal    q = 1 / (1 + 10^((median − rating) / 400))     chance of beating the median batch model
Vectara       q = 0.1 + 0.8 × (fcr − min) / (max − min)       over the batch models with a score
quality       = Σ wᵢ qᵢ / Σ wᵢ   over the signals the model has
coverage      = Σ wᵢ present; quality left blank below 0.5
```

- **Pareto frontier:** sort by cost (no cache) and keep each model that beats every cheaper one on quality.
- **Good-enough pick (★):** the cheapest model with at least 90% of the best quality in that workload.
- **Variant rule:** LMArena lists reasoning-effort variants separately. `reason` uses the
  highest-effort variant. Every other workload uses the lowest-effort one, because entry 08's costs
  assume reasoning off.
- **Reasoning flag (†):** for about 39% of models, the only variant LMArena lists is a high- or
  max-effort one. That covers most newer models: GPT-5.x/6, Gemini 3.6–4, Claude 5.x, DeepSeek V4.1 Flash.
  Their score then overstates what you get with reasoning off, or the cost understates what you
  pay to get that score. The `reasoning_variant` column flags these rows.

## What it shows (2026-10-31)

The frontier is nearly the same for every LMArena-scored workload:

| Step | Model | Quality (synth) | US$/1k (synth) |
| --- | --- | ---: | ---: |
| cheapest | gpt-oss-20b | 0.23 | 0.26 |
| | gpt-oss-120b | 0.32 | 0.32 |
| ~median quality at ~$0.4 | DeepSeek V4.1 Flash † | 0.54 | 0.38 |
| | **GLM-5.3 Flash** (no reasoning tag) | 0.54 | 0.44 |
| ★ good-enough pick | Gemini 3.8 Flash † | 0.59 | 4.31 |
| top end | Gemini 4 Argon †, Claude Opus 5.5 † | 0.64–0.65 | 11.5–23 |

- **GLM-5.3 Flash and DeepSeek V4.1 Flash cover the cheap end.** They score around the median batch
  model at roughly a tenth of the price of the ★ pick. GLM-5.3 Flash's LMArena entry carries no
  effort tag, so its score is the one most likely to hold with reasoning off. It is the ★ pick for
  `judge` and `reason`.
- **For `synth`**, going from GLM-5.3 Flash to Gemini 3.8 Flash costs about 10× for +0.04 quality,
  and going to Opus 5.5 about 50× for +0.10. With prompt pairs, a cheap generator plus a filtering
  pass is likely the better spend. That is inferred, not tested.
- **The gpt-oss models are cheapest but well below median** on every LMArena category.
- **`summarise`**: DeepSeek V4.1 Flash is the ★ pick, with Vectara factual consistency of 95.8%. Only
  gpt-5.4-nano scores higher (96.9%), at 2.4× the cost. The top of this table rests mostly on
  Vectara, because the cheap models aren't in the document arena (coverage 0.6). 39 models are scored.
- **`doc_qa` is the weakest table:** 24 models, none of them in the cheapest group, because the
  document arena doesn't list them. Treat it as a gap.

## Caveats

- Arena Elo is human preference on chat prompts, not task accuracy. A preferred answer isn't
  necessarily a correct label.
- Elo compresses the range: the whole field sits between about 0.2 and 0.65, so read small gaps as ties.
- The name mapping is by hand. Dated snapshots (GPT-4o, o3-mini, the older Claude models) may not be the
  exact snapshot OpenRouter serves.
- Credit LMArena (CC-BY-4.0) and Vectara when republishing.
