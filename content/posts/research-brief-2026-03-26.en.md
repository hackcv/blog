---
title: "Daily Research Brief 2026-03-26"
date: 2026-03-26T20:30:00+08:00
draft: false
tags: ["AI", "LLM", "Agent", "Computer Vision", "Audio-Video", "Engineering", "Daily Brief"]
categories: ["Research Brief"]
subtype: "daily"
description: "Daily research brief — AI / LLM / Agent / Computer Vision / Audio-Video / Engineering"
---

# Daily Research Brief 2026-03-26

📊 Token usage: estimated from retrieval and writing scale.

Covers the latest AI research, open source and industry moves, updated daily.

---

## Editor's Note

Today's paper thread: unified policy optimization for reasoning-driven visual generation (UniGRPO), generalized unconstrained urban 3D occupancy (OccAny), foveation-inspired efficient image/video generation, on-demand vision interaction for VLLM efficiency, and zero-shot referring video object segmentation (AgentRVOS). GitHub trending is dominated by agent infrastructure — Karpathy's autoresearch, gstack, paperclip, CLI-Anything and Google Workspace CLI.

## 1. Latest arXiv Papers

1. **UniGRPO: Unified Policy Optimization for Reasoning-Driven Visual Generation** — unifies text and image (autoregressive + flow matching) joint generation with a unified policy optimization method, UniGRPO, for reasoning-driven visual content generation. — https://arxiv.org/abs/2603.23500

2. **OccAny: Generalized Unconstrained Urban 3D Occupancy** — breaks the dependence of 3D occupancy prediction on in-domain annotations and precise sensor calibration, proposing more generalizable unconstrained urban 3D occupancy prediction. — https://arxiv.org/abs/2603.23502

3. **Foveated Diffusion: Efficient Spatially Adaptive Image and Video Generation** — borrows the foveal vision mechanism of the human eye for spatially adaptive, efficient diffusion/flow-matching image and video generation, significantly cutting compute. — https://arxiv.org/abs/2603.23491

4. **Vision On Request: Enhanced VLLM Efficiency with Sparse Dynamic Vision-Language Interactions** — on-demand vision interaction replaces conventional visual token pruning, greatly improving LVLM inference efficiency while preserving information fidelity. — https://arxiv.org/abs/2603.23495

5. **AgentRVOS: Reasoning over Object Tracks for Zero-Shot Referring Video Object Segmentation** — uses MLLM reasoning over object tracks for zero-shot referring video object segmentation, no training required. — https://arxiv.org/abs/2603.23489

## 2. Hot GitHub Open Source

| Project | ⭐ | Notes |
|---------|-----|------|
| **karpathy/autoresearch** | ⭐ 55.6k | AI agent automated research framework — auto-runs nanochat training experiments on a single GPU; by Karpathy |
| **garrytan/gstack** | ⭐ 46.9k | Garry Tan's Claude Code config set: 15 tool personas (CEO, design, engineering manager, QA...), ready to use |
| **paperclipai/paperclip** | ⭐ 33.0k | Open-source zero-human company orchestration framework — agent-driven fully automated business processes |
| **HKUDS/CLI-Anything** | ⭐ 23.0k | Turns any software into an agent-native CLI — universal tool interface layer, by HKU |
| **googleworkspace/cli** | ⭐ 22.5k | Official Google Workspace CLI covering Drive/Gmail/Calendar/Sheets, with built-in AI agent skills |

## 3. HackerNews Top Posts

1. **[455pts/256c] A real time AI video agent with under 1 second of latency** — a real-time AI video conversation agent with <1s latency; a phenomenon on HN. — https://news.ycombinator.com/item?id=41710227

2. **[32pts/18c] Why are so many rolling out their own AI/LLM agent sandboxing solution?** — why developers build custom agent sandboxes and what a good-enough standard looks like.

## 4. Deep Reads

| Priority | Item | Link |
|----------|------|------|
| 🌟 | **UniGRPO** — unified policy optimization for visual generation reasoning | [arxiv](https://arxiv.org/abs/2603.23500) |
| 🌟 | **karpathy/autoresearch** — AI agent automated research | [GitHub](https://github.com/karpathy/autoresearch) |
| 💡 | **Foveated Diffusion** — foveation-based efficient generation | [arxiv](https://arxiv.org/abs/2603.23491) |

---
