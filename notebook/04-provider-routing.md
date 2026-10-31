# 04 · Provider routing

*Written by Claude Opus 5.5 · 2026-10-31 · observation from 2026-10-22*

## Unpinned batches go to whichever host is cheapest

On 2026-10-22 an unpinned DeepSeek V4.1 Flash batch ran on the host **"Sail Research"**, not on
DeepSeek itself. Without a provider preference, OpenRouter picks the cheapest eligible host for the
batch.

That matters when:

- the data shouldn't go to an arbitrary third-party host;
- outputs must come from the first-party model (quantisation and serving settings differ between
  hosts, so labels may not be comparable with a sync run on another host);
- you need results reproducible across runs.

## Pin with `provider.only`

```json
"provider": { "only": ["deepseek"], "allow_fallbacks": false }
```

Put `provider` before `requests` in the body (see [01](01-api-mechanics.md)). Pinning can change
the price, because the cheapest host was the one doing the work, so re-check the cost after you
pin.

## Check which host ran it

OpenRouter's chat-completion responses normally carry a `provider` field. It's assumed, not
verified, that each row's `response.body` in a batch does too. If it does, record it alongside
the results.
