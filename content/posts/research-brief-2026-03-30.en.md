---
title: "Daily Research Brief 2026-03-30"
date: 2026-03-30T20:30:00+08:00
draft: false
tags: ["AI", "LLM", "Agent", "Computer Vision", "Audio-Video", "Engineering", "Daily Brief"]
categories: ["Research Brief"]
subtype: "daily"
description: "Daily research brief — AI / LLM / Agent / Computer Vision / Audio-Video / Engineering"
---

# Daily Research Brief 2026-03-30

📊 Token usage: estimated from retrieval and writing scale.

Covers the latest AI research, open source and industry moves, updated daily.

---

## Editor's Note

Today's papers: autoregressive 3D Gaussian scene generation (GaussianGPT), world-consistent video generation via 4D latent reward (VGGRPO), a perception-centric video reasoning benchmark (PerceptionComp), geometry-aware spatial reasoning for VLMs (GeoSR), and zero-shot depth-from-defocus (FOSSA). GitHub trending stays agent-centric (AutoGPT, ollama, transformers, Langflow, Dify); HackerNews highlights agent behavior caching (Muscle-Mem), vision-native E2E testing (Magnitude), and a 48-hour agent red-team methodology.

## 1. Latest arXiv Papers

1. **GaussianGPT: Towards Autoregressive 3D Gaussian Scene Generation** — a Transformer-based autoregressive 3D Gaussian scene generation model producing 3D Gaussians via next-token prediction. Uses a sparse 3D convolutional autoencoder + vector quantization to compress Gaussian primitives; supports scene completion, outpainting and controllable sampling. Complementary to diffusion models; natively supports context-aware 3D generation. — https://arxiv.org/abs/2603.26661

2. **VGGRPO: Towards World-Consistent Video Generation with 4D Latent Reward** — applies GRPO in latent space for geometry-consistent video post-training. A Latent Geometry Model (LGM) decodes scene geometry directly from latents, avoiding expensive VAE decoding; supports dynamic scenes with dual constraints (camera-motion smoothing reward + geometric reprojection consistency reward). — https://arxiv.org/abs/2603.26599

3. **PerceptionComp: A Video Benchmark for Complex Perception-Centric Reasoning** — a video benchmark requiring multi-time-span visual evidence + compositional logical reasoning (1,114 questions / 279 videos). The strongest model, Gemini-3-Flash, reaches only 45.96%; open models stay below 40% — perception-centric long-horizon reasoning remains a bottleneck. — https://arxiv.org/abs/2603.26653

4. **GeoSR: Make Geometry Matter for Spatial Reasoning** — via Geometry-Unleashing Masking (masking 2D visual tokens to force reliance on geometry tokens) and Geometry-Guided Fusion (gated routing that adaptively amplifies geometry contributions), lets VLMs truly use 3D geometry for spatial reasoning; SOTA on static and dynamic benchmarks. — https://arxiv.org/abs/2603.26639

5. **Zero-Shot Depth from Defocus (FOSSA)** — a Transformer-based zero-shot focal-stack depth-from-defocus network; the core is a stack attention layer with focal-distance embeddings enabling efficient information exchange across the focal stack. Also releases the ZEDD benchmark (8.3x more scenes than its predecessor), cutting error by up to 55.7%. — https://arxiv.org/abs/2603.26658

## 2. Hot GitHub Open Source

1. [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) ⭐ 182.9k — Python. Autonomous AI agent platform supporting agentic workflow building and deployment; very actively updated.

2. [ollama/ollama](https://github.com/ollama/ollama) ⭐ 166.5k — Go. The standard tool for running LLMs locally; latest support for Kimi-K2.5, GLM-5, MiniMax, DeepSeek, Qwen and more.

3. [huggingface/transformers](https://github.com/huggingface/transformers) ⭐ 158.6k — Python. SOTA model-definition framework covering text/vision/audio/multimodal, continuously integrating the newest models (Gemma3, GLM, Qwen...).

4. [langflow-ai/langflow](https://github.com/langflow-ai/langflow) ⭐ 146.4k — Python. Visual AI agent and workflow building platform; low-code drag-and-drop multi-agent apps.

5. [langgenius/dify](https://github.com/langgenius/dify) ⭐ 135k — TypeScript/Python. Production-grade agentic workflow platform with RAG, MCP and multi-model orchestration; active pushes today.

## 3. HackerNews Top Posts

1. [Show HN: Muscle-Mem — behavior cache for AI agents](https://github.com/pig-dot-dev/muscle-mem) ⭐ 226 points · 51 comments — caches agent tool-calling traces like a JIT compiler; repeated tasks take deterministic replay, switching back to agent mode only on edge cases. A pragmatic answer to the $40/hr token cost of pure-vision agents.

2. [Show HN: Magnitude — AI-native web testing framework](https://github.com/magnitudedev/magnitude) ⭐ 179 points · 44 comments — replaces set-of-marks with a pure-vision VLM (Moondream), dual-agent architecture (planner + executor); a faster, cheaper E2E testing framework than browser-use.

3. [Show HN: AI agents built and shipped an app in 36 hours for $270](https://www.ninjaflix.ai/) — hot post — 4 AI agents collaborated end-to-end from tech-stack choice to deployment, building a news-to-short-video platform (Sora 2 Pro + Veo 3.1); exposes real multi-agent problems: groupthink, hallucination, unstable video quality.

4. [Show HN: How to red-team your AI agent in 48 hours](https://tachyonicai.com/blog/how-to-red-team-ai-agent/) — 4-stage framework: reconnaissance → automated scanning → manual exploitation → verified report. Core insight: prompt injection → tool abuse → data exfiltration is the most common attack chain; indirect injection (RAG/web) is severely underestimated.

5. [Show HN: Running AI agents across environments needs a proper solution](https://github.com/liquidos-ai/Odyssey) — a Rust-built agent runtime addressing Python agent memory bloat, slow Docker startup and agent reuse; bundle-first packaging and cross-environment deployment.

## 4. Deep Reads

| Type | Title | Why it matters | Link |
|------|-------|----------------|------|
| Paper | VGGRPO | latent-space GRPO for video geometric consistency; avoids VAE decode overhead; high engineering value | https://arxiv.org/abs/2603.26599 |
| Paper | GeoSR | systematic solution for VLM spatial reasoning; geometry-token utilization worth pondering | https://arxiv.org/abs/2603.26639 |
| Paper | PerceptionComp | new video multimodal reasoning benchmark; strongest model only 46%, huge research space | https://arxiv.org/abs/2603.26653 |
| Project | Muscle-Mem | pragmatic agent engineering; RPA + agent hybrid execution worth borrowing | https://github.com/pig-dot-dev/muscle-mem |
| Article | AI agent red-team methodology | systematic framework for production-grade agent security; must-read for engineering | https://tachyonicai.com/blog/how-to-red-team-ai-agent/ |

---
