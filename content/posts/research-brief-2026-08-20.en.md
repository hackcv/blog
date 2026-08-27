---
title: "Daily Research Brief 2026-08-20"
date: 2026-08-20T20:30:00+08:00
draft: false
tags: ["AI", "LLM", "Agent", "Computer Vision", "Audio-Video", "Engineering", "Daily Brief"]
categories: ["Research Brief"]
description: "Daily research brief — AI / LLM / Agent / Computer Vision / Audio-Video / Engineering"
---

# Daily Research Brief 2026-08-20

📊 Token usage: estimated from retrieval and writing scale.

Covers the latest AI research, open source and industry moves, updated daily.

---

## Editor's Note

The one thing worth recording today: capability increments are moving from "model weights" to "execution systems + authorization boundaries". StateM spent nothing on training — only rebuilding the harness (persistent state, staged context, verifiable transitions, recoverable runbooks) — to push Terminal-Bench 2.1 raw accuracy to 95.3%, or hit the same score at ~$15 of API spend vs the GPT reference line's $574.68. The same day, Demystifying Agent Skills used 8,135 trial records to explain why skills work: **65.7% of gains come from "program anchoring", not injected knowledge**, and retrieval precision collapses from 29.6% to 3.3% as the skill pool grows from 5 to 100.

## 1. Latest arXiv Papers

1. **What is Missing from AI Post-Training AI: An Empirical Analysis** — https://arxiv.org/abs/2608.19072
2. **Bayesian Partner Modelling enables Adaptive Replanning for LLM Coordination** — https://arxiv.org/abs/2608.18490
3. **StateM: Reaching 95.3% Raw Accuracy, or a $15 Frontier Run, on Terminal-Bench 2.1 via Harness Scaling** — https://arxiv.org/abs/2608.15089
4. **Demystifying Agent Skills: Why They Work-Until They Don't** — https://arxiv.org/abs/2608.14036
5. **ASI-Bench: At the Dawn of Artificial Superintelligence** — https://arxiv.org/abs/2608.17271
6. **When Agents Act on Web3: An Attack-Surface Survey of MCP, Skills, and Tool Calling** — https://arxiv.org/abs/2608.17275
7. **Physics of Agents: Statistical Mechanics Predicts Collective Behavior of AI Agents** — https://arxiv.org/abs/2608.16578
8. **Embodied-Navigator: Point, Think, Memorize, and Align for Efficient Navigation** — https://arxiv.org/abs/2608.17512

## 2. Hot GitHub Open Source

- **deepseek-harness** ecosystem surging (130k★ in 4 days); task-aware routing suites (dsh-routing-suite, sprix-sage-router) charting independently
- **ponytail** (111.8k★) — "cognitive restraint, default-don't-implement" agents
- **OpenBot** (CopilotKit) — containerized agents with review-before-act governance gates

## 3. Selected Industry News

- **StateM vs GPT reference line**: harness-only scaling reaches frontier results at ~$15 vs $574.68
- **OpenAI**: admits underestimating model offensive cyber capability (HF incident); pauses two weeks of large-scale training
- **Anthropic**: watermarks on all models; archives "Model 2" over alignment risk
- **NVIDIA AVO**: same Claude Opus 5 hit 25/25 on ARC-AGI-3 public set
