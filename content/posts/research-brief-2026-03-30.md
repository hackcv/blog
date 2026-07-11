---
title: "每日研究简报 2026-03-30"
date: 2026-03-30T22:11:00+08:00
draft: false
tags: ["AI", "大模型", "Agent", "计算机视觉", "音视频处理", "工程优化", "每日简报"]
categories: ["研究简报"]
description: "AI / 大模型 / Agent / 计算机视觉 / 音视频处理算法 / 工程优化 领域每日研究简报"
---

# 🌾 每日研究简报 · 2026-03-30

> 领域：AI / 大模型 / Agent / 计算机视觉 / 音视频处理算法 / 工程优化

---

## 📄 arxiv 最新论文（5篇）

### 1. GaussianGPT: Towards Autoregressive 3D Gaussian Scene Generation
- **方向**：3D生成 / 计算机视觉
- **摘要**：提出基于 Transformer 的自回归 3D 高斯场景生成模型，通过 next-token prediction 直接生成 3D Gaussians。使用稀疏 3D 卷积自编码器 + 向量量化压缩高斯原语，支持场景补全、外绘、可控采样。与扩散模型互补，天然支持 context-aware 3D 生成。
- **链接**：https://arxiv.org/abs/2603.26661

### 2. VGGRPO: Towards World-Consistent Video Generation with 4D Latent Reward
- **方向**：视频生成 / 工程优化
- **摘要**：提出 VGGRPO，在 latent 空间用 GRPO 做几何一致性视频后训练。引入 Latent Geometry Model（LGM）直接从 latent 解码场景几何，避免昂贵的 VAE 解码。支持动态场景，用相机运动平滑奖励 + 几何重投影一致性奖励双重约束。
- **链接**：https://arxiv.org/abs/2603.26599

### 3. PerceptionComp: A Video Benchmark for Complex Perception-Centric Reasoning
- **方向**：多模态大模型 / 视频理解
- **摘要**：提出 PerceptionComp，一个需要多时间段视觉证据 + 组合逻辑推理的视频 benchmark（1114题/279视频）。最强模型 Gemini-3-Flash 仅达 45.96%，开源模型低于 40%，揭示感知中心长时序推理仍是瓶颈。
- **链接**：https://arxiv.org/abs/2603.26653

### 4. GeoSR: Make Geometry Matter for Spatial Reasoning
- **方向**：VLM / 空间推理
- **摘要**：提出 GeoSR 框架，通过 Geometry-Unleashing Masking（遮蔽 2D 视觉 token 迫使模型依赖几何 token）和 Geometry-Guided Fusion（门控路由自适应放大几何贡献），让 VLM 真正利用 3D 几何信息做空间推理，在静态和动态 benchmark 上 SOTA。
- **链接**：https://arxiv.org/abs/2603.26639

### 5. Zero-Shot Depth from Defocus (FOSSA)
- **方向**：计算摄影 / 深度估计
- **摘要**：提出 FOSSA，基于 Transformer 的零样本焦距散焦深度估计网络，核心是带焦距距离嵌入的 stack attention layer，实现焦点堆栈间高效信息交换。同时发布 ZEDD benchmark（比前作多 8.3x 场景），误差降低最高 55.7%。
- **链接**：https://arxiv.org/abs/2603.26658

---

## 🔥 GitHub 热门项目（5个）

### 1. [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) ⭐ 182.9k
- **语言**：Python
- **简介**：自主 AI Agent 平台，支持 agentic workflow 构建与部署，持续活跃更新中。

### 2. [ollama/ollama](https://github.com/ollama/ollama) ⭐ 166.5k
- **语言**：Go
- **简介**：本地运行大模型的标准工具，最新支持 Kimi-K2.5、GLM-5、MiniMax、DeepSeek、Qwen 等主流模型。

### 3. [huggingface/transformers](https://github.com/huggingface/transformers) ⭐ 158.6k
- **语言**：Python
- **简介**：SOTA 模型定义框架，覆盖文本/视觉/音频/多模态，持续集成最新模型（Gemma3、GLM、Qwen 等）。

### 4. [langflow-ai/langflow](https://github.com/langflow-ai/langflow) ⭐ 146.4k
- **语言**：Python
- **简介**：可视化 AI Agent 和 workflow 构建平台，低代码拖拽式搭建多 Agent 应用。

### 5. [langgenius/dify](https://github.com/langgenius/dify) ⭐ 135k
- **语言**：TypeScript/Python
- **简介**：生产级 agentic workflow 开发平台，支持 RAG、MCP、多模型编排，今日仍在活跃推送。

---

## 🗞️ HackerNews 热帖（5条）

### 1. [Show HN: Muscle-Mem — AI Agent 的行为缓存](https://github.com/pig-dot-dev/muscle-mem) ⭐ 226分 · 51评论
像 JIT 编译器一样缓存 Agent 的 tool-calling 轨迹，重复任务走确定性回放，遇到边缘情况再切回 Agent 模式。解决纯视觉 Agent $40/hr token 成本问题的实用方案。

### 2. [Show HN: Magnitude — AI 原生 Web 测试框架](https://github.com/magnitudedev/magnitude) ⭐ 179分 · 44评论
用纯视觉 VLM（Moondream）替代 set-of-marks 方案，双 Agent 架构（规划器 + 执行器），比 browser-use 更快更便宜的 E2E 测试框架。

### 3. [Show HN: AI agents 36小时 $270 端到端开发并上线了一个 App](https://www.ninjaflix.ai/) ⭐ 热帖
4个 AI Agent 协作，从选技术栈到部署全自动，构建了一个新闻转短视频平台（Sora 2 Pro + Veo 3.1）。揭示了多 Agent 协作中 groupthink、幻觉、视频质量不稳定等真实问题。

### 4. [Show HN: 如何在 48 小时内红队测试你的 AI Agent](https://tachyonicai.com/blog/how-to-red-team-ai-agent/)
4阶段框架：侦察→自动扫描→手动利用→验证报告。核心洞察：prompt injection → tool abuse → 数据泄露是最常见攻击链，间接注入（RAG/web）被严重低估。

### 5. [Show HN: Running AI agents across environments needs a proper solution](https://github.com/liquidos-ai/Odyssey)
用 Rust 构建的 Agent 运行时 Odyssey，解决 Python Agent 内存占用大、Docker 启动慢、Agent 难以复用等工程问题，支持 bundle-first 打包和跨环境部署。

---

## 📋 深读推荐

| 类型 | 标题 | 推荐理由 | 链接 |
|------|------|----------|------|
| 论文 | VGGRPO | Latent 空间 GRPO 做视频几何一致性，工程价值高，避免 VAE 解码开销 | https://arxiv.org/abs/2603.26599 |
| 论文 | GeoSR | VLM 空间推理的系统性解法，几何 token 利用率问题值得深思 | https://arxiv.org/abs/2603.26639 |
| 论文 | PerceptionComp | 视频多模态推理的新 benchmark，当前最强模型仅 46%，研究空间巨大 | https://arxiv.org/abs/2603.26653 |
| 项目 | Muscle-Mem | Agent 工程化的务实方案，RPA + Agent 混合执行思路值得借鉴 | https://github.com/pig-dot-dev/muscle-mem |
| 文章 | AI Agent 红队测试方法论 | 生产级 Agent 安全的系统性框架，工程落地必读 | https://tachyonicai.com/blog/how-to-red-team-ai-agent/ |

---

> 📅 生成时间：2026-03-30 22:11 CST | 数据来源：arxiv API · GitHub API · HackerNews Algolia API
