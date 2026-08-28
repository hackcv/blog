---
title: "Daily Research Brief 2026-03-21/22"
date: 2026-03-20T20:30:00+08:00
draft: false
tags: ["AI", "LLM", "Agent", "Computer Vision", "Audio-Video", "Engineering", "Daily Brief"]
categories: ["Research Brief"]
subtype: "daily"
description: "Daily research brief — AI / LLM / Agent / Computer Vision / Audio-Video / Engineering"
---

# Daily Research Brief 2026-03-21/22

📊 Token usage: estimated from retrieval and writing scale.

Covers the latest AI research, open source and industry moves, updated daily.

---

## Editor's Note

Weekend issue covering 03-19–03-22: a strong CV/generation thread (VEGA-3D, Matryoshka Gaussian Splatting, Cubic Discrete Diffusion, EffectErase), LLM/Agent work (FinTradeBench, Nemotron-Cascade 2, F2LLM-v2), and a notable open-source surge — ClawTeam's agent swarm (2,600+ stars in days). Note: Chinese community sources (Zhihu/Juejin) require login and were unavailable this period.

## 1. Latest arXiv Papers (03-19 ~ 03-22)

### CV / Multimodal / Generative Models

1. **VEGA-3D: Generation Models Know Space** — using the implicit 3D prior of video generation models for scene understanding; MLLMs are semantically strong but spatially blind.
   ⭐ Worth reading: frontier fusion of CV + generative models + 3D scene understanding.

2. **Matryoshka Gaussian Splatting** — adjustable-fidelity scene rendering (Level of Detail) from a single model; highly significant for practical 3D GS deployment.
   ⭐ Worth reading: engineering optimization + practical 3D reconstruction breakthrough.

3. **Cubic Discrete Diffusion: Discrete Visual Generation** — combining discrete diffusion with high-dim representation tokens, unifying visual generation into the token-prediction paradigm of language models.
   ⭐ Worth reading: new idea for unified multimodal token generation.

4. **EffectErase: Joint Video Object Removal and Insertion** — removing dynamic objects from video along with their visual effects (shadows, reflections) with high-quality restoration.
   ⭐ Worth reading: practical video editing + CV engineering.

5. **SAMA: Factorized Semantic Anchoring and Motion Alignment** — tackles the balance between semantic modification and motion preservation in instruction-guided video editing.

### LLM / Agent / Optimization

6. **FinTradeBench: Financial Reasoning Benchmark for LLMs** — a financial decision-reasoning benchmark requiring synthesis of company fundamentals and heterogeneous signals.
   ⭐ Worth reading: evaluation standard for LLM finance applications.

7. **Nemotron-Cascade 2: Post-Training LLMs** — post-training via Cascade RL + multi-domain on-policy distillation.
   ⭐ Worth reading: a new direction in LLM post-training.

8. **F2LLM-v2: Multilingual Embeddings (8 sizes, 80M-14B)** — multilingual general-purpose embedding models balancing inclusivity, performance and efficiency.

9. **DriveTok: 3D Driving Scene Tokenization** — a 3D driving-scene tokenization scheme unifying multi-view reconstruction and understanding.

10. **Not All Features Are Created Equal (VLA Models)** — mechanistic study of Vision-Language-Action models exposing feature-inequality issues.

## 2. Hot GitHub Open Source (past week)

| Project | ⭐ Stars | Notes |
|---------|---------|-------|
| **ClawTeam / HKUDS** | ⭐ 2,602 | Agent Swarm Intelligence — single command to full automation; HKU data-mining group |
| **wangziqi06/724-office** | ⭐ 530 | Self-evolving AI agent system — 26 tools, 3500 lines of pure Python, MCP / three-tier memory, self-repair |
| **NeoVertex1/nuggets** | ⭐ 315 | First holographic-memory AI assistant |
| **huggingface/hf-agents** | ⭐ 314 | Local coding agent driven by llama.cpp |
| **mattprusak/autoresearch-genealogy** | ⭐ 856 | Structured prompt templates for AI-assisted genealogy research |

> ⭐ **Watchlist: ClawTeam** — multi-agent swarm framework, 2600+ stars, architecture worth studying.

## 3. HackerNews Top Posts (03-20 ~ 03-22)

| Heat | Title | Link |
|------|-------|------|
| 🔥 116👍 24💬 | Patchwork – open-source framework automating dev chores | [github](https://github.com/patched-codes/patchwork) |
| 10👍 | Pomerium Agentic Access Gateway – dynamic auth for AI agents | — |
| 6👍 2💬 | Cheevly – natural-language IDE for building collaborative AI agents | — |
| 5👍 | nanochat rewritten in C++ (ggml inference) | [github](https://github.com/k-ye/nanochagg.ml) |
| 5👍 2💬 | Claude Sonnet 4.5 free (ad-supported) | — |
| 4👍 | Forge – 3MB Rust binary orchestrating multiple AI coding agents | [github](https://github.com/nxtg-ai/forge-orchestrator) |

## 4. Deep Reads

| Priority | Item | Direction |
|----------|------|-----------|
| 🌟 | **VEGA-3D** | CV + generative models + 3D scene understanding |
| 🌟 | **Cubic Discrete Diffusion** | unified multimodal token generation |
| 🌟 | **ClawTeam** | reference multi-agent swarm project |
| 💡 | **FinTradeBench** | LLM financial reasoning evaluation |
| 💡 | **724-office** | self-evolving AI agent engineering practice |

## Notes

- Zhihu / Juejin Chinese communities require login for their APIs, so auto-collection was unavailable this period.
- GitHub Trending direct connection is sometimes unstable; the fallback uses the GitHub API to search for newly popular projects over the past week.
- HackerNews posts are filtered for AI/ML relevance via the Algolia API.

---
