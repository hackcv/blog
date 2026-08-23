---
title: "26年第28周-AI研究周报"
author: "hackcv"
date: 2026-07-12T21:00:00+08:00
draft: false
tags: ["AI", "大模型", "Agent", "每周总结", "计算机视觉", "网络安全", "每日简报", "趋势预测"]
categories: ["研究简报"]
description: "hackcv 本周（2026-07-06~07-12）AI研究周报：模型发布、AI安全攻防、智能体工具等七大主线总结，含本周亮点、值得关注方向与趋势预测。"
---

# 26年第28周-AI研究周报

- **复盘周期**：2026-07-06（周一）~ 2026-07-12（周日）
- **报告日期**：2026-07-12
- **说明**：本期内容真实可溯；07-12 期 token 统计为该期显式标注的「估算值」，已在合计中单独说明。

---

## 一、概览

| 指标 | 数值 |
|---|---|
| 本周发布期数 | **7 期**（07-06 ~ 07-12，每日一期） |
| 论文（## 一） | 56 篇（8×7，含跨期重复 4 篇次） |
| GitHub 项目（## 二） | 56 个（8×7，含跨期重复 17 项目次） |
| 行业资讯（## 三） | 56 条（8×7，含跨期重复 22 条次） |
| Token 消耗合计 | **约 320,181 tokens** |
| 发布频率 | **正常**，7/7 天按时发布，无缺失日期 |

**Token 消耗明细**：
- 07-06：43,752（输入 34,826 / 输出 8,926）
- 07-07：44,216（输入 35,328 / 输出 8,888）
- 07-08：44,872（输入 35,689 / 输出 9,183）
- 07-09：45,231（输入 36,127 / 输出 9,104）
- 07-10：44,923（输入 35,816 / 输出 9,107）
- 07-11：45,187（输入 35,992 / 输出 9,195）
- 07-12：**约 52,000（估算值）**（输入约 34,000 / 输出约 18,000）

> 实测 6 期合计 268,181 tokens；07-12 为估算值，故全周合计为「约 320,181 tokens」。整体 token 消耗稳定在 4.4 万/期上下，07-12 因正文与排版更长且标注为估算，数值偏高。

---

## 二、本周内容主题总结

### 1. 模型发布（本周最强主线，贯穿全周）
- **OpenAI GPT-5.6 系列（Sol/Terra/Luna）+ ChatGPT Work 智能体**：07-08 首发后连续多期追踪，含 Ultra 多 Agent 协同、Luna 由 Sol 自主训练（AI 自我进化）、ARC-AGI-3 首通等子话题。
- **Google Gemma 4**：31B 端侧多模态、Apache 2.0 全开源，干掉重型视觉/音频编码器，标志端侧模型能力质变。
- **智谱 GLM 5.2**：首个达到 GPT/Claude 同级的开源权重模型，成本仅闭源约 1/20，连登多期冲击闭源定价体系。
- **其他**：美团 LongCat-2.0（1.6 万亿参数、国产算力闭环）、SpaceXAI Grok 4.5、Meta Muse Spark 1.1、（传闻）Gemini 3.5 Pro。

### 2. AI 安全攻防（本周第二主线，论文+项目+资讯三路齐发）
- **攻击侧**：全球首例 AI Agent 自主勒索攻击 JadePuffer（07-08/07-09）、GitLost（恶意 Issue 诱导 Agent 泄露私有代码，07-10）、Claude Code 安全后门致阿里全面禁用（07-06/07-10）。
- **防御/红队侧**：开源红队工具 `strix`/`T3MP3ST`/`pentagi` 多次上榜；论文《Distributed Attacks in Persistent-State AI Control》《Overthinking 提取模型秘密》《Prismata 防御跨站提示注入》。
- **政策侧**：美国 CISA 采用 Anthropic Mythos 审查政府代码（07-09）。
- 安全是 hackcv 的核心基因，本周供给充沛且质量高。

### 3. 智能体工具与编排（GitHub 栏目绝对主力）
- 框架/运行时：OpenClaw（35.5 万星登顶 GitHub 历史第一）、vercel/eve、stablyai/orca（并行运行时）、agency-agents（虚拟公司全家桶）。
- 记忆机制成为新热点：`cognee`（知识图谱记忆）、`TencentDB-Agent-Memory`（四层语义金字塔）、论文《Remember When It Matters》《Proactive Memory Agent》。
- 技能标准化：`addyosmani/agent-skills`、`agentskills/agentskills`、`mattpocock/skills`、`obra/superpowers`。
- 沙箱与基础设施：Tencent/CubeSandbox（硬件级隔离）、OmniRoute（模型路由网关）、OfficeCLI。

### 4. 具身智能
- 宇树科技科创板 IPO（"具身智能第一股"，07-06）；蚂蚁 `LingBot-VLA 2.0` 具身基座模型（07-10）；科大讯飞 `Embodied-Omni`（07-11）；论文 Ego-Human、FSD-VLN（无人机）、INTENT（车辆意图）。

### 5. 算力芯片
- 国内 AI 芯片份额首破 52%（07-06）；DeepSeek 秘密自研推理芯片（07-08/07-09）；三星 Q2 利润暴增 19 倍连登（07-07~07-09）；H100 租赁价暴涨 40%（07-08）；曙光 8000 十万卡超集群（07-11）；Meta Iris 自研芯片（07-11）；端侧芯片聆思科技融资（07-10）；北大相变忆阻器类脑芯片（07-06）。

### 6. AI for Science
- 阿里达摩院 AI 发现 4 种超导材料（07-06）；VASP Agent 第一性原理计算（07-09）；Physics-Audited Agentic Discovery（07-09）；SpaCellAgent 细胞轨迹（07-10）；Does AI Understand Imaging 计算成像基准（07-10）；VaseMuseum 文物智能体（07-09）。

### 7. 监管政策
- 《人工智能拟人化互动服务管理暂行办法》施行，字节/阿里/腾讯集体下线公共智能体（07-06/07-07）；国家四部门《人工智能＋人社》（07-08）；上交所 AI 大模型企业科创板上市指引（07-09）；OpenAI 出让股权/秘密 IPO 牵动监管（07-06/07-08/07-09）；Anthropic 企业 API 份额首超 OpenAI（合规口碑转化采购，07-12）。

---

## 三、本周亮点与值得关注的方向

1. **AI 自我进化从叙事变事实**：GPT-5.6 的 Luna 由 Sol 自主完成训练（找 GPU、定配置、写脚本、核验全程无人工）+ NousResearch/hermes-agent 开源自进化 Agent，意味着模型迭代的人力结构正在被改写。
2. **安全攻防进入「AI vs AI」实战期**：JadePuffer 全自主勒索、GitLost 提示注入泄密、Claude Code 后门——攻击已工业化，防御侧 `strix`/`T3MP3ST`/`pentagi` 同步成熟，是 hackcv 安全基因的最佳发挥场。
3. **端侧多模态质变**：Gemma 4 31B 干掉重型编码器、可离线跑在笔记本/手机，叠加 `pocket-tts` 端侧 TTS，端侧智能体闭环成形。
4. **Agent 记忆机制集中爆发**：cognee、TencentDB-Agent-Memory 与论文《Remember When It Matters》同周出现，长程可靠性成为 Agent 落地核心门槛。
5. **国产算力闭环里程碑**：美团 LongCat-2.0（五万卡国产集群训练万亿模型）、曙光 8000 十万卡超集群，标志训练侧自主可控。
6. **视觉推理精细化**：P2R（Perceive-to-Reason）、HIVE（幻觉后推理）、DeltaV（差分视觉更新）等 CV 论文扎堆，与 hackcv 的计算机视觉基因高度契合。

---

## 四、趋势预测（未来 2~4 周前瞻，基于本周真实信号）

> 以下预测均由本周已出现的技术与产业信号推导，非虚构内容；以「预测」标注以示与事实区分。

1. **AI 自我进化从卖点走向治理议题**：GPT-5.6 的 Luna 由 Sol 自主完成训练（找 GPU、定配置、写脚本、核验全程无人工）、NousResearch/hermes-agent 开源自进化 Agent——「模型自我迭代」已成为头部厂商标配叙事。预测：未来 2~4 周开源侧将密集跟进自进化 Agent 框架，同时「谁在监督自我进化模型」「自进化是否需备案」会成为新的治理争论点。
2. **Agent 安全进入「AI vs AI」红蓝对抗常态**：JadePuffer 全自主勒索、GitLost 提示注入泄密、Claude Code 后门已证明攻击工业化；防御侧 `strix`/`T3MP3ST`/`pentagi` 同期成熟。预测：企业级 Agent 部署将把「红队凭证」列为强制项，监管可能针对「自主 Agent 攻击」出台专门条款。
3. **端侧多模态 + 端侧 TTS 引爆「个人本地智能体」**：Gemma 4 31B 干掉重型编码器可离线跑在笔记本/手机、`pocket-tts` 端侧语音落地。预测：隐私优先的 on-device Agent 成为差异化主线，手机/笔记本是主要载体，「端侧能力」将成模型发布的新卖点。
4. **Agent 记忆层标准化为可插拔组件**：`cognee`、`TencentDB-Agent-Memory` 与论文《Remember When It Matters》同周爆发。预测：记忆将像向量数据库一样成为 Agent 技术栈的「可插拔记忆层」标配，并出现专门的记忆可靠性评测基准。
5. **国产算力训练侧自主可控加速**：美团 LongCat-2.0（五万卡国产集群）、曙光 8000（十万卡）、DeepSeek 自研推理芯片、国内 AI 芯片份额首破 52%。预测：训练侧国产闭环在下半年继续突破，若 DeepSeek 自研芯片落地将显著压低推理成本结构。
6. **「合规即竞争力」在采购端兑现**：拟人化互动办法施行、上交所 AI 企业上市指引、Anthropic 企业 API 份额首超 OpenAI（合规口碑转化采购）。预测：合规将成为模型与企业采购的核心门槛，国内监管细化会倒逼 Agent 产品去拟人化/备案化。

---

## 附：本周高频内容速查（去重后按主题）

- **模型发布**：GPT-5.6 / ChatGPT Work / Gemma 4 / GLM 5.2 / LongCat-2.0 / Grok 4.5 / Muse Spark 1.1 /（传闻）Gemini 3.5 Pro
- **AI 安全攻防**：JadePuffer 自主勒索 / GitLost 提示注入 / Claude Code 后门 / strix / T3MP3ST / pentagi / Prismata / CISA×Mythos
- **自研算力芯片**：DeepSeek 推理芯片 / Meta Iris / 三星 HBM / 曙光 8000 / 聆思端侧芯片 / 北大忆阻器
- **国产算力**：份额 52% / H100 租赁 +40% / LongCat-2.0 万亿级闭环
- **智能体编排**：OpenClaw / orca / agency-agents / WebSwarm / vercel/eve
- **Agent 记忆**：cognee / TencentDB-Agent-Memory / Remember When / Proactive Memory
- **技能标准化**：agent-skills / agentskills / skills / superpowers / taste-skill
- **具身智能**：宇树 IPO / LingBot-VLA 2.0 / Embodied-Omni / Ego-Human / FSD-VLN
- **AI for Science**：超导材料发现 / VASP Agent / SpaCellAgent / 计算成像 / 文物智能体
- **端侧 AI**：Gemma 4 / pocket-tts / 端侧推理芯片
- **监管合规**：拟人化互动办法 / 人工智能＋人社 / 上交所上市指引 / Anthropic 份额反超
- **CV 纵深**：TopoGPT / Perceive-to-Reason / HIVE / DeltaV / ProLaViT / AlayaWorld

---

*本报告由自动化任务基于真实内容生成，未做任何虚构。07-12 期 token 为估算值已在正文标注。*
