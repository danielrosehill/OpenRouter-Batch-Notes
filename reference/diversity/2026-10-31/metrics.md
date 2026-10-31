| Model | Reasoning | Scen. items | Scen. dup | Scen. nn_sim | Scen. top-3 share (words) | Dict. 3-gram J | Dict. distinct-2 | Same opening | Errors | Cost $ (13 calls) |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| `google/gemini-3.8-flash` | off | 75 | 0.03 | 0.150 | 0.32 (room, snacks, supplies) | 0.034 | 0.68 | 0.6 | 0 | 0.0149 |
| `z-ai/glm-5.3` | low | 50 | 0.00 | 0.111 | 0.38 (assistant, between, grocery) | 0.041 | 0.63 | 0.3 | 0 | 0.0082 |
| `google/gemini-3.1-flash-lite` | off | 75 | 0.00 | 0.153 | 0.41 (kitchen, standing, supplies) | 0.042 | 0.65 | 0.7 | 0 | 0.0080 |
| `deepseek/deepseek-v4.1-flash` | off | 75 | 0.00 | 0.132 | 0.37 (grocery, home, supplies) | 0.057 | 0.57 | 0.8 | 0 | 0.0016 |
| `openai/gpt-6-luna` | off | 75 | 0.00 | 0.210 | 0.56 (adds, checking, records) | 0.061 | 0.63 | 0.8 | 0 | 0.0015 |
| `anthropic/claude-haiku-5.5` | off | 75 | 0.00 | 0.152 | 0.23 (car, man, store) | 0.064 | 0.59 | 0.7 | 0 | 0.0028 |
| `z-ai/glm-5.3-flash` | low | 75 | 0.05 | 0.159 | 0.47 (between, man, supplies) | 0.065 | 0.58 | 1.0 | 0 | 0.0006 |
| `openai/gpt-oss-120b` | low | 77 | 0.00 | 0.192 | 0.61 (grocery, new, records) | 0.067 | 0.56 | 0.0 | 0 | 0.0009 |
| `qwen/qwen3.7-plus` | off | 75 | 0.05 | 0.207 | 0.28 (add, adds, student) | 0.071 | 0.57 | 0.9 | 0 | 0.0043 |
| `openai/gpt-5.6-luna` | off | 75 | 0.03 | 0.210 | 0.57 (records, store, supplies) | 0.085 | 0.53 | 1.0 | 0 | 0.0035 |
| `anthropic/claude-sonnet-5.5` | low | 75 | 0.00 | 0.159 | 0.36 (kitchen, man, woman) | 0.162 | 0.47 | 1.0 | 0 | 0.0608 |
