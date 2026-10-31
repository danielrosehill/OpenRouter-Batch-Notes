# 03 · Reasoning and JSON output

*Written by Claude Opus 5.5 · 2026-10-31 · observations from 2026-10-14 and 2026-10-22*

These were found on sync calls to DeepSeek V4.1 Flash via OpenRouter. They matter more in batch
work, because a mistake is multiplied across every row and you only find out when the batch
completes.

## Reasoning tokens bill as output

For reasoning models (gpt-oss, DeepSeek, GLM, the o-series), reasoning tokens are billed as output
and can multiply the output side of a job several times. None of the job costs in
[02](02-batch-vs-sync-pricing.md) include them.

## Turn reasoning off; don't just hide it (verified 2026-10-14)

| Setting | Reasoning tokens | Result |
| --- | --- | --- |
| `"reasoning": {"enabled": false}` | 0 | ~0.9 s, ~$0.00005 for a 3-sentence JSON reply |
| `"reasoning": {"effort": "none"}` | 0 | same as above |
| `"reasoning": {"effort": "low", "exclude": true}` | ~480 billed | about 8× the cost |

`exclude` only removes reasoning from the response. You still pay for it.

## Reasoning on with a small `max_tokens` gives empty answers (verified 2026-10-22)

With reasoning left at its default (on) and `max_tokens: 120`, the whole budget went on reasoning
and **every `content` came back `null`**, across a 6,046-prompt classification run. For
classification and labelling, send `"reasoning": {"enabled": false}` explicitly.

## `json_object` is not schema enforcement (verified 2026-10-22)

DeepSeek's API has no `json_schema` mode, so the schema goes in the system prompt with
`response_format: {"type": "json_object"}`. With reasoning off, about **1.7%** of rows came back
malformed:

- a list where a string was expected
- stray `": "` fragments
- wrong-case enum values
- `null` labels with confidence 0

A reasoning-on retry of just the failed rows fixed most of them. Nothing enforces enums, so
always normalise and validate after the batch, and plan a retry pass. Parse from the first `{`
rather than trusting the whole string to be JSON.

For models that do support `json_schema` (all 78 `:batch` ids on 2026-10-19 listed
`structured_outputs`), prefer it, though see [06](06-open-questions.md) on whether it holds
under batch.
