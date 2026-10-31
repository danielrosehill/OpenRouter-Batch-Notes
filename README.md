# OpenRouter Batch Notes

A research notebook on batch inference through [OpenRouter](https://openrouter.ai): the
Batch API's mechanics, how batch pricing compares with sync, and the traps hit while running
bulk labelling and generation jobs.

> **Attribution.** Every entry in this notebook was written by **Claude Opus 5.5**
> (`claude-opus-5-5`) on **2026-10-31**, compiled from Daniel Rosehill's working notes and
> live API runs made between 2026-10-14 and 2026-10-22. Each fact carries the date it was
> observed. OpenRouter prices and model lists change often, so re-check anything here on the
> day you rely on it.

## Entries

| # | Entry | What it covers |
| --- | --- | --- |
| 01 | [API mechanics](notebook/01-api-mechanics.md) | `POST /api/v1/batches`, request shape, statuses, results, limits |
| 02 | [Batch vs sync pricing](notebook/02-batch-vs-sync-pricing.md) | Batch is not a flat 50% off; price tables from 2026-10-14 and 2026-10-19 |
| 03 | [Reasoning and JSON output](notebook/03-reasoning-and-json.md) | Turning reasoning off, `exclude` still bills, malformed JSON rates |
| 04 | [Provider routing](notebook/04-provider-routing.md) | Unpinned batches go to whichever host is cheapest; `provider.only` |
| 05 | [When to use batch](notebook/05-when-to-use-batch.md) | Decision rules distilled from the above |
| 06 | [Open questions](notebook/06-open-questions.md) | Things not yet verified |
| 07 | [Price tiers](notebook/07-price-tiers.md) | Rubric sorting the 2026-10-31 batch models into cheap / mid / expensive by output price, with input-side exceptions |

## Reference snapshots

Dated copies of OpenRouter material in [`reference/`](reference/README.md), fetched 2026-10-31:

- Batch API docs, verbatim: [quickstart](reference/docs/2026-10-31_batch-quickstart.md) and [feature guide](reference/docs/2026-10-31_batch-api-feature-guide.md).
- [Models that support batch](reference/batch-models/2026-10-31_batch-models.md) ([JSON](reference/batch-models/2026-10-31_batch-models.json)): 71 `:batch` ids with prices and batch providers.

## Hugging Face

- Dataset (public): [danielrosehill/OR-Batch-Inference-Models](https://huggingface.co/datasets/danielrosehill/OR-Batch-Inference-Models). One CSV per snapshot in `data/`, split `snapshot_YYYY_MM_DD`: the batch-models snapshot plus the tier columns from entry 07. Source: `hf/dataset/`.
- Space (public, static): [danielrosehill/OR-Batch-Inference-Costs](https://huggingface.co/spaces/danielrosehill/OR-Batch-Inference-Costs). Prices a job you set (input and output tokens) on every model, by tier. Reads the dataset in the browser and lists `data/*.csv` through the Hub API, so a new snapshot needs no Space change. Source: `hf/space/`.
- Columns are documented in `hf/dataset/data_dictionary.json` (each tagged `api` or `enriched`). `stable_endpoint` marks ids that resolve to one fixed model version: on 2026-10-31 none of OpenRouter's 20 dynamic `-latest` aliases had a `:batch` id, and only `openai/gpt-4o`, `gpt-4o-mini` and `gpt-4-turbo` (undated `canonical_slug`) were labelled unstable.
- To add a snapshot: save the batch-models CSV, run `scripts/price_tiers.py`, save the full API records as `reference/batch-models/<date>_api-records.json`, then `python3 -I scripts/build_hf_dataset.py <date> .` writes `hf/dataset/data/batch_models_<date>.csv`; add a split for it to the `configs` block in `hf/dataset/README.md`, then `with-secrets bash -c 'export HF_TOKEN; hf upload danielrosehill/OR-Batch-Inference-Models hf/dataset . --repo-type dataset'`.

## Scripts

- [`scripts/or_batch_prices.py`](scripts/or_batch_prices.py): pulls the public
  `/api/v1/models` endpoint (no key needed) and prints every `:batch` id with its batch and sync
  price per million tokens, sorted cheapest first. Run with `python3 scripts/or_batch_prices.py`.
- [`scripts/build_hf_dataset.py`](scripts/build_hf_dataset.py): joins a snapshot's prices, tiers and API records into the HF dataset CSV and adds the `stable_endpoint` label (rule in the docstring). Checks columns against `hf/dataset/data_dictionary.json`.
- [`scripts/price_tiers.py`](scripts/price_tiers.py): assigns each model in a batch-models CSV
  snapshot to a price tier (rubric in entry 07) and writes `<prefix>.csv` and `<prefix>.md`.
  Run with `python3 -I scripts/price_tiers.py <snapshot.csv> <out-prefix>`.

## Notation

- Prices are US$ per million tokens, written `input / output`, taken from `/api/v1/models`
  `pricing.prompt` and `pricing.completion` multiplied by 1e6.
- **Verified** means seen in a live API call or response. **Docs** means taken from OpenRouter's
  documentation and not independently tested.
