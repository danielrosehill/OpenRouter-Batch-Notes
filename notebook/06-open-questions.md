# 06 · Open questions

*Written by Claude Opus 5.5 · 2026-10-31*

None of these had been tested by 2026-10-31.

- **The 2026-10-22 sync price for DeepSeek V4.1 Flash.** It was recorded as 0.30 / 1.20, ten
  times the 2026-10-19 sync reading (0.028 / 0.080). It may be a transcription error or a real
  change; it wasn't re-pulled.
- **Does `json_schema` / `structured_outputs` hold under batch?** All `:batch` ids advertise it.
  Enum enforcement in particular hasn't been tested on a real batch.
- **Price and host after pinning.** How much does `provider.only` raise the cost against the
  unpinned cheapest host?
- **Large batches.** Only small test batches and sync runs of about 6,000 rows have been
  measured. Real completion times for batches of thousands of rows are unknown.
- **Failure modes.** No batch has yet ended `failed` or `expired`, so it's unknown whether
  partial results are returned and how a failed batch is charged.
- **Why batch is sometimes dearer.** The single-route explanation in
  [02](02-batch-vs-sync-pricing.md) is inferred, not confirmed by OpenRouter.
