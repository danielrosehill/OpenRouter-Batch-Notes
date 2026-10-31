# 09 · Synthetic data: which models give varied, non-repetitive output

*Written by Claude Opus 5.5 · 2026-10-31 · own probe (`scripts/diversity_probe.py`, raw data in
[`reference/diversity/2026-10-31/`](../reference/diversity/2026-10-31/)) plus EQ-Bench Creative Writing v3
(fetched 2026-10-31 from `eqbench.com/creative_writing.js`)*

## The main finding: variety comes from the seed, not the model

The probe asked 11 batch-capable models the **same bare prompt** ten times each ("write a raw dictated to-do
list", temperature 1.0). Of the 110 samples, **91 mentioned the dentist and 83 dry cleaning**, across every
vendor. Models converge on the same "typical" content, and switching model does not fix that. Mixing models
does cut *wording* overlap: mean word-trigram Jaccard was 0.068 between samples from the same model and 0.023
between samples from different models. It does not change the topics.

So for synthetic data:

1. **Seed every item.** Generate a list of distinct situations/personas/attributes first (in chunks of about
   25, each chunk told to avoid the obvious). Then write one item per seed. Never sample N items from one
   prompt.
2. **Rotate two or three model families for the writing step**, so wording habits don't pile up in one
   direction.
3. **Deduplicate afterwards** with an n-gram or embedding near-duplicate pass.

## Probe results (n = 75 scenario items, 10 dictations per model; small sample, treat as directional)

| Model | Batch $/M in/out | Reasoning | Scenario nn_sim ↓ | Scenario top-3 share ↓ | Dictation 3-gram J ↓ | Dictation distinct-2 ↑ |
|---|---|---|---:|---:|---:|---:|
| `google/gemini-3.8-flash` | 0.375 / 1.875 | low (no off) | 0.150 | 0.32 | **0.034** | **0.68** |
| `z-ai/glm-5.3` | 0.45 / 2.00 | low (**mandatory**) | **0.111** | 0.38 | 0.041 | 0.63 |
| `google/gemini-3.1-flash-lite` | 0.125 / 0.75 | low | 0.153 | 0.41 | 0.042 | 0.65 |
| `deepseek/deepseek-v4.1-flash` | 0.05 / 0.15 | off | 0.132 | 0.37 | 0.057 | 0.57 |
| `openai/gpt-6-luna` | 0.05 / 0.25 | off | 0.210 | 0.56 | 0.061 | 0.63 |
| `anthropic/claude-haiku-5.5` | 0.05 / 0.25 | off | 0.152 | **0.23** | 0.064 | 0.59 |
| `z-ai/glm-5.3-flash` | 0.05 / 0.18 | low (**mandatory**) | 0.159 | 0.47 | 0.065 | 0.58 |
| `openai/gpt-oss-120b` | 0.03 / 0.136 | low (**mandatory**) | 0.192 | 0.61 | 0.067 | 0.56 |
| `qwen/qwen3.7-plus` | (batch, see 07) | off | 0.207 | 0.28 | 0.071 | 0.57 |
| `openai/gpt-5.6-luna` | 0.10 / 0.60 | off | 0.210 | 0.57 | 0.085 | 0.53 |
| `anthropic/claude-sonnet-5.5` | 1.00 / 5.00 | low (**mandatory**) | 0.159 | 0.36 | **0.162** | **0.47** |

- nn_sim: mean, over scenario items, of the highest content-word Jaccard to any other item. top-3 share: the
  share of items that use one of the model's three most frequent content words (topic clustering).
- **Sonnet 5.5 collapses hardest on an unseeded prompt.** Its trigram overlap is 2.5× the next model's, and
  every sample opened "Okay, so to-do list for tomorrow. Um, first thing, I need to call the dentist". This
  fits NoveltyBench's finding that larger and more reasoning-heavy models are less diverse. Seeded, it is
  still a strong writer. Don't use it for open sampling.
- **"Reasoning is mandatory for this endpoint and cannot be disabled"** (HTTP 400 on `{"enabled": false}`):
  `claude-sonnet-5.5`, `glm-5.3`, `glm-5.3-flash` and `gpt-oss-120b` on 2026-10-31. Send
  `{"effort": "low"}` and budget the extra output tokens.

## EQ-Bench Creative Writing v3 (public, prose quality; slop and repetition: lower is better)

| Model | Elo | Slop | Repetition | Batch $/M out |
|---|---:|---:|---:|---:|
| `glm-5.3` | 2076 | 8.4 | 3.23 | 2.00 |
| `kimi-k3` | 2083 | 9.7 | 3.73 | 11.40 |
| `gpt-5.6-luna` | 1832 | 11.8 | 4.00 | 0.60 |
| `claude-sonnet-5` | 1798 | 11.6 | 4.62 | 5.00 |
| `gemini-3.8-flash` | 1744 | 22.6 | 3.12 | 1.875 |
| `deepseek-v4.1-flash` | 1540 | 22.4 | 5.21 | 0.15 |
| `gemini-3.5-flash-lite` | 1559 | 25.2 | 5.25 | 1.25 |
| `gpt-oss-120b` | 956 | 31.4 | 4.03 | 0.136 |
| `gpt-5-nano` | 703 | 14.9 | 2.98 | 0.20 |

Not on the board on 2026-10-31: Haiku 5.5, Sonnet 5.5, GPT-6 Luna, GLM-5.3-Flash. **GLM-5.3 is the
outlier**: near-frontier prose (Elo 2076, the lowest slop of any affordable model) at a 1b-tier batch price.
Gemini 3.8 Flash varies its wording well but leans on stock "slop" words in long prose.

## Picks for synthetic data (2026-10-31)

| Step | Pick | Why |
|---|---|---|
| Seeds / scenario lists | `deepseek/deepseek-v4.1-flash` batch, or `claude-haiku-5.5` batch | Cheapest with low clustering. Haiku had the least topic clustering (0.23). |
| Writing items, quality first | `z-ai/glm-5.3` + `google/gemini-3.8-flash`, rotated | Best prose (GLM) and most varied wording (Gemini) |
| Writing items, volume first | `deepseek/deepseek-v4.1-flash` + `claude-haiku-5.5` + `google/gemini-3.1-flash-lite`, rotated | All under 0.75/M output. Rotation offsets DeepSeek's repetition score of 5.2. |
| Avoid for unseeded sampling | `claude-sonnet-5.5`, `openai/gpt-5.6-luna` | Most collapsed in the probe |
| Avoid for anything prose | `openai/gpt-oss-120b`, `openai/gpt-5-nano` | EQ-Bench Elo 956 / 703 |

## Sources

- EQ-Bench Creative Writing v3 data: https://eqbench.com/creative_writing.html (data in `creative_writing.js`)
- NoveltyBench (Zhang et al., 2025): https://arxiv.org/abs/2504.05228
