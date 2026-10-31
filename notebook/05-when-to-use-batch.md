# 05 · When to use batch

*Written by Claude Opus 5.5 · 2026-10-31 · distilled from entries 01–04*

1. **Interactive or latency-bound?** Use sync. Batch is asynchronous with a 24 h window.
2. **Bulk, offline, can wait minutes to hours?** Batch is a candidate. Go on to 3.
3. **Pull prices on the day** (`scripts/or_batch_prices.py`) and compare batch with sync for the
   exact model.
   - OpenAI, Anthropic, Google and Mistral ids: batch has been a reliable 50% off.
   - Open-weight ids (DeepSeek, GLM, Kimi, small gpt-oss): batch has been dearer than sync on
     some days. If sync is cheaper, run sync calls in a thread pool instead.
4. **Reasoning model?** Send `"reasoning": {"enabled": false}` unless the task needs it, and
   never rely on `exclude` to save money.
5. **Data sensitivity or reproducibility?** Pin the provider with `provider.only`.
6. **Pilot first.** Submit a handful of rows, confirm the output parses and the real
   `usage.cost` matches the estimate, then submit the full set.
7. **Validate afterwards.** Join results on `custom_id`, normalise, validate against the
   schema, and retry the failures (with reasoning on if they're malformed).

Cheapest batch ids seen on 2026-10-19 for short JSON labelling: `openai/gpt-oss-20b:batch`,
`openai/gpt-oss-120b:batch`, `openai/gpt-5-nano:batch`.
