---
title: "Paper Review: SemComp-Bench — Video Generation Evaluation Moves from 'Looks Right' to 'Task Done'"
author: "hackcv"
date: 2026-08-23
section: "deep"
subtype: "paper"
tags: ["AI", "Video Generation", "Benchmark", "SemComp-Bench", "Paper Review"]
categories: ["Research Brief"]
description: "The hottest paper on HF this week (153 upvotes): Semantic Task Completion video generation + the six-domain SemComp-Data + VLM-driven OA/GR dual-metric protocol, with full benchmark tables."
---

> **One-line takeaway**: SemComp-Bench redefines video generation as **outcome-oriented semantic task completion** — success = achieving the intended outcome × semantic grounding against a reference image — and ships a six-domain dataset with a VLM-based auto-evaluation protocol (OA/GR dual scores). Measured across 7 mainstream models: **the best OA is only 37.8%**, I2V consistently beats T2V, and within-scene spatiotemporal consistency is the universal bottleneck — the "quality ceiling, task completion is the next frontier" claim is now backed by data.

## The Problem

**Background**: Video generation evaluation has long been dominated by "quality" metrics — FVD, CLIP similarity, human preference. They measure "how realistic the video looks," and are **completely blind to task goals**.

**The flaw**: For a request like "move the coffee cup from the desk to the windowsill," a model that generates a gorgeous close-up of the cup may still score high FVD — because FVD compares frame distributions, not "did the cup move?" As controllable video generation goes mainstream, "was the goal achieved" becomes the only acceptance criterion that matters, and legacy metrics fail.

## Method Breakdown

### Task Redefinition: Semantic Task Completion

Success = **Outcome Achievement** × **Semantic Grounding**. Evaluation looks only at the final result — no requirement for a complete intermediate step sequence, and no traditional appearance consistency with the reference image.

### Data: SemComp-Data (Six Domains, 21 Subcategories)

Sampled ~20K videos from Koala-36M → **1,273 instances**. Each instance = `(reference frame, instruction pair {brief + detailed}, outcome-centric clip)`, with the reference frame and clip from the *same* source video (guaranteeing real feasibility). Four-stage curation:

| Stage | What it does |
|---|---|
| **Candidate Filtering** | 45 keywords (news/movie/entertainment groups) drop narration-dependent videos; VLM classifies into six domains, discards low-evidence items as *Uncertain* |
| **State Mining** | Frame-level timestamp localization (State Grounding) + QA check: VLM picks "which frame is the outcome"; mismatches are conservatively dropped |
| **Video Extension** | Panda-70M shot detection + same-scene merging, anchored at the outcome timestamp, extended to 3–4s (mean 4.03s) |
| **Instruction Structuring** | Brief instruction ≤30 words (`verb + subject + preposition + outcome state`); detailed instruction adds alignment type from a 17-item attribute vocabulary (object_category / person_identity / spatial_relation / pose …) |

Six domains: Food & Cooking, Beauty & Fashion, Sports & Fitness, Crafts & DIY, Gardening & Pets, Arts & Precision.

### Evaluation Protocol: VLM Answers Structured Binary Questions

Generated videos are sampled into **27 frames**; each video is scored by **3 independent VLM calls** (Doubao-Seed-1.8), averaged.

**OA dimension** (4 yes/no questions, **conjunctive** — all must pass):

```
Aᵢ = a_or × a_sg × a_gec × a_gvc ∈ {0,1}     OA Score = (1/N)ΣAᵢ
```

| Question | Criterion |
|---|---|
| a_or Outcome Realization | Does the video clearly reach the instructed completion state at coarse semantics? |
| a_sg Semantic Grounding | Does the result preserve/modify task-relevant entities per the reference-instruction pair? |
| a_gec Entity Consistency | Key entities stay identifiable — no unexplained disappearance/replacement/drift? (reversed, no → 1) |
| a_gvc Global Continuity | No abrupt global switch in scene/view/layout/background? (reversed, no → 1) |

**GR dimension** (5 yes/no questions, **arithmetic mean**):

```
Gᵢ = (g_pp + g_vc + g_afr + g_wsc + g_ti)/5     GR Score = (1/N)ΣGᵢ
```

Physical plausibility / visual clarity / artifact-free rendering / within-scene spatiotemporal coherence / text & interface integrity.

## Results (SemComp-Core: 60 stratified instances)

**Table 1: OA Score (detailed instruction, I2V)**

| Model | A_or | A_sg | A_gec | A_gvc | **OA** |
|---|---|---|---|---|---|
| **HY†-1.5-720P-I2V** | 0.878 | 0.706 | 0.583 | 0.794 | **37.8%** |
| Wan2.2-I2V-A14B | 0.800 | 0.528 | 0.628 | 0.789 | 28.3% |
| Wan2.2-TI2V-5B | 0.589 | 0.400 | 0.689 | 0.922 | 23.3% |
| SkyReels-V2-14B | 0.733 | 0.489 | 0.522 | 0.772 | 22.8% |
| Seedance 2.0 | 0.839 | 0.744 | 0.444 | 0.594 | 20.0% |
| CogVideoX1.5-5B | 0.550 | 0.389 | 0.506 | 0.744 | 14.4% |
| Phantom-1.3B | 0.539 | 0.356 | 0.322 | 0.511 | 3.9% |

(†HY = HunyuanVideo. GR leaderboard: Seedance 2.0 tops at 91.8%, Wan2.2-A14B 89.0%.)

**Key findings**:

1. **Best OA is only 37.8%** — achieving the outcome while preserving reference grounding is genuinely hard today
2. **I2V beats T2V across all three model families** — gains come from grounding/entity consistency/global continuity; outcome realization rates are comparable
3. **Instruction specificity trade-off**: detailed instructions give higher OA but are harder to generate; brief ones are more coherent but far lower task completion (CogVideoX T2V-brief OA = 0.6%)
4. **Within-scene spatiotemporal coherence is the global bottleneck**: all models G_wsc ∈ 0.328–0.739
5. **GR and OA do not correspond**: Seedance tops GR (91.8%) but scores only 20% OA — "renders steadily" and "gets it done" are different things; both metrics are needed

(3-run std dev: OA 0.96–4.41pp, GR 1.35–7.20pp; Seedance OA most volatile.)

## Limitations & Commentary

- **L1**: The VLM judge is a double-edged sword — it may be insensitive to physical plausibility / precise spatial relations; manual spot-checks are needed (paper reports per-question std anomalies up to 15.84pp on G_wsc)
- **L2**: Six domains skew toward "everyday operations"; real productivity task space is much larger
- **For practitioners**: the evaluation mindset transfers directly — any pipeline whose output gets *used* should move acceptance from "similarity" to "goal achievement rate." Rollout path: small task set + VLM judge (Doubao/Claude/GPT), replace human acceptance first, then scale

## Reproduction Notes

- arXiv: 2608.17426; dataset + eval scripts released with the paper
- Eval cost: 3 VLM calls per video + 27-frame sampling — budget-friendly
- Metric gotcha: OA must use the **conjunctive** formula (all 4 must pass); GR uses arithmetic mean — different semantics, don't mix
