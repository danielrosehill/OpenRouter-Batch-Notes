# 02 · Batch vs sync pricing

*Written by Claude Opus 5.5 · 2026-10-31 · prices observed 2026-10-14, 2026-10-19, 2026-10-22*

## Headline

**OpenRouter batch is not a flat 50% discount.** For first-party lab models it usually is; for
open-weight models served by third-party hosts, batch can be *dearer* than sync. Compare both
on the day you submit.

The likely reason: a sync id's price is the cheapest provider's price across all its hosts,
while a batch id is priced on a single route.

## 2026-10-19 snapshot (`/api/v1/models`, 78 `:batch` ids)

US$ per million tokens. "Job" is one pass of 2,500 rows × 1,800 input and 200 output tokens
(4.5M in, 0.5M out) at batch prices, with reasoning tokens excluded.

| Model id | batch in / out | sync in / out | Job |
| --- | --- | --- | --- |
| `openai/gpt-oss-20b:batch` | 0.024 / 0.112 | 0.018 / 0.090 | $0.16 |
| `openai/gpt-oss-120b:batch` | 0.030 / 0.136 | 0.150 / 0.600 | $0.20 |
| `openai/gpt-5-nano:batch` | 0.025 / 0.200 | 0.050 / 0.400 | $0.21 |
| `deepseek/deepseek-v4.1-flash:batch` | 0.050 / 0.150 | 0.028 / 0.080 | $0.30 |
| `z-ai/glm-5.3-flash:batch` | 0.050 / 0.180 | 0.048 / 0.160 | $0.32 |
| `google/gemini-2.5-flash-lite:batch` | 0.050 / 0.200 | 0.100 / 0.400 | $0.33 |
| `anthropic/claude-haiku-5.5:batch` | 0.050 / 0.250 | 0.100 / 0.500 | $0.35 |
| `mistralai/mistral-small-2603:batch` | 0.075 / 0.300 | 0.150 / 0.600 | $0.49 |
| `google/gemini-3.1-flash-lite:batch` | 0.125 / 0.750 | 0.250 / 1.500 | $0.94 |
| `qwen/qwen3.7-plus:batch` | 0.230 / 0.920 | 0.320 / 1.280 | $1.50 |
| `anthropic/claude-sonnet-5.5:batch` | 1.000 / 5.000 | 2.000 / 10.000 | $7.00 |
| `anthropic/claude-opus-5.5:batch` | 2.000 / 10.000 | 4.000 / 20.000 | $14.00 |

All 78 `:batch` ids listed both `structured_outputs` and `response_format` in
`supported_parameters`.

### What the snapshot shows

- **Flat 50%** for the OpenAI, Anthropic, Google and Mistral ids.
- **About 80% off** for `openai/gpt-oss-120b` (0.030 vs 0.150 input).
- **Batch dearer than sync** for `deepseek-v4.1-flash`, `gpt-oss-20b`, `glm-5.3-flash`,
  `glm-5.3` (input 0.45 vs 0.079) and `kimi-k3` (input 2.28 vs 0.239).

## Prices move within days

- 2026-10-14: `deepseek/deepseek-v4.1-flash:batch` was 0.112 / 0.336 against sync
  0.020 / 0.891. Input dearer, output cheaper.
- 2026-10-19: the same batch id was 0.050 / 0.150 against sync 0.028 / 0.080. Dearer on both
  sides.
- 2026-10-22: the batch price was recorded as 0.05 / 0.15, now cheaper than sync. The sync figure
  noted that day (0.30 / 1.20) doesn't fit the 10-19 reading and wasn't re-checked; see
  [06](06-open-questions.md).
- `gpt-oss-20b:batch` and `glm-5.3-flash:batch` were dearer than sync on both 2026-10-19 and
  2026-10-22.

## Cost is rarely the deciding factor at small scale

The whole 2,500-row pass costs cents on the cheap tier and $7 on Sonnet 5.5; even 50,000 rows
on Sonnet 5.5 batch is about $140. At that scale, choose the model on output quality against a
gold set, then use batch-vs-sync only to pick the cheaper lane for that model.

## Reproduce

`python3 scripts/or_batch_prices.py` prints the current table.
