---
title: "Algorithm Deep-Dive: SkillForge — Synthesize Issues in 4 Steps, Distill a Dual-Layer Skill Library, +5.8% on SWE-bench"
author: "hackcv"
date: 2026-08-23
section: "deep"
subtype: "code"
tags: ["AI", "Agent", "Skill Distillation", "SkillForge", "Algorithm Deep-Dive"]
categories: ["Research Brief"]
description: "SkillForge full breakdown: strict-mask 4-step issue synthesis, dual-layer entity-grounded skills (diagnostic + intervention), BM25+JIT two-phase retrieval; SWE-bench Verified 72.2% (+5.8%), Pro 34.1% (+5.8%)."
---

> **One-line takeaway**: SkillForge doesn't wait for real issues — it **synthesizes project-specific issues by re-implementing test-covered core functionality**, distills **entity-anchored skills** (diagnostic + intervention layers) while solving them, and injects skills on-demand at interaction time. SWE-bench Verified: DeepSeek-V3.2 hits **72.2%** (baseline 66.4%, +5.8%), GPT-5-mini **60.6%** (+5.6%) — and ablation shows both knowledge layers are necessary.

## Background & Motivation

### The Project-Knowledge Bottleneck

LLM coding agents fail on specific repos because they lack project knowledge — module layout, coding style, implicit constraints. Existing self-evolving methods each have a hard flaw:

| Route | Approach | Flaw |
|---|---|---|
| History learning (SWE-Exp/EvoCoder/MemGovern) | Distill from past fixes | **Depends on historical fix signals**; cold-start fails on new repos |
| Online exploration (SAGE/SWE-Debate/Live-SWE) | Learn on real issues | **Per-issue exploration cost** is high |

SkillForge takes a third path: **construct knowledge gaps from the repo's tests** — tests are the spec, with a built-in verifier.

## Core Approach (4-Step Synthesis → Dual-Layer Distillation → Two-Phase Retrieval)

### ① Issue Synthesis (Four Steps)

| Step | What it does |
|---|---|
| **1. Test-driven scope** | Coverage-instrumented execution of each **passing test** → execution trace → covered source files/line ranges, sliced into coherent segments |
| **2. Critical-segment selection** | LLM picks top-k key segments (test purpose + segment summary); **key differentiator**: can select multiple segments across components → synthesizes issues that expose **cross-component interactions** |
| **3. Code rewriting (strict-mask)** | **No original implementation given** — only surrounding lines, position/indent, and a high-level test goal; the LLM rewrites a plausible implementation preserving the API but simplifying logic → induces "general vs repo-specific knowledge" gaps (i.e., real developer mistakes) |
| **4. Instance assembly** | Rewrite breaks the test → buggy snapshot + buggy/reference patches → LLM turns failure evidence into a problem statement **without fix hints** → standard SWE-bench format |

577 synthetic issues were produced on SWE-bench Verified (time-isolated: rollback to pre-golden-patch snapshot).

### ② Dual-Layer Skill Library (Entity-Grounded)

**Global diagnostic skills M_ext** (3 fields, answering "where to look"):

| Field | Content |
|---|---|
| `purpose` | The entity's functional role in issue resolution (is it a debug entry point?) |
| `playbook` | Reusable, repeatedly-validated reasoning strategy (repo-specific, not generic advice) |
| `related_apis` | APIs frequently co-involved and why (repo interaction patterns) |

**Local intervention skills M_int** (answering "how to change"): distilled from **successful trajectories** (correct fix strategies) and **failed trajectories** (pitfalls exposed by diffing wrong patch vs reference patch), shaped as `{api_path, intervention_skills[]}`.

Skills are aligned to **real code entities** by parsing shell commands (grep/sed/cat) in trajectories + an AST-derived structural index — preventing the LLM from hallucinating nonexistent interfaces.

### ③ Two-Phase Retrieval (Context-Aware Injection)

- **Macro initialization**: new issue description → **BM25** top-5 from M_ext → prepended as project prior in the initial prompt
- **Micro JIT injection**: M_int is NOT injected all at once — the agent's **shell commands are monitored**; when an accessed file hits an M_int entry, the intervention hint is attached as an auxiliary observation in real time. Skills stay **strictly aligned with current code interaction**, avoiding semantic-retrieval ambiguity

## Results

**SWE-bench Verified (Table I, Pass@1)**:

| Method | DeepSeek-V3.2 | GPT-5-mini |
|---|---|---|
| **SkillForge** | **72.2%** | **60.6%** |
| Mini-SWE-Agent (baseline) | 66.4% | 55.0% |
| MemGovern (best history baseline) | 69.2% | 58.0% |
| SAGE / SWE-Debate (online baselines) | 67.2% / 68.2% | 56.0% / 56.4% |
| SkillForge w/ SWE-Smith (single-function rewrite) | 68.0% | 56.4% |
| SkillForge w/ LLM Summary | 68.7% | 54.4% |

**SWE-bench Pro** (731 instances, Python/JS/TS/Go): 34.1% / 51.7% (+5.8% / +4.1%).

**Ablations & hyperparameters**:

- **Component ablation**: removing M_ext ↓3.8%/↓3.0%; removing M_int ↓4.4%/↓3.4% — **both necessary; intervention skills matter slightly more**
- **Cross-LLM transfer**: GPT-5-mini using DeepSeck-distilled knowledge scores 55.0% < 60.6% self-distilled — **skills bind to the distilling model** (different coding priors → different exposed mismatches); clear diagonal pattern
- **Retrieval count**: k_r peaks at 5 (69.7%); full injection drops to 67.5% (low-ranked skills crowd the context window)
- **Rewrite count**: k_s peaks at 5 (multi-entity interactions expose richer knowledge), slight drop at 7
- **Cross-repo**: improvement on all 7 largest repos, zero regressions (DeepSeek up to +13.6% Sphinx, GPT-5-mini +15.6% scikit-learn), vs SWE-Exp regressing on 3 (Matplotlib −11.8%)

**Case study (Django #11206)**: formatting a tiny Decimal — `format(Decimal("1e-200"), ".", decimal_pos=2)` should yield "0.00" but returns "1.00e-200". Baseline agent used an exponent heuristic → FAIL_TO_PASS 0/2; SkillForge agent, guided by retrieved knowledge to preserve the existing formatting pipeline and reason about numeric equivalence with the repo's precision semantics → 2/2.

## Engineering Notes

- **Test quality = synthesis quality**: weak-assertion tests are bad synthesis material; add key tests first if a repo lacks them
- **Skill granularity**: entity-anchored (file/function level) beats generic experience — retrieval hit rate and injection alignment are the key levers
- **Rollout path**: validate the synthesis-distill loop on a medium repo (a few hundred files) first; reference action budget 250 steps, temperature 0
- **Cost note**: synthesis + distillation have extra inference overhead — best for high-frequency, homogeneous issue flows that amortize the skill library

## Scope & Trade-offs

- **Fits**: repos with test suites, cold-start on new repos, high-frequency homogeneous issues
- **Doesn't fit**: testless repos that won't add tests; one-off issue flows (library grows with low reuse)
- **Trade-offs**: vs history learning (no cold-start dependency but needs tests); vs online exploration (no per-issue cost but needs upfront synthesis budget); vs agent-skills (auto-generated + entity-anchored vs human-curated)

## Reproduction Notes

- arXiv: 2608.18933; code/data **github.com/cslsolow/SkillForge** (SJTU, Haibing Guan's group)
- Pipeline: coverage-instrumented test runs → strict-mask rewriting → failure-evidence-to-statement → Mini-SWE-Agent + BM25 retrieval + JIT injection
