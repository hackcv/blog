---
title: "Daily Research Brief 2026-08-22"
date: 2026-08-22T20:30:00+08:00
draft: false
tags: ["AI", "LLM", "Agent", "Computer Vision", "Audio-Video", "Engineering", "Daily Brief"]
categories: ["Research Brief"]
subtype: "daily"
description: "Daily research brief — AI / LLM / Agent / Computer Vision / Audio-Video / Engineering"
---

# Daily Research Brief 2026-08-22

📊 Token usage: estimated from retrieval and writing scale.

Covers the latest AI research, open source and industry moves, updated daily.

---

## Editor's Note

Today's main thread: "execution systems + skill ecosystems" formally take over the leverage point of AI competition, with long-context inference efficiency and agent memory as two technical undercurrents.

## 1. Latest arXiv Papers

### 1. EnvHarness: Awakening Static Worlds for Agent Learning

**Abstract**: A framework that turns static repositories into dynamic, evolving environments for agent RL — no domain-specific customization or expensive verifiers needed. Environments co-evolve with the policy during training.

**Link**: https://arxiv.org/abs/2608.19880

### 2. VLA Self-Demo Fine-Tuning

**Abstract**: Vision-language-action models fine-tuned on self-generated demonstrations for long-horizon manipulation (+11.6%), zero parameter updates to the base policy.

**Link**: https://arxiv.org/abs/2608.19490

### 3. FlashPrefill V2: Block-Sparse Prefill Attention

**Abstract**: Block-sparse prefill attention that cuts KV and attention compute for long-context prefill.

**Link**: https://arxiv.org/abs/2608.19758

### 4. SWE-bench Science

**Abstract**: A scientific-reproduction variant of SWE-bench evaluating agents on faithfully reproducing papers.

**Link**: https://arxiv.org/abs/2608.19799

### 5. PersonalBench: What Personalized LLMs Reveal About Author Identity

**Abstract**: A benchmark probing how personalized LLMs reflect author identity — and what that reveals about attribution.

**Link**: https://arxiv.org/abs/2608.19746

### 6. ReCache: Tool-Augmented Agent KV-Cache Reuse

**Abstract**: KV-cache reuse across tool-augmented agent steps — cutting redundant recomputation in long tool loops.

**Link**: https://arxiv.org/abs/2608.19662

### 7. Can Agent Memory Systems Track Evolving State?

**Abstract**: Evaluates agent memory systems on tracking evolving state (StateMemBench), showing current-state accuracy lifts from 0.205 to 0.363 on DeepSeek-V4-Flash (1.8×).

**Link**: https://arxiv.org/abs/2608.19652

### 8. Eureka: Task-Conditioned Meta-Agent Orchestration for Scientific Discovery

**Abstract**: Task-conditioned meta-agent orchestration for autonomous scientific discovery.

**Link**: https://arxiv.org/abs/2608.19047

## 2. Hot GitHub Open Source

- **DeepSeek deepseek-harness** — "everything is a plugin" harness, 130k★ in 4 days
- **rerelease of OpenAI Codex runtime** (Apache-2.0) — reasoning-trace retention + context compression lifted ARC-AGI-3 from 13.3% to 38.3% with 1/6 output tokens
- **Agent skills wave**: addyosmani/agent-skills (80k★), obra/superpowers, pbakaus/impeccable, book-to-skill, spec-kit, headroom (context compression, 60–95% token cut)

## 3. Selected Industry News

- **Anthropic**: Computer Use / Browser Use / Skills API / Files API all GA
- **NVIDIA AVO**: same Claude Opus 5 hit 25/25 (100 RHAE) on ARC-AGI-3 public set; 7 days of GPU kernels up to 3.5% faster than cuDNN
- **Pricing**: DeepSeek weekend valley pricing; OpenAI GPT-5.6 Sol −33% output price ($30→$20); Gemini 3.7 Flash ~half price
- **Security**: OpenAI pauses two weeks of large-scale training after HF breach; Anthropic archives "Model 2"; China's mandatory agent-security national standard moves forward
