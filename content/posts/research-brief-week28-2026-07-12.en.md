---
title: "AI Research Weekly — 2026 Week 28"
date: 2026-07-12T21:00:00+08:00
draft: false
tags: ["AI", "LLM", "Agent", "Computer Vision", "Security", "Weekly Summary", "Trend Forecast"]
categories: ["Research Brief"]
subtype: "weekly"
description: "hackcv weekly AI research review — Week 28 (2026-07-06 ~ 07-12): model releases, AI security, agent tooling, embodied AI, compute, AI for Science, regulation."
---

# AI Research Weekly — 2026 Week 28

> Review period: 2026-07-06 (Mon) ~ 2026-07-12 (Sun) ｜ Updated every Sunday

## 1. Overview

- **Issues published**: 7 (07-06 ~ 07-12, one per day, no gaps)
- **Total items**: 56 papers + 56 GitHub projects + 56 industry news items (incl. ~4 cross-issue paper duplicates, ~17 project duplicates, ~22 news duplicates)
- **Total token usage**: ~320,181 (six measured days total 268,181; 07-12 was an estimate ~52,000, flagged in the source)
- **Publishing cadence**: normal, 7/7 days, ~44k tokens per issue on average

## 2. Weekly Theme Summary

### 1. Model releases (strongest thread of the week)
- **OpenAI GPT-5.6 family (Sol/Terra/Luna) + ChatGPT Work agent**: tracked across multiple issues after the 07-08 launch — Ultra multi-agent coordination, Luna trained autonomously by Sol (AI self-evolution), first ARC-AGI-3 pass, etc.
- **Google Gemma 4**: 31B on-device multimodal, fully open under Apache 2.0, drops heavy vision/audio encoders — a qualitative shift in on-device model capability.
- **Zhipu GLM 5.2**: first open-weight model reaching GPT/Claude parity, at ~1/20 of closed-source cost; hit multiple issues and pressured closed-source pricing.
- **Others**: Meituan LongCat-2.0 (1.6T params, domestic compute closed loop), SpaceXAI Grok 4.5, Meta Muse Spark 1.1, (rumored) Gemini 3.5 Pro.

### 2. AI security offense/defense (second thread, papers + projects + news all week)
- **Attack side**: world's first fully autonomous AI agent ransomware JadePuffer (07-08/09), GitLost (malicious issues luring agents into leaking private code, 07-10), Claude Code security backdoor leading to an Alibaba-wide ban (07-06/10).
- **Defense/red-team side**: open-source red-team tools `strix`/`T3MP3ST`/`pentagi` charted repeatedly; papers on distributed attacks in persistent-state AI control, Overthinking-based model-secret extraction, and Prismata defending cross-site prompt injection.
- **Policy side**: US CISA adopted Anthropic's Mythos for government code review (07-09).
- Security is hackcv's core DNA; supply this week was rich and high quality.

### 3. Agent tooling & orchestration (dominant GitHub category)
- Frameworks/runtimes: OpenClaw (355k stars, #1 all-time on GitHub), vercel/eve, stablyai/orca (parallel runtime), agency-agents (virtual company suite).
- **Memory mechanisms became a new hotspot**: `cognee` (knowledge-graph memory), `TencentDB-Agent-Memory` (four-layer semantic pyramid), papers "Remember When It Matters" and "Proactive Memory Agent".
- **Skill standardization**: `addyosmani/agent-skills`, `agentskills/agentskills`, `mattpocock/skills`, `obra/superpowers`.
- Sandbox & infrastructure: Tencent/CubeSandbox (hardware-level isolation), OmniRoute (model-routing gateway), OfficeCLI.

### 4. Embodied intelligence
- Unitree's STAR Market IPO ("first embodied-intelligence stock", 07-06); Ant `LingBot-VLA 2.0` embodied foundation model (07-10); iFlytek `Embodied-Omni` (07-11); papers Ego-Human, FSD-VLN (drones), INTENT (vehicle intent).

### 5. Compute & chips
- Domestic AI chip share passed 52% (07-06); DeepSeek secretly developing its own inference chip (07-08/09); Samsung Q2 profit +19x (07-07~09); H100 rental prices +40% (07-08); Sugon 8000 100k-GPU cluster (07-11); Meta Iris custom chip (07-11); on-device chip maker Lingsi raised (07-10); PKU phase-change memristor brain-inspired chip (07-06).

### 6. AI for Science
- Alibaba DAMO discovered 4 superconducting materials (07-06); VASP Agent first-principles computation (07-09); Physics-Audited Agentic Discovery (07-09); SpaCellAgent cell trajectories (07-10); "Does AI Understand Imaging" computational imaging benchmark (07-10); VaseMuseum cultural-relics agent (07-09).

### 7. Regulation
- The Interim Measures for AI Anthropomorphic Interaction Services took effect; ByteDance/Alibaba/Tencent collectively took public agents offline (07-06/07); four ministries issued "AI + Human Resources & Social Security" (07-08); SSE STAR Market listing guidance for AI-model companies (07-09); OpenAI equity sale/confidential IPO drew regulatory attention (07-06/08/09); Anthropic's enterprise API share first surpassed OpenAI (compliance reputation converting to procurement, 07-12).

## 3. Highlights & Directions to Watch

1. **AI self-evolution went from narrative to fact**: GPT-5.6's Luna was trained autonomously by Sol (finding GPUs, configuring, writing scripts, verifying — no human in the loop) plus NousResearch/hermes-agent open-source self-evolving agents — the labor structure of model iteration is being rewritten.
2. **Security entered an "AI vs AI" live-fire phase**: JadePuffer fully autonomous ransomware, GitLost prompt-injection leaks, Claude Code backdoor — attacks are industrialized, while defense (`strix`/`T3MP3ST`/`pentagi`) matures in parallel; the best arena for hackcv's security DNA.
3. **On-device multimodal quality leap**: Gemma 4 31B drops heavy encoders and runs offline on laptops/phones; with `pocket-tts` on-device TTS, the on-device agent loop is forming.
4. **Agent memory exploded as a topic**: cognee, TencentDB-Agent-Memory and the paper "Remember When It Matters" all in the same week — long-horizon reliability is becoming the core gate for agent deployment.
5. **Domestic compute closed-loop milestone**: Meituan LongCat-2.0 (trillion-parameter model on a 50k-GPU domestic cluster), Sugon 8000 100k-GPU cluster — training-side self-sufficiency.
6. **Fine-grained visual reasoning**: P2R (Perceive-to-Reason), HIVE (post-hallucination reasoning), DeltaV (differential vision updates) and other CV papers clustered, aligning with hackcv's computer-vision DNA.

## 4. Trend Predictions (next 2-4 weeks, derived from real signals)

1. **AI self-evolution moves from selling point to governance issue**: Luna trained by Sol with zero human involvement, plus open-source self-evolving agents — predict dense open-source follow-ups of self-evolving agent frameworks, while "who supervises self-evolving models" and "does self-evolution need registration" become new governance debate points.
2. **Agent security enters routine "AI vs AI" red-blue competition**: JadePuffer, GitLost and the Claude Code backdoor prove industrialized attacks; defenses mature in parallel. Predict: enterprise agent deployments will make "red-team credentials" mandatory, and regulators may draft provisions targeting autonomous agent attacks.
3. **On-device multimodal + on-device TTS ignite "personal local agents"**: Gemma 4 31B offline on laptops/phones plus `pocket-tts`. Predict: privacy-first on-device agents become a differentiation track, with phones/laptops as the main carriers and "on-device capability" a new model-launch selling point.
4. **Agent memory standardizes as a pluggable component**: cognee, TencentDB-Agent-Memory and "Remember When It Matters" all at once. Predict: memory becomes a standard "pluggable memory layer" like vector DBs, plus dedicated memory-reliability benchmarks.
5. **Training-side domestic compute self-sufficiency accelerates**: Meituan LongCat-2.0, Sugon 8000, DeepSeek custom inference chip, domestic share past 52%. Predict: training-side domestic closed loops keep breaking through in H2; a DeepSeek custom chip would significantly restructure inference cost.
6. **"Compliance as competitiveness" pays off in procurement**: anthropomorphic-interaction rules, SSE AI-listing guidance, Anthropic enterprise share surpassing OpenAI. Predict: compliance becomes a core gate in model and enterprise procurement; tighter domestic rules force agent products toward de-anthropomorphization/registration.

## Appendix: High-Frequency Keywords (deduplicated by topic)

- **Model releases**: GPT-5.6 / ChatGPT Work / Gemma 4 / GLM 5.2 / LongCat-2.0 / Grok 4.5 / Muse Spark 1.1 / (rumor) Gemini 3.5 Pro
- **AI security**: JadePuffer autonomous ransomware / GitLost prompt injection / Claude Code backdoor / strix / T3MP3ST / pentagi / Prismata / CISA×Mythos
- **Custom chips**: DeepSeek inference chip / Meta Iris / Samsung HBM / Sugon 8000 / Lingsi on-device chip / PKU memristor
- **Domestic compute**: 52% share / H100 rental +40% / LongCat-2.0 trillion-param closed loop
- **Agent orchestration**: OpenClaw / orca / agency-agents / WebSwarm / vercel/eve
- **Agent memory**: cognee / TencentDB-Agent-Memory / Remember When / Proactive Memory
- **Skill standardization**: agent-skills / agentskills / skills / superpowers / taste-skill
- **Embodied AI**: Unitree IPO / LingBot-VLA 2.0 / Embodied-Omni / Ego-Human / FSD-VLN
- **AI for Science**: superconducting discovery / VASP Agent / SpaCellAgent / computational imaging / cultural-relics agent
- **On-device AI**: Gemma 4 / pocket-tts / on-device inference chips
- **Regulation & compliance**: anthropomorphic-interaction rules / AI + HRSS / SSE listing guidance / Anthropic share overtake
- **CV depth**: TopoGPT / Perceive-to-Reason / HIVE / DeltaV / ProLaViT / AlayaWorld

---
