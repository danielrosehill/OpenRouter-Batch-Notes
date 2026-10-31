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

## Reference snapshots

Dated copies of OpenRouter material in [`reference/`](reference/README.md), fetched 2026-10-31:

- Batch API docs, verbatim: [quickstart](reference/docs/2026-10-31_batch-quickstart.md) and [feature guide](reference/docs/2026-10-31_batch-api-feature-guide.md).
- [Models that support batch](reference/batch-models/2026-10-31_batch-models.md) ([JSON](reference/batch-models/2026-10-31_batch-models.json)): 71 `:batch` ids with prices and batch providers.

## Scripts

- [`scripts/or_batch_prices.py`](scripts/or_batch_prices.py): pulls the public
  `/api/v1/models` endpoint (no key needed) and prints every `:batch` id with its batch and sync
  price per million tokens, sorted cheapest first. Run with `python3 scripts/or_batch_prices.py`.

## Notation

- Prices are US$ per million tokens, written `input / output`, taken from `/api/v1/models`
  `pricing.prompt` and `pricing.completion` multiplied by 1e6.
- **Verified** means seen in a live API call or response. **Docs** means taken from OpenRouter's
  documentation and not independently tested.
