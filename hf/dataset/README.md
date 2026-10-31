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

## Data dictionary

Machine-readable copy: [`data_dictionary.json`](data_dictionary.json). **Origin** says where a value comes from:

- **api**: retrieved from OpenRouter's public API at fetch time, reformatted only (units, joins).
- **enriched**: added by us, either computed from API fields by a stated rule or a judgement label. OpenRouter does not publish these.

| Column | Origin | Type | Meaning |
| --- | --- | --- | --- |
| `snapshot_date` | enriched | date | UTC date the API was fetched. Same for every row of a file. |
| `model_listed_utc` | api | date | Date OpenRouter first listed the model (`created`, Unix time to UTC date). Not the date batch support arrived. |
| `model` | api | string | Sync model slug (`id` with `:batch` removed). |
| `batch_id` | api | string | Batch slug (`id`) to submit batches with. |
| `name` | api | string | Display name (`name`). |
| `context_length` | api | integer | Context window in tokens (`context_length`). |
| `input_modalities` | api | string | `architecture.input_modalities`, `;`-separated. |
| `batch_input_usd_per_m` | api | number | Batch input price, US$ per million tokens (`pricing.prompt` x 1e6, base tier). |
| `batch_output_usd_per_m` | api | number | Batch output price, US$ per million tokens (`pricing.completion` x 1e6, base tier). |
| `sync_input_usd_per_m` | api | number or null | Input price of the sync id for the same model. Empty if the sync id is not listed. |
| `sync_output_usd_per_m` | api | number or null | Output price of the sync id for the same model. Empty if not listed. |
| `batch_providers` | api | string | Providers serving the `:batch` id, from `/api/v1/models/{id}/endpoints`, `;`-separated. |
| `canonical_slug` | api | string | `canonical_slug`: OpenRouter's permanent slug, usually the model name plus a release-date stamp. |
| `hugging_face_id` | api | string or null | `hugging_face_id`: weights repo for open-weight models. Empty for closed models. |
| `expiration_date` | api | date or null | `expiration_date`: announced retirement date. Empty if none announced. |
| `tier` | enriched | string | Cheap / Mid / Expensive by batch output price: < $3, $3-20, >= $20 per million. Rule: notebook/07-price-tiers.md, scripts/price_tiers.py. |
| `tier_rank` | enriched | integer | 1 = Cheap, 2 = Mid, 3 = Expensive. |
| `sub_band` | enriched | string | 1a <= 1.00, 1b 1-3, 2a 3-8, 2b 8-20, 3a 20-50, 3b >= 50 (batch output $/M). |
| `input_band` | enriched | string | Cheap < 0.60, Mid 0.60-3.00, Expensive >= 3.00 (batch input $/M). |
| `input_mismatch` | enriched | boolean | True when input_band differs from tier: the model changes tier on input-heavy jobs. |
| `out_in_ratio` | enriched | number | batch_output_usd_per_m / batch_input_usd_per_m, 1 decimal. |
| `reference_job_usd` | enriched | number | Cost in US$ of 4.5M input + 0.5M output tokens at batch prices (bulk-labelling job shape, 9:1). |
| `stable_endpoint` | enriched | boolean | True if the id resolves to one fixed model version. False for dynamic aliases (`~` prefix or `latest` in the id, which OpenRouter says 'always redirects to the latest model') and for closed models whose canonical_slug has no date stamp (an upstream alias the provider can repoint). Rule: scripts/build_hf_dataset.py. |
| `stability_basis` | enriched | string | Which branch of the stable_endpoint rule applied. |

Tier boundaries sit in the widest gaps of the 2026-10-31 output-price ladder
(2.50 → 3.75, 7.50 → 10, 15 → 25, 37.50 → 60).

## Endpoint stability

`stable_endpoint` says whether the id always resolves to the same model version. OpenRouter's
dynamic aliases (`~google/gemini-flash-latest`, `~anthropic/claude-sonnet-latest` and 18 others
on 2026-10-31) silently move to each new release. **None of them has a `:batch` id**, so every
alias is excluded from batch by construction. Three batch models are still labelled unstable:
`openai/gpt-4o`, `openai/gpt-4o-mini` and `openai/gpt-4-turbo`. Their `canonical_slug` carries no
date, so they map to OpenAI's undated names, which OpenAI can repoint to a newer snapshot (it
did so for `gpt-4o` in 2024). That they are aliases is inferred from the undated slug. OpenRouter
does not state it. The other 68 have a dated `canonical_slug` (66) or are open weights with a fixed
Hugging Face repo (2, gpt-oss).

*Compiled by Claude Opus 5.5 for Daniel Rosehill, 2026-10-31.*
