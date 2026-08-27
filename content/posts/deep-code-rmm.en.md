---
title: "Algorithm Deep-Dive: RMM — TopK Column-Norm Slicing: Formulas, 1B–70B Results, and the Attention/MLP Asymmetry"
author: "hackcv"
date: 2026-08-23
section: "deep"
subtype: "code"
tags: ["AI", "Inference Optimization", "Matrix Multiplication", "RMM", "Algorithm Deep-Dive"]
categories: ["Research Brief"]
description: "RMM full breakdown: contraction-dim TopK column-norm selection, minimax optimality proof, retention-ratio knob; 8 benchmarks × 4 retention levels, attention vs MLP asymmetry data, A100 end-to-end 1.40× speedup."
---

> **One-line takeaway**: RMM selects **TopK slices by column L2 norm along the contraction dimension** of matrix multiplications and computes only what's kept — no training, no weight changes, one retention-ratio knob for a predictable accuracy-efficiency trade-off. Measured: **70B is nearly lossless at 80% retention**, Llama3.1 8B gets **1.40× end-to-end speedup** on long sequences, 4096-token runs avoid **OOM** on 70B; mechanistically, **attention is far more reducible than MLP** (Q projection drops only 2pp at RR=0.5 vs 29.5pp for whole-MLP).

## Background & Motivation

Transformer inference cost is dominated by high-dimensional matmuls (QK^T, PV, three FFN projections), but much of it is redundant: attention scores are sparse, FFN activations are highly sparse in high dimensions. Existing approaches face a dilemma:

| Route | Representative | Flaw |
|---|---|---|
| Trained sparsity | SparseGPT/Wanda/SliceGPT | Changes weights, costly |
| Static pruning | Magnitude et al. | Input-independent; degrades sharply across distributions |

RMM fills the gap: **no weight changes + input-adaptive dynamic pruning**.

## Core Approach (Formula Level)

### Contraction-Dimension TopK Selection

For matmul `Y = A·B` (A∈ℝ^{n×d} activations, B∈ℝ^{d×m}), select index set ℐ ⊆ [d] (|ℐ| = ⌈ρd⌉) along the contraction dim:

```
RMM_ρ(A,B) = A[:,ℐ] · B[ℐ,:]
```

**Importance score = activation column L2 norm**: `s_j = ||A[:,j]||₂`, take TopK-largest ⌈ρd⌉.

**Properties**:
- Deterministic for a given input; input-adaptive per layer/head/token
- **Minimax optimal** (Theorem 1): TopK by column norm minimizes worst-case approximation error over any B under the retention budget
- Error bound: `||AB − A[:,ℐ]B[ℐ,:]||_F ≤ Σ_{j∉ℐ} ||A[:,j]||₂·||B[j,:]||₂`
- Complexity: O(n·ρd·m) vs dense O(n·d·m); column-norm O(n·d) + TopK overhead is small

**Component mapping**: QK^T selects along head feature dim (score = Q column norm), PV optionally along token positions, MLP/linear projections along activation hidden dim; under GQA, selection is done on Q per head and K/V gather the corresponding dims.

### The retention-ratio (ρ) Knob

ρ∈(0,1] directly controls ⌈ρd⌉ retained dims — a smooth, predictable trade-off. **Component-differentiated**: attention can be aggressive (RR as low as 0.5), MLP must be conservative and split by projection type. With no labeled data, scan ~100 unlabeled samples for consistency (Llama-3.1-8B at RR=0.7: 87/100 Wikipedia paragraphs **sequence-identical** to the dense model).

## Results

### Scaling law (8 tasks × RR 0.9→0.5)

| Model | RR=0.8 | RR=0.5 |
|---|---|---|
| Llama3.1 **70B** | near-full (MMLU 75.0→72.6) | still usable (GSM8K 53.7→19.9 but most tasks gentle) |
| Qwen3 32B | almost lossless (MMLU 80.8→78.6) | gentle degradation |
| Llama3.1 8B | mild drop | GSM8K 26.2→5.9 noticeable |
| Qwen3.1 7B | clear drop | GSM8K 39.9→1.7 collapses |

**Larger models tolerate more reduction**; small models show an inflection around RR=0.7 (WikiText ppl: Llama3.2-1B 20.04→31.29 at RR=0.7).

### vs Static pruning (RR=0.5, Llama3.1 8B, avg 5 QA)

| Method | Avg |
|---|---|
| Full model | 69.8 |
| **RMM** | **59.8** |
| SparseGPT | 56.1 |
| Wanda | 52.7 |
| Magnitude | 39.3 |
| SliceGPT | 37.0 |

### Attention vs MLP: structural asymmetry (Table 16, 8B, avg 5 QA)

| Target | RR=0.9 | RR=0.7 | RR=0.5 |
|---|---|---|---|
| **Q projection** | 69.60 | 70.01 | **67.80** (nearly flat) |
| QKV projections | 68.92 | 67.35 | 59.79 |
| Attention-internal (QK^T+PV) | 69.45 | 66.98 | 59.56 |
| **Whole MLP** | 63.06 | 55.93 | **40.28** (collapses) |
| MLP Up | 65.69 | 59.88 | 52.44 |
| MLP Down | 67.43 | 65.75 | 61.36 |

Supplementary (ARC-Easy RR=0.7 normalized): attention drops 3.52pt (retained energy 89.69%), MLP Up 16.32 (82.24%), MLP Down 3.51 (99.02%), whole MLP 18.78 (87.85%) — **Down is most robust, Up most sensitive, errors accumulate across projections**.

### Long context (Ruler, RR=0.5 still flat)

CWE 5K/15K/30K: 98.0/94.0/28.9 vs baseline 98.2/94.0/29.6 — **pruning does not amplify long-context degradation**.

### A100 measurements (ρ=0.8, batch=1)

| Seq len | QK^T | AV | E2E (8B) | E2E (70B) |
|---|---|---|---|---|
| 1024 | 1.36× | 1.67× | 1.05× | 1.03× |
| 2048 | 1.29× | 1.81× | **1.27×** | **1.41×** |
| 4096 | 1.56× | 1.89× | **1.40×** | **OOM→runs** |

**Longer sequences, bigger gains** (selection overhead dominates at short lengths); 70B goes from OOM to runnable at 4096 — memory savings and latency wins together.

### Compatibility & generalization

- **Orthogonal to INT8**: INT8 + RMM (attention RR=0.8) COPA 81.40→77.40 — lower precision × fewer FLOPs stack
- **VLM generalization**: Qwen2.5-VL-7B nearly lossless at RR=0.8 (POPE 83.7→82.0); InternVL3-8B flat at 92.33 even at RR=0.5
- **vs TEAL (activation sparsity)**: TEAL only prunes projection inputs, cannot shrink QK^T/PV internal matmuls; RMM's matrix-product view covers a broader operation space

## Engineering Notes

- **Integration**: wrap attention/FFN operators — prototype in PyTorch; production needs custom kernels to realize actual speedups
- **Config**: aggressive attention (RR 0.5–0.7), conservative MLP (0.8+, Down can be lower); tune prefill (prune FFN) and decode (prune attention) separately
- **Gotchas**: short sequences gain little; strong-reasoning tasks like GSM8K are most sensitive (fastest to degrade) — be careful with math workloads
- **Validation**: scan ~100 unlabeled samples for consistency to pick ρ quickly, no annotation needed

## Scope & Trade-offs

- **Fits**: long context, batch generation, lowering cost on deployed models, memory-constrained 4096+ runs; stacks with quantization
- **Doesn't fit**: short-sequence high-concurrency small batches (gains washed out by GEMM libraries); strict-accuracy workloads
- **Trade-offs**: vs static sparsity (dynamic robustness but needs kernels); vs quantization (orthogonal, stackable); vs activation sparsity TEAL (broader matmul coverage)

## Reproduction Notes

- arXiv: 2608.13426 (8-13, 24 pages); authors Zixuan Lan et al.; no repo noted
- Path: implement the column-norm TopK slicing operator → run the RR curve on an 8B model → long-sequence A100 benchmark
- Per-component RR (attention vs MLP) is the key engineering decision
