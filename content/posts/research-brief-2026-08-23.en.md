---
title: "Daily Research Brief 2026-08-23"
date: 2026-08-23T20:30:00+08:00
draft: false
tags: ["AI", "LLM", "Agent", "Computer Vision", "Audio-Video", "Engineering", "Daily Brief"]
categories: ["Research Brief"]
subtype: "daily"
description: "Daily research brief — AI / LLM / Agent / Computer Vision / Audio-Video / Engineering"
---

# Daily Research Brief 2026-08-23

📊 Token usage: estimated from retrieval and writing scale.

Covers the latest AI research, open source and industry moves, updated daily.

---

## Editor's Note

Today's strong signal: "the agent race has formally shifted from model worship to systems engineering" — papers, open source and industry all point at the runtime layer around the model.

## 1. Latest arXiv Papers

### 1. Task-CoEvolve: Efficient Harness Optimization via Adaptive Validation Task Selection

**Abstract**: Harness optimization rewrites harness code to improve LLM agents without touching weights — but current methods re-run the full validation set every round even when tasks have lost discriminative power. Task-CoEvolve co-evolves the validation task set with the harness: variance-weighted sampling from history focuses the evaluation budget on the most divergent tasks, with a sampling-aware estimator recovering full-set scores from partial evaluation. Stable gains over fixed-subset baselines on online text classification and Terminal-Bench 2.1, matching full-set search's final performance while cutting evaluation calls by **80%** during optimization.

**Link**: https://arxiv.org/abs/2608.20169

### 2. Optimal Skill Selection for LLM Agents with Provable Bicriteria Guarantees

**Abstract**: Fitting reusable skill documents into a limited context window is the main way agents gain task capability — but current methods score skills independently and take top-k, with no quality guarantee and no token-cost awareness. This work gives the first model of "how a skill set determines execution outcome", formalizes selection as maximizing monotone submodular reward minus context penalty under a hard token budget, and proposes BPS with a bicriteria (1−1/e, 1) approximation. On a contamination-controlled BigCodeBench variant, BPS hits 0.73 task success vs 0.20–0.52 for skill routers/text retrievers/self-selection, using **28% fewer tokens** than the strongest router.

**Link**: https://arxiv.org/abs/2608.19993

### 3. MileGPO: Milestone Inference with Local Evidence for Graph-Based Policy Optimization of Long-Horizon LLM Agents

**Abstract**: Derives process-level credit for long-horizon agents via milestone inference with local evidence in graph-based policy optimization.

**Link**: https://arxiv.org/abs/2608.19803

### 4. Harness Continual Learning: Continual Adaptation Beyond Model Parameters

**Abstract**: Proposes "harness-level continual learning" — prompt/memory/skills keep drifting while the model is frozen, requiring each peripheral update to be regression-tested like a code commit.

**Link**: https://arxiv.org/abs/2608.19013

### 5. SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning

**Abstract**: A single-rollout autoregressive policy optimization method sharing policy/value backbones, cutting sampling cost in agentic RL.

**Link**: https://arxiv.org/abs/2608.19842

### 6. Rule-Compliant Visual Spatial Planning for Multimodal Large Language Models

**Abstract**: Visual spatial planning under explicit rule constraints (RuleMaze) for MLLMs.

**Link**: https://arxiv.org/abs/2608.20237

### 7. ID-VTG: Image-Disambiguated Video Temporal Grounding

**Abstract**: Image-plus-text disambiguated video temporal grounding — using both modalities to resolve timing ambiguities.

**Link**: https://arxiv.org/abs/2608.20127

### 8. 4DAnyone: Create Anyone in 4D from a Casual Monocular Video

**Abstract**: 4D digital-human generation from a single monocular video with O(1) context compression.

**Link**: https://arxiv.org/abs/2608.20335

## 2. Hot GitHub Open Source

- **ruvnet/ruflo** (68,940★) — orchestratable meta-harness for multi-agent swarms
- **modular/modular** — modular's agent runtime
- **missuo/herdrm** — cross-device terminal control for parallel coding agents
- **x64dbg-mcp-server** — debugger wired into MCP
- **addyosmani/agent-skills** (80k★, Trending #2) — engineering experience as reusable skills
- **obra/superpowers**, **pbakaus/impeccable**, **book-to-skill**, **spec-kit**, **headroom** (context compression, 60–95% token cut)

## 3. Selected Industry News

- **DeepSeek open-sources deepseek-harness** ("everything is a plugin", 130k★ in 4 days)
- **OpenAI open-sources the agent runtime behind Codex** (Apache-2.0): "preserve reasoning traces + context compression" alone lifted GPT-5.6 Sol on ARC-AGI-3 from 13.3% to 38.3% with 1/6 the output tokens
- **NVIDIA AVO**: search strategy + persistent memory + stagnation monitoring took the same Claude Opus 5 from ~30% to a perfect score on ARC-AGI-3 public set (25/25, 100 RHAE), and produced GPU kernels up to 3.5% faster than cuDNN for 7 straight days
- **Anthropic GA**: Computer Use / Browser Use / Skills API / Files API all general availability
- **Pricing**: DeepSeek weekend valley pricing from 08-23; OpenAI GPT-5.6 Sol API >20% cut (output $30→$20, −33%); Gemini 3.7 Flash ~half price
- **Model releases**: DeepSeek V3.1 (hybrid reasoning, 128K, Anthropic-API compatible), V4 Pro official (Terminal Bench 87.9); SenseNova U1.5 Lite; GLM-5.3 open weights 08-28; Ant Ling-3.0 & ByteDance Seed-OSS-36B open-sourced same day; Xiaohongshu dots3-note preview (MoE 280B/16B active, 512K, Apache-2.0)
- **Security**: OpenAI admits underestimating model offensive capability (HF incident, chained zero-days + leaked credentials), pausing large-scale training for two weeks; Anthropic archives frontier model "Model 2" over alignment risk; ChainDrop npm worm pollutes 444 packages; OpenAI reverses to lobby for SB53 in California (training-time monitoring + full-cycle cybersecurity); China's mandatory "Agent Application Security Basic Requirements" national standard project was initiated
