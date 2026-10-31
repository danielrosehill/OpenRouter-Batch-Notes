# 08 · Workload profiles and cache weighting

*Written by Claude Opus 5.5 · 2026-10-31 · prices from the 2026-10-31 snapshot (`hf/dataset/data/batch_models_2026-10-31.csv`, 71 `:batch` ids)*

Per-token prices don't tell you what a job costs until you know its shape. This entry defines
eight common batch workloads as per-request token shapes and costs each one on every batch
model, with and without prompt caching. The token shapes are **assumed**, chosen to be typical.
They were not measured from real runs. Swap in your own figures from a pilot's `usage`.

- Profiles: [`reference/workloads/workload-profiles.json`](../reference/workloads/workload-profiles.json)
- Costs, long format (568 rows = 71 models × 8 profiles): [`reference/workloads/2026-10-31_workload-costs.csv`](../reference/workloads/2026-10-31_workload-costs.csv)
- Matrix, US$ per 1,000 requests: [`reference/workloads/2026-10-31_workload-costs.md`](../reference/workloads/2026-10-31_workload-costs.md)
- Regenerate: `python3 -I scripts/workload_costs.py hf/dataset/data/batch_models_<date>.csv reference/workloads/workload-profiles.json reference/workloads/<date>_workload-costs`

## Weightings

`in:out` is the ratio of input to output tokens. `cache` is the share of input that is an
identical prefix (system prompt, schema, few-shot examples, shared document) and so can be
cached. Output counts hidden reasoning tokens, because they bill as output.

| Profile | Tokens in / out per request | in : out | Input share | Output share | Cacheable share of input |
| --- | --- | --- | ---: | ---: | ---: |
| `classify`: classification / labelling | 1,600 / 20 | 80 : 1 | 98.8% | 1.2% | 75% |
| `doc_qa`: many questions over one long document | 20,000 / 300 | 67 : 1 | 98.5% | 1.5% | 97.5% |
| `summarise`: document summarisation | 8,000 / 600 | 13 : 1 | 93.0% | 7.0% | 0% |
| `judge`: LLM-as-judge / eval grading | 3,000 / 250 | 12 : 1 | 92.3% | 7.7% | 50% |
| `extract`: structured extraction to JSON | 4,000 / 500 | 8 : 1 | 88.9% | 11.1% | 30% |
| `translate`: translation / rewriting | 2,000 / 900 | 2.2 : 1 | 69.0% | 31.0% | 60% |
| `synth`: synthetic data generation | 1,500 / 2,000 | 1 : 1.3 | 42.9% | 57.1% | 80% |
| `reason`: reasoning-heavy solving | 1,000 / 5,000 | 1 : 5 | 16.7% | 83.3% | 0% |

The 9:1 reference job in [07](07-price-tiers.md) sits between `extract` and `judge`.

## Formula

Blended price per million total tokens, with `w_in` and `w_out` the input and output shares and
`c` the cached share of input:

```
blended $/M = w_in × [ (1 − c) × p_in + c × p_cache ] + w_out × p_out
p_cache     = (1 − 1/R) × p_read + (1/R) × p_write        R = requests per cache write (20 assumed)
p_write     = published input_cache_write, else p_in
```

Without caching, `c = 0` and this reduces to `w_in × p_in + w_out × p_out`. The script applies the
same formula per request and reports US$ per 1,000 requests.

**Cache assumptions** (`cache_assumptions` in the profiles file):

- Best case: every cacheable token hits (hit rate 1.0). Real hit rates are lower.
- One cache write per 20 requests. This only matters where a write premium exists (1.25× input
  for Anthropic and OpenAI's GPT-5.6 Sol / GPT-6 / GPT-6.1).
- Shared prefixes under 1,024 tokens are counted as uncacheable, because OpenAI and Anthropic
  don't cache below that. That is why `summarise` and `reason` get 0%.
- **Unverified:** OpenRouter does not say whether requests in one batch hit each other's cache.
  The batch guide says only "prompt caching rates vary by model" (see
  [`06`](06-open-questions.md)). Treat the cached columns as an upper bound on savings until a
  pilot's `usage` shows cached tokens.

## What the numbers show (2026-10-31)

Best-case saving from caching, across the 60 models that publish a cache price:

| Profile | Saving range | Cheapest cached (US$ / 1k requests) |
| --- | --- | --- |
| `doc_qa` | 44 – 86% | gpt-5-nano 0.14, DeepSeek V4.1 Flash 0.19, Haiku 5.5 0.25 |
| `classify` | 34 – 67% | gpt-5-nano 0.018, DeepSeek V4.1 Flash 0.031, Haiku 5.5 0.035 |
| `judge` | 18 – 35% | gpt-5-nano 0.093, gpt-oss-20b 0.10, DeepSeek V4.1 Flash 0.12 |
| `translate` | 10 – 25% | gpt-oss-20b 0.15, gpt-oss-120b 0.18, DeepSeek V4.1 Flash 0.18 |
| `extract` | 10 – 19% | gpt-oss-20b 0.15, gpt-5-nano 0.17, gpt-oss-120b 0.19 |
| `synth` | 6 – 17% | gpt-oss-20b 0.26, gpt-oss-120b 0.32, DeepSeek V4.1 Flash 0.32 |
| `summarise`, `reason` | 0% | gpt-oss-20b 0.26 / 0.58 |

- **Caching only matters for input-heavy jobs with a big shared prefix** (`doc_qa`, `classify`).
  There it can reorder models: gpt-oss-20b has no cache price, so it is cheapest for `classify`
  without caching but behind gpt-5-nano, DeepSeek and Haiku 5.5 with it.
- **Output-heavy jobs ignore caching.** For `synth` and `reason` the output price decides the
  cost. Rank by `batch_output_usd_per_m` (the tiers in 07).
- **Cheap reads beat cheap input at the top end.** On `doc_qa`, Sonnet 5.5 drops from $21.50 to
  $4.15 per 1,000 requests and Opus 5.5 from $43 to $8.29, because their cache read is 0.05× input.
  Older OpenAI models (GPT-4o 0.5×, GPT-4.1 / o3 0.25×) save far less.
- Per-model figures for every profile are in the matrix file.
