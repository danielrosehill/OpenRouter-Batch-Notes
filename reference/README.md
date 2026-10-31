# Reference snapshots

Dated copies of OpenRouter's own material, kept so the notebook can cite what the docs said on a given day. Filenames start with the fetch date (UTC). Add new snapshots alongside, never overwrite.

- `docs/2026-10-31_batch-quickstart.md`: verbatim https://openrouter.ai/docs/batch-quickstart.md (request shape, inputs, status, results, cancel/delete, provider routing).
- `docs/2026-10-31_batch-api-feature-guide.md`: verbatim https://openrouter.ai/docs/guides/features/batch-api.md (overview, pricing, limits).
- `batch-models/2026-10-31_batch-models.md` / `.json`: every model with a `:batch` id in `/api/v1/models`, with batch vs sync prices and batch providers from `/api/v1/models/{id}/endpoints`.
- `batch-models/2026-10-31_batch-models.csv` and `.pdf`: the same list sorted newest to oldest by the model's `created` date (when OpenRouter listed the model; the `:batch` id carries the same timestamp, so it is not the date batch support arrived). The PDF is built with `typst compile 2026-10-31_batch-models.typ` from the CSV, run inside `reference/batch-models/`.

The doc pages are served as Markdown by appending `.md` to any docs URL; `https://openrouter.ai/docs/llms.txt` indexes them. Both model endpoints are public (no key). Fetched 2026-10-31T14:52:01Z.
