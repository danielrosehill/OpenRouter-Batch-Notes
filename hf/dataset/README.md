---
license: cc-by-4.0
pretty_name: OpenRouter Batch Inference Models
language:
- en
tags:
- openrouter
- llm-pricing
- batch-inference
- tabular
size_categories:
- n<1K
configs:
- config_name: default
  data_files:
  - split: snapshot_2026_10_31
    path: data/batch_models_2026-10-31.csv
---

# OpenRouter Batch Inference Models

Every model with a `:batch` id on [OpenRouter](https://openrouter.ai) on **2026-10-31** (71 models),
with batch and sync prices, the providers that serve batch, and a price-tier label.

- Source: public `https://openrouter.ai/api/v1/models` and `/api/v1/models/{id}/endpoints`,
  fetched 2026-10-31T14:52:01Z. No key needed.
- Prices: US$ per million tokens, base tier, from `pricing.prompt` / `pricing.completion` × 1e6.
- Each snapshot is a split named `snapshot_YYYY_MM_DD`. New snapshots are added, never overwritten.
- Visualiser: [danielrosehill/OR-Batch-Inference-Costs](https://huggingface.co/spaces/danielrosehill/OR-Batch-Inference-Costs).
- Source notebook and scripts: [danielrosehill/OpenRouter-Batch-Notes](https://github.com/danielrosehill/OpenRouter-Batch-Notes)
  (rubric: `notebook/07-price-tiers.md`, tiering: `scripts/price_tiers.py`).

Prices change often. Re-check on the day you rely on them.

## Columns

| Column | Meaning |
| --- | --- |
| `snapshot_date` | Date the prices were fetched (UTC) |
| `model_listed_utc` | Date OpenRouter first listed the model (`created`). Not the date batch support arrived |
| `model` / `batch_id` / `name` | Sync slug, batch slug to submit, display name |
| `context_length` | Tokens |
| `input_modalities` | `;`-separated |
| `batch_input_usd_per_m`, `batch_output_usd_per_m` | Batch price per million tokens |
| `sync_input_usd_per_m`, `sync_output_usd_per_m` | Sync price for the same model (empty if not listed) |
| `batch_providers` | `;`-separated providers serving the `:batch` route |
| `tier`, `tier_rank` | `Cheap` (1), `Mid` (2), `Expensive` (3), by batch output price |
| `sub_band` | `1a` ≤ 1.00, `1b` 1.00–3.00, `2a` 3–8, `2b` 8–20, `3a` 20–50, `3b` ≥ 50 (output $/M) |
| `input_band` | `Cheap` < 0.60, `Mid` 0.60–3.00, `Expensive` ≥ 3.00 (input $/M) |
| `input_mismatch` | `True` when `input_band` ≠ `tier` (the model moves tier on input-heavy jobs) |
| `out_in_ratio` | Batch output price ÷ batch input price |
| `reference_job_usd` | Cost of 4.5M input + 0.5M output tokens at batch prices (a bulk-labelling job shape) |

Tier boundaries sit in the widest gaps of the 2026-10-31 output-price ladder
(2.50 → 3.75, 7.50 → 10, 15 → 25, 37.50 → 60).

*Compiled by Claude Opus 5.5 for Daniel Rosehill, 2026-10-31.*
