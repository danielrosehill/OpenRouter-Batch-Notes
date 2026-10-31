# OpenRouter models with batch variants, 2026-10-31

Snapshot taken 2026-10-31T14:51:47+00:00 from `https://openrouter.ai/api/v1/models (ids ending ':batch') + /api/v1/models/{id}/endpoints`. 71 models. A model supports batch inference when `/api/v1/models` lists a `<slug>:batch` id (the docs' "batch models list", https://openrouter.ai/models?variant=batch). Submit batches with the base slug; the `:batch` id is where batch pricing is published. Prices are US$ per million tokens, `input / output`, base tier (long-context overrides omitted; see the JSON). Batch providers come from `/api/v1/models/{id}/endpoints` for the `:batch` id.

| Model (submit as) | Context | Batch in/out | Sync in/out | Batch providers |
| --- | ---: | ---: | ---: | --- |
| `anthropic/claude-fable-5.1` | 1,000,000 | 5 / 25 | 10 / 50 | Anthropic |
| `anthropic/claude-fable-5` | 1,000,000 | 5 / 25 | 10 / 50 | Anthropic |
| `anthropic/claude-haiku-4.5` | 200,000 | 0.5 / 2.5 | 1 / 5 | Anthropic |
| `anthropic/claude-haiku-5.5` | 1,000,000 | 0.05 / 0.25 | 0.1 / 0.5 | Anthropic |
| `anthropic/claude-opus-4.1` | 200,000 | 7.5 / 37.5 | 15 / 75 | Anthropic |
| `anthropic/claude-opus-4.5` | 200,000 | 2.5 / 12.5 | 5 / 25 | Anthropic |
| `anthropic/claude-opus-4.6` | 1,000,000 | 2.5 / 12.5 | 5 / 25 | Anthropic |
| `anthropic/claude-opus-4.7` | 1,000,000 | 2.5 / 12.5 | 5 / 25 | Anthropic |
| `anthropic/claude-opus-4.8` | 1,000,000 | 2.5 / 12.5 | 5 / 25 | Anthropic |
| `anthropic/claude-opus-5.5` | 1,000,000 | 2 / 10 | 4 / 20 | Anthropic |
| `anthropic/claude-opus-5` | 1,000,000 | 2.5 / 12.5 | 5 / 25 | Anthropic |
| `anthropic/claude-sonnet-4.5` | 1,000,000 | 1.5 / 7.5 | 3 / 15 | Anthropic |
| `anthropic/claude-sonnet-4.6` | 1,000,000 | 1.5 / 7.5 | 3 / 15 | Anthropic |
| `anthropic/claude-sonnet-5.5` | 1,000,000 | 1 / 5 | 2 / 10 | Anthropic |
| `anthropic/claude-sonnet-5` | 1,000,000 | 1 / 5 | 2 / 10 | Anthropic |
| `deepseek/deepseek-v4.1-flash` | 1,048,576 | 0.05 / 0.15 | 0.045 / 0.5 | Sail Research, DeepInfra |
| `google/gemini-3-flash-preview` | 1,048,576 | 0.25 / 1.5 | 0.5 / 3 | Google |
| `google/gemini-3.1-flash-lite` | 1,048,576 | 0.125 / 0.75 | 0.25 / 1.5 | Google |
| `google/gemini-3.1-pro-preview` | 1,048,576 | 1 / 6 | 2 / 12 | Google |
| `google/gemini-3.5-flash-lite` | 1,048,576 | 0.15 / 1.25 | 0.3 / 2.5 | Google |
| `google/gemini-3.5-flash` | 1,048,576 | 0.75 / 4.5 | 1.5 / 9 | Google |
| `google/gemini-3.6-flash` | 1,048,576 | 0.375 / 1.875 | 0.75 / 3.75 | Google |
| `google/gemini-3.7-flash` | 1,048,576 | 0.375 / 1.875 | 0.75 / 3.75 | Google |
| `google/gemini-3.8-flash` | 1,048,576 | 0.375 / 1.875 | 0.825 / 4.125 | Google |
| `google/gemini-4-argon` | 1,048,576 | 1 / 5 | 2 / 10 | Google |
| `mistralai/mistral-medium-3-5` | 262,144 | 0.75 / 3.75 | 1.5 / 7.5 | Mistral |
| `moonshotai/kimi-k3` | 1,048,576 | 2.28 / 11.4 | 0.192 / 15 | DeepInfra |
| `openai/gpt-4-turbo` | 128,000 | 5 / 15 | n/a | OpenAI |
| `openai/gpt-4.1-mini` | 1,047,576 | 0.2 / 0.8 | 0.4 / 1.6 | OpenAI |
| `openai/gpt-4.1-nano` | 1,047,576 | 0.05 / 0.2 | 0.1 / 0.4 | OpenAI |
| `openai/gpt-4.1` | 1,047,576 | 1 / 4 | 2 / 8 | OpenAI |
| `openai/gpt-4o-mini` | 128,000 | 0.075 / 0.3 | 0.15 / 0.6 | OpenAI |
| `openai/gpt-4o` | 128,000 | 1.25 / 5 | 2.5 / 10 | OpenAI |
| `openai/gpt-5-mini` | 400,000 | 0.125 / 1 | 0.25 / 2 | OpenAI |
| `openai/gpt-5-nano` | 400,000 | 0.025 / 0.2 | 0.05 / 0.4 | OpenAI |
| `openai/gpt-5-pro` | 400,000 | 7.5 / 60 | 15 / 120 | OpenAI |
| `openai/gpt-5.1` | 400,000 | 0.625 / 5 | 1.25 / 10 | OpenAI |
| `openai/gpt-5.2-pro` | 400,000 | 10.5 / 84 | 21 / 168 | OpenAI |
| `openai/gpt-5.2` | 400,000 | 0.875 / 7 | 1.75 / 14 | OpenAI |
| `openai/gpt-5.4-mini` | 400,000 | 0.375 / 2.25 | 0.75 / 4.5 | OpenAI |
| `openai/gpt-5.4-nano` | 400,000 | 0.1 / 0.625 | 0.2 / 1.25 | OpenAI |
| `openai/gpt-5.4-pro` | 1,050,000 | 15 / 90 | 30 / 180 | OpenAI |
| `openai/gpt-5.4` | 1,050,000 | 1.25 / 7.5 | 2.5 / 15 | OpenAI |
| `openai/gpt-5.5-pro` | 1,050,000 | 15 / 90 | 30 / 180 | OpenAI |
| `openai/gpt-5.5` | 1,050,000 | 2.5 / 15 | 5 / 30 | OpenAI |
| `openai/gpt-5.6-luna-pro` | 1,050,000 | 0.1 / 0.6 | 0.2 / 1.2 | OpenAI |
| `openai/gpt-5.6-luna` | 1,050,000 | 0.1 / 0.6 | 0.2 / 1.2 | OpenAI |
| `openai/gpt-5.6-sol-pro` | 1,050,000 | 2 / 10 | 4 / 20 | OpenAI |
| `openai/gpt-5.6-sol` | 1,050,000 | 2 / 10 | 4 / 20 | OpenAI |
| `openai/gpt-5.6-terra-pro` | 1,050,000 | 1 / 6 | 2 / 12 | OpenAI |
| `openai/gpt-5.6-terra` | 1,050,000 | 1 / 6 | 2 / 12 | OpenAI |
| `openai/gpt-5` | 400,000 | 0.625 / 5 | 1.25 / 10 | OpenAI |
| `openai/gpt-6-astra-pro` | 1,050,000 | 5 / 25 | 10 / 50 | OpenAI |
| `openai/gpt-6-astra` | 1,050,000 | 5 / 25 | 10 / 50 | OpenAI |
| `openai/gpt-6-luna-pro` | 1,050,000 | 0.05 / 0.25 | 0.1 / 0.5 | OpenAI |
| `openai/gpt-6-luna` | 1,050,000 | 0.05 / 0.25 | 0.1 / 0.5 | OpenAI |
| `openai/gpt-6-sol-pro` | 1,050,000 | 1 / 5 | 2 / 10 | OpenAI |
| `openai/gpt-6-sol` | 1,050,000 | 1 / 5 | 2 / 10 | OpenAI |
| `openai/gpt-6.1-sol-pro` | 1,050,000 | 1 / 5 | 2 / 10 | OpenAI |
| `openai/gpt-6.1-sol` | 1,050,000 | 1 / 5 | 2 / 10 | OpenAI |
| `openai/gpt-6.1-terra-pro` | 1,050,000 | 0.5 / 2.5 | 1 / 5 | OpenAI |
| `openai/gpt-6.1-terra` | 1,050,000 | 0.5 / 2.5 | 1 / 5 | OpenAI |
| `openai/gpt-oss-120b` | 131,072 | 0.0296 / 0.136 | 0.15 / 0.6 | DeepInfra |
| `openai/gpt-oss-20b` | 131,072 | 0.024 / 0.112 | 0.018 / 0.09 | DeepInfra |
| `openai/o3-mini` | 200,000 | 0.55 / 2.2 | n/a | OpenAI |
| `openai/o3` | 200,000 | 1 / 4 | 2 / 8 | OpenAI |
| `openai/o4-mini` | 200,000 | 0.55 / 2.2 | n/a | OpenAI |
| `qwen/qwen3.7-plus` | 262,144 | 0.23 / 0.92 | 0.32 / 1.28 | Alibaba |
| `x-ai/grok-4.3` | 1,000,000 | 1 / 2 | 1.25 / 2.5 | xAI |
| `z-ai/glm-5.3-flash` | 1,048,576 | 0.05 / 0.18 | 0.0163 / 0.1479 | Sail Research, DeepInfra |
| `z-ai/glm-5.3` | 1,048,576 | 0.45 / 2 | 0.0699 / 1.4 | DeepInfra |
