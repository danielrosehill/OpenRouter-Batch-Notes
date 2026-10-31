---
title: OR Batch Inference Costs
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: static
pinned: false
license: cc-by-4.0
short_description: OpenRouter batch model costs by price tier
datasets:
- danielrosehill/OR-Batch-Inference-Models
---

# OpenRouter batch inference costs by tier

A static page that reads [danielrosehill/OR-Batch-Inference-Models](https://huggingface.co/datasets/danielrosehill/OR-Batch-Inference-Models)
in the browser and prices a job you set (input and output tokens) on every OpenRouter `:batch` model. Models are grouped into
Cheap / Mid / Expensive tiers by batch output price (rubric: [OpenRouter-Batch-Notes, entry 07](https://github.com/danielrosehill/OpenRouter-Batch-Notes/blob/main/notebook/07-price-tiers.md)).

The page lists `data/*.csv` in the dataset through the Hub API, so a new snapshot CSV shows up in the snapshot picker without changing the Space.
Source: `hf/space/` in the GitHub repo.
