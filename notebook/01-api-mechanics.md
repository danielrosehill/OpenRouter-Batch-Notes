# 01 · Batch API mechanics

*Written by Claude Opus 5.5 · 2026-10-31 · observations from 2026-10-14 and 2026-10-22*

Docs: <https://openrouter.ai/docs/batch-quickstart>

## Two ways to say "batch"

1. **`:batch` model variants** (e.g. `openai/gpt-oss-20b:batch`). These appear in
   `/api/v1/models` with their own pricing. A model is batch-capable when a `<id>:batch` variant
   exists: 78 of 470 models on 2026-10-19, 75 of 468 on 2026-10-22. Browse them at
   <https://openrouter.ai/models?variant=batch>.
2. **The Batch endpoint, `POST /api/v1/batches`** (verified 2026-10-22). This is the real
   submission route. It takes the **base** model id; the endpoint is what selects batch pricing,
   so strip any `:batch` suffix.

A 2026-10-14 call to a `:batch` id returned `202` with status `validating`, so batch requests
are asynchronous whichever way you send them. Never put one behind an interactive button.

## Request shape

```json
{
  "endpoint": "/v1/chat/completions",
  "model": "deepseek/deepseek-v4.1-flash",
  "provider": { "only": ["deepseek"] },
  "completion_window": "24h",
  "requests": [
    { "custom_id": "row-0001", "body": { "messages": [ { "role": "user", "content": "…" } ] } }
  ]
}
```

- `endpoint`, `model`, `provider` and `completion_window` must come **before** `requests` in the
  body, or the API returns 400 (docs).
- Each `body` is an ordinary chat-completions body.
- `24h` is the only accepted `completion_window` (verified 2026-10-14).

## Lifecycle (verified 2026-10-22)

- Submit returns `{"id": "batch-…", "status": "validating"}`.
- **`GET /api/v1/batches/{id}` returns 404 "not found" for a short time right after submit.**
  Treat it as "not visible yet" and keep polling; a poller that retries for 5 minutes was
  enough.
- Statuses: `validating → in_progress → finalizing → completed | failed | expired | cancelled`.
- Results come **inline** on the completed batch object, in `results`, **out of order**:
  `{custom_id, response: {status_code, body}}` or `{custom_id, error}`. Join on `custom_id`.
- `GET /api/v1/batches` (the list) returns `results: null`; fetch each batch by id.
- The batch's `usage.cost` is the actual charge in US$.

## Timing

- Median completion was about 7 minutes at launch (docs, noted 2026-10-14).
- A 2-row test batch completed in 60 s (2026-10-22).

## Limits (docs, noted 2026-10-22)

- 200 MB per batch; text only.
- Artifacts are deleted after 30 days, and the batch then returns `410`.
- No cancel endpoint. `DELETE` works only on finished batches.
- At submit, the estimated cost is checked against the account's credit balance.
