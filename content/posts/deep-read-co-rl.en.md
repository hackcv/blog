---
title: "Paper Review: Co-RL — Peer Rewards Replace RLHF: Formulas, Mechanism, and 7+4 Benchmark Results"
author: "hackcv"
date: 2026-08-23
section: "deep"
subtype: "paper"
tags: ["AI", "Reinforcement Learning", "Multi-Agent", "Co-RL", "Paper Review"]
categories: ["Research Brief"]
description: "Co-RL full breakdown: peer-reward pseudo-label formulas, ring-topology majority voting, three diversity dimensions, GRPO integration; Qwen2.5-3B +8.6% avg across 7 text benchmarks, VLM +7.2% across 4, label-free parity with supervised methods, code open-sourced."
---

> **One-line takeaway**: Co-RL makes parameter-independent models judge each other — rewards come from **majority-voted pseudo-labels of peer answers**, not one's own. Cohort diversity (heterogeneous families/sizes/sample rephrasings) breaks the correlated-error feedback loop of self-rewarding. Measured: Qwen2.5-3B averages **+8.6%** across 7 text benchmarks (49.3 vs 40.7 base), 5 VLMs average **+2.3–7.2%**, matching or beating supervised methods **with zero ground-truth labels**.

## The Problem

### The "Supervision Dependence" Dilemma of Reasoning RL

RL's strongest gains for LLM/VLM reasoning rely on **verifiable rewards** (code tests, math answers) — but such annotations are costly and deplete as reasoning capability exceeds what humans can reliably evaluate.

### The Mechanistic Flaws of Self-Rewarding

Letting a model grade itself is the common shortcut, but the paper identifies three failure paths:

1. **Correlated-error loop**: feedback from oneself (or same-source models) reinforces the same mistakes
2. **Response homogenization**: a single reward signal collapses the policy
3. **Training collapse**: diversity exhaustion → loss oscillation/divergence

**Core insight**: the problem is not "unsupervised" but "**feedback correlated with the learner**" — cut the correlation and the unsupervised signal becomes clean.

## Method Breakdown (Formula Level)

### Cross-Agent Supervision (Peer Rewards)

**Pseudo-label construction** (ring topology; agent n is supervised by peer n−1):

```
â₋ₙ(x) ∈ argmax_b Σⱼ₌₁ᴷ 𝟙[aₙ₋₁ʲ = b]      # majority vote over K sampled answers
```

**Reward assignment** (hard 0/1):

```
rₙᵏ = 𝟙[aₙᵏ = â₋ₙ(x)]                     # 1 iff matches peer pseudo-label
```

**GRPO integration** (in-group relative advantage):

```
Âₙᵏ = (rₙᵏ − mean{rₙʲ}) / std{rₙʲ}        # normalized within rollout group
```

Key point: **an agent never contributes to its own supervision target** — the essential difference from self-rewarding.

### Three Dimensions of Cohort Diversity

| Dimension | Implementation | Mechanism |
|---|---|---|
| **Decoupled optimization** | Independent params/optimizers, no shared gradients, interact only at reward time | Independence itself is a diversity source |
| **Cross-family & size** | Pair Qwen×Llama (different tokenizers/pretraining), 3B×1.7B mixes | Different inductive biases → orthogonal error patterns |
| **Input formation** | DeepSeek-V3 rephrases MATH problems; agents train on different phrasings | Breaks phrasing-correlated errors |

**Quantified evidence** (error-decoupling analysis): cross-family pairing (Qwen2.5-3B × Llama-3.2-3B) Cohen's κ=0.38, complementarity c=31.2%; same-family (×Qwen3-1.7B) κ=0.52, c=24.2% — **cross-family errors overlap far less**, the root reason peer grading works.

### Training Loop

Per step: sample prompt batch → all agents **parallel-sample** K responses → build pseudo-labels/rewards from peers → **synchronous** GRPO update of all policies. Symmetric design: every agent is both learner and supervisor.

## Results

**Text (Table 1, 3B-class, avg of 7 benchmarks)**:

| Model | Base | GT-Reward (supervised) | Best self-reward TTRL | **Co-RL** |
|---|---|---|---|---|
| Qwen2.5-3B | 40.7 | 47.4 | 47.3 | **49.3** (+8.6%) |
| Llama-3.2-3B | 38.7 | 43.0 | 43.1 | **43.9** (+5.2%) |

7 benchmarks = GSM8K/MATH-500/AMC/HumanEval/GPQA/MBPP/LiveCodeBench. Co-RL gains 3.0–8.6% on average, **0.8–2.0% above the strongest self-reward baseline**.

**Multimodal (Table 4, 2B–12B VLMs, MathVision/MathVerse/MathVista/We-Math)**:

| Model | Base | TTRL | **Co-RL** |
|---|---|---|---|
| Qwen2.5-VL-3B | 37.24 | 42.54 | **43.89** (+6.65%) |
| InternVL-3.5-2B | 43.11 | 45.04 | **45.40** |

On larger models (7B–12B) Co-RL consistently beats TTRL; **on Gemma-3-12B it exceeds GT-Reward (supervised)**.

**Key ablations**:

- **Training stability**: Co-RL keeps reward variance/length stable throughout; TTRL shows reward collapse / length degradation / divergence
- **Budget-fair comparison**: two individually TTRL-trained models + inference ensemble vs Co-RL's two agents — Co-RL still wins, proving gains come from **cross-supervision**, not ensembling/compute
- **Three-agent scaling**: Qwen2.5-3B + Llama-3.2-3B + Qwen3-1.7B jointly trained — all three improve +7.8%/+6.0%/+8.2%, averaging parity with GT-Reward
- **Multi-agent baselines** (CoMAS setting): Co-RL 62.97, well ahead of MAPoRL(58.22)/TTRL(58.18)/CoMAS(58.94), with half the agents and no external judge

## Limitations & Commentary

- **L1**: cohort size = training cost ×N; diversity hyperparameters (model mix, rephrase ratio) need tuning
- **L2**: emergent reasoning is implicit behavior — no quality ceiling guarantee, no interpretability
- **Lineage**: self-rewarding (self-grades) → self-play (self-opponent) → **Co-RL (heterogeneous peer grading)** — in the "no external supervision" spectrum, it trades diversity for signal quality, complementing verifier-based routes
- **For practitioners**: when doing reasoning RL without labels, Co-RL is the most promising unsupervised route; infra teams can borrow the "cohort architecture + diversity scheduling" design pattern directly

## Reproduction Notes

- arXiv: 2608.17253 (v2); code open-sourced at **github.com/DrStranded/Co-RL**
- Bar: multi-model parallel training (start with two 3B models to validate the mechanism); temperature/sampling K per paper; ring-topology pseudo-labels via majority vote
- Start with a *cross-family* model pair (biggest error-decoupling gains), then scale size
