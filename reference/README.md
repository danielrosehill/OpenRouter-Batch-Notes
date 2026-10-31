# Reference snapshots

Dated copies of OpenRouter's own material, kept so the notebook can cite what the docs said on a given day. Filenames start with the fetch date (UTC). Add new snapshots alongside, never overwrite.

- `docs/2026-10-31_batch-quickstart.md`: verbatim https://openrouter.ai/docs/batch-quickstart.md (request shape, inputs, status, results, cancel/delete, provider routing).
- `docs/2026-10-31_batch-api-feature-guide.md`: verbatim https://openrouter.ai/docs/guides/features/batch-api.md (overview, pricing, limits).
- `batch-models/2026-10-31_batch-models.md` / `.json`: every model with a `:batch` id in `/api/v1/models`, with batch vs sync prices and batch providers from `/api/v1/models/{id}/endpoints`.

The doc pages are served as Markdown by appending `.md` to any docs URL; `https://openrouter.ai/docs/llms.txt` indexes them. Both model endpoints are public (no key). Fetched 2026-10-31T14:52:01Z.
