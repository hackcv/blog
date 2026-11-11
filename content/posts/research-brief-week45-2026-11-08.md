---
title: "26年第45周-AI研究周报"
date: 2026-11-08T20:30:00+08:00
draft: false
categories: ["研究简报"]
tags: ["AI", "Agent", "计算机视觉", "网络安全", "每周总结", "趋势预测"]
description: "26年第45周 AI 研究周报：近七天内容趋势复盘"
---

# 26年第45周-AI研究周报

> 复盘周期：2026-11-02（周一）~ 2026-11-08（周日） ｜ 每周日更新

## 一、概览

本周（第 45 周）共发布《AI 研究简报》7 期（11/02–11/08，每日一期），覆盖 arXiv 论文、GitHub 开源项目、精选行业资讯三大栏目，每期各 8 条，主线内容共 168 条；其中 11/04 另含 1 条「持续追踪」，本周合计 169 条。发布节奏稳定（每日约 20:30 更新，7/7 连续无断更），发布频率正常。

本周内容呈现三条清晰的主轴：① 模型能力继续「商品化 + 价格被压垮」，开放权重与主权 AI 同步放量；② Agent 从「能干活」转向「可治理、可审计、可编排」的生产组件；③ 资本端出现明显的「估值双杀」与价格战信号，倒逼工程侧「少讲故事、多交付」。安全、端侧、视频生成、世界模型、AI for Science 等方向均有密集且有代表性的进展。

## 二、本周内容主题总结

### 1. 模型发布与开放权重：能力商品化，选「赢家」已无意义

本周模型侧的关键词是「专业化 + 开放 + 降本」。国产与开源阵营持续放量：美团发布 **LongCat-2.5**（1.6T MoE、主攻长程 Agent 与复杂代码工程）；小米开源 **Xiaomi-OCR-0**（0.8B 文档理解，开放权重 + MCP + Agent Skill）；百度发布 **ERNIE 5.5 Flash Base** 权重（280B MoE）；Mistral 在 Large 4 开放权重后又推出 **Voxtral 3** 语音栈，并出现开放权重的 **Apriel Voice 27B**（语音 + 推理 + 工具 + 图文）；Google 开源 **EmbeddingGemma 2**（740M 多模态嵌入，本地向量存储降 6×）；Nace AI 开源 **Drex Max v1**（27B 端侧决策，Mac 调优）；Thinking Machines 推出 **Inkling 2 Small**（先安全测试后 Apache 2.0 开放）。闭源侧同样密集：OpenAI **Images 2.6**（GIF + 提速 50%）、**Gemini Omni 1.2 Flash**（视频生成/编辑降价）、Cohere 完成 **70 亿加元 Series E**（加拿大政府入股、定位主权 AI）。11/02 还集中曝光了 **GPT-6.2 Astra 灰测**与 **Claude Mythos 5.5** 泄露（均非官方）。行业共识正在从「挑更强的模型」滑向「怎么编排、怎么治理、在谁的掌控下跑」。

### 2. AI 安全攻防：从被动拒答到主动追问与分级开放

安全议题本周高频且立体。治理侧：OpenAI 更新模型行为准则、把「忠于人类」列为首条，并**暂停 GPT-6.1 Astra 发布、收紧工具调用监控**；将 **GPT-6 Cyber** 仅向审核通过的安全客户开放——前沿模型按「风险画像」而非仅付费墙分级开放，正在成为新范式（Gemini 4 Carbon 首发给网络防御者同属此列）。技术侧：针对「跨模态逻辑汇聚」的隐式风险有 **ThinkingGuard**（ACM MM 2026）；**SAFE-PRO** 主张在意图层主动追问而非被动拒答；**Visual Token 压缩**被证明反而增强鲁棒性（jailbreak 防御 +13.29%）；**HalluScope** 把幻觉做到细粒度诊断；**GraphSeal / VIPBench** 盯住语音深度伪造与嗓音身份；**ATAR** 用可解释工具调用做图像伪造检测。Agent 安全尤其值得警惕：**Benign Skills** 论文指出给 Agent 加良性技能虽提升良性任务 10.3 个百分点，却同步拉高不安全动作率 10.3 个百分点。攻防扩散信号：Wired 报道开源 **DeepSeek 完成 73% 黑客任务 vs OpenAI Daybreak 81%**，成本仅约 1/10，直接冲击「限制访问以延缓扩散」的论调。监管侧美国司法部披露 **AI 虚构学生骗贷逾 2 亿美元**案。

### 3. 智能体工具与编排：从「能干活」转向「可治理、可审计」

Agent 基础设施本周的重心明显从能力堆砌转向工程编排与可信治理。框架工程的价值被量化：**IBM 用同一开源模型只换智能体框架，任务完成率从 30% 干到 81%**——「怎么让模型干活」比「换更强模型」更影响落地。编排层收口：Factory 发布**模型无关的 Droid 1.0**，呼应 Anthropic「避免过度子 agent 扇出」的提醒；Google **ADK 2.14 将 A2A 协议标记为稳定**，跨厂商 agent 互操作有了官方标准；**Claude Code 2.1.319 把 MCP 工具调用转入后台执行**，长任务不再阻塞主交互。治理与审计工具密集出现：Uber 开源 **ADR**（Agent 灾难恢复）、**iFixAi** 120 秒内审计 Agent 是否按预期执行、**asqav-sdk** 提供量子安全签名的可验证证据、Cloudflare 推出 **Agent 流量治理**、Box 发布 **Architect** 面向 Agent 内容工作流、Vercel 把 **agent-browser「AI 同事」** 产品化。研究侧：**Routed Continual Learning**（Meta FAIR，API 成本降 72%）、**SPyCE**（技能-策略协同进化）、**OpenVLHarness**（视觉 Agentic 工具调用）、**RecSA**（百万 token 外推至对数级成本）、**SKIM**（agent 类别感知剪枝）为长程、低成本、可落地 Agent 提供方法。**Beneath the Surface** 与 **DelegateEval** 则分别给「Agent 自我进化」降温、为「个人对外服务 Agent」建立评测框架。

### 4. 多模态与视频生成：理解先于渲染成为共识

视频生成方向出现共识性转向——瓶颈不在 DiT 堆料，而在理解链路与 Agent 能力。可灵团队首次系统复盘，把「理解栈（数据—条件—对齐—评估）」而非「渲染栈」作为可控生成的瓶颈（**Behind Video Generation**）；**EvoWorld** 把「视线之外的因果演化」单独拎出来度量并给出基准；**SleuthVLM** 给出反直觉结论——omni 理解的瓶颈不是「听」而是 Agent 能力，用 27B VLM 击败所有开源 omni 模型。统一表征 **Omni-Encoder** 用单一 SigLIP-2 ViT 共享参数处理图/视频/音频/音视四模态。视频生成落地件持续补强：**Gemini Omni 1.2 Flash** 下调视频生成定价、**LiveFoley / Chronos / TaoMate-HD / ReVi** 分别覆盖实时音画、身份保持、数字人、长视频回顾。行业侧 OpenAI **Images 2.6** 加入 GIF 并提速 50%。

### 5. 端侧与本地推理：门槛持续下探

「在自己机器上改模型、跑模型」正变成日常工程。轻量模型持续刷新下限：**Light-MER** 把多模态情感识别压到 sub-1B 仍 SOTA；**Xiaomi-OCR-0**（0.8B）、**EmbeddingGemma 2**（740M）、**Drex Max v1**（27B Mac 调优）把文档、检索、决策压到端侧。**colibri**（纯 C 编写的 MoE 分级推理引擎，热/温/冷专家分层放置 + NVMe 流式加载）让普通硬件也能跑超大 MoE；**heretic** 用训练-free 手段本地改模型行为（去审查、去 AI 味）；**Nace Drex、AnyModelBot、OpenMausBot** 等把「本地优先 + 多模型入口」做成开源方案。**MiniMax M3.1 Flash 428B** 的社区量化/部署方案被官方汇总，推动超大 MoE 从「能下载」走向「能落地」。

### 6. 具身智能与世界模型：可推导、可解释的基础在补

当行业沉迷 scaling 时，顶尖团队回身补「可推导、可解释」的地基。清华姚期智团队提出**「代数世界模型」**（主张像牛顿一样从数据迈向可推导物理规律），同期西湖大学成立**世界模型研究中心**。**EvoWorld**（视线之外因果演化）、**Seeing Beyond the Next Step**（把世界模型前瞻摊销进策略、部署时移除世界模型做单步前向）把世界模型推向可控、可部署。**Hugging Face LeRobot 0.7** 支持流式训练与实时策略交互，显著降低具身实验门槛。垂直落地样本扎实：**SMILE** 多智能体临床推理（肝脏超声）、**BOMMA** 桥梁运维多智能体（调度召回 99.40%）、**MUSTARD** 动态异常检测（把异常从单帧推进到时序运动）。Stanhope AI 用 Friston「主动推断」做低功耗自主决策，是「后 LLM」路线的早期押注。

### 7. 算力、基建与资本：整合期、价格战与「估值双杀」

资本侧本周最刺眼的是「估值双杀」：OpenAI 完成 **110 亿美元新融资但估值降至 1.25 万亿**（低于最初 1.4 万亿目标），Anthropic IPO 投标价低至 **1.1 万亿**（远低于 2 万亿放风）。更硬的信号来自 Ramp：**企业 AI token 支出环比增速从 7 月 42% 骤降至 8–9 月 1.5%**——用量在涨、金额持平，token 正变成薄利多销的基础设施（OpenAI、Anthropic 均已大幅降价）。基建进入整合期：谷歌以约 **170 亿美元**承接 Crusoe 怀俄明 **10GW** 在建数据中心；英伟达拓展 Vera Rubin + Oracle 云部署、锁定首尔 AI Day，并以 1150 亿美元并购 Lumentum（光互连）、投资 Naver 10 亿美元。推理层被资本追捧（Fal 融资 13 亿、估值翻倍至 160 亿）。地缘约束凸显：OpenAI 因数据中心争议转向「社区共治」；Menlo 调研显示**美国企业开源模型支出 89% 流向中国模型**（Kimi 61%、DeepSeek 15%、GLM 11%）。

### 8. AI for Science 与行业落地

科研与垂直场景持续用 Agent 提效：**SMILE**（肝脏超声报告）、**MUSTARD / OmniAD**（工业异常检测，MMAD 79.9% 准确率）、**WhatIf**（LLM 社会仿真用于政策推演，UIST 2026）、**PromptBN**（LLM 驱动贝叶斯网络结构发现）、**Time-R1**（时序预测慢思考 RL）。金融侧 **TradingAgents**（多智能体交易）、**Kronos**（「K 线语言」基础模型）把 Agent 与基础模型落到量化场景。

### 9. 监管与主权

监管节奏出现「喘息而非免责」：欧盟《数字综合法案》(Reg 2026/1744) 把 AI 法案高风险义务推迟至 2027/2028，但透明度义务仍按原定施行。主权 AI 从口号变现金：Cohere 加拿大政府直接入股、绑定算力基建承诺。Anthropic 为 Claude 接入 **Plaid 只读个人理财连接**（不用于训练），划清个人 Agent 触碰敏感数据的可信边界。

## 三、本周亮点与值得关注的方向

- **「框架 > 模型」被实证**：IBM 同模型换框架 30%→81%、Factory Droid 模型无关编排、Anthropic 单 agent 循环倾向——落地杠杆正在从被调用的模型转移到编排/验证层。
- **安全分级开放成范式**：GPT-6 Cyber 限安全客户、Gemini Carbon 给防御者，配合 SAFE-PRO 主动追问、Benign Skills 量化副作用，安全设计从「事后护栏」前移到「能力路由 + 意图层」。
- **视频生成的「理解先于渲染」**：可灵复盘、EvoWorld、SleuthVLM 三篇互为印证，视频模型竞赛的下一度量很可能是「世界一致性与可控性」而非单纯画质。
- **Agent 治理工具井喷**：iFixAi、asqav-sdk、uber/ADR、Cloudflare Agent 流量治理、Box Architect 共同指向「Agent 进生产环境后的可审计、可恢复、可管控」刚需。
- **「公众买账」成为 AI 基建新变量**：OpenAI 数据中心争议后转向社区共治、改口「compute campuses」，地方政治约束开始反作用于算力扩张。
- **中国开源模型出海被量化**：Menlo 一手数据（89% 美国企业开源支出流向中国模型）为选型与地缘判断提供了硬证据。

## 四、趋势预测（未来 2~4 周前瞻）

> 以下为基于本周真实信号的推断，以「预测」标注，与上述事实明确区分。

- **预测 1（Agent 治理层标准化）**：在 IBM 换框架 30%→81%、iFixAi、asqav-sdk、uber/ADR、Claude Code 后台 MCP 等密集信号下，未来 2–4 周「可审计、可验证、可恢复」的 Agent 治理工具会继续集中涌现，且大概率向「标准化审计格式 + 量子安全签名」收敛，成为企业接入 Agent 的默认前置件。
- **预测 2（国产基座权重持续开放）**：百度 ERNIE 5.5 Flash Base、Mistral Large 4、DeepSeek 等已把开放权重做成常态，叠加 Menlo 显示的「中国模型海外采用率走高」，预测未来几周会有更多国产大模型放出可微调基座权重，主权 + 成本门槛继续下探。
- **预测 3（视频评测转向世界一致性）**：可灵复盘、EvoWorld、SleuthVLM 把「理解 / 因果一致性」摆上台面，预测视频生成 benchmark 会从画质/时长竞赛，新增「跨镜头身份、音视契约、视线之外演化」类可度量指标，影响下一轮模型发布话术。
- **预测 4（token 价格战深化、本地推理升温）**：Ramp 数据（支出增速骤降、单价砍半）与 Fal 估值跃升共同说明价值正向「推理/部署层」迁移；预测更多企业会采用模型无关网关（new-api 类）与本地/端侧推理（colibri、heretic 类）来对冲价格与合规风险。
- **预测 5（前沿能力走「白名单 + 审计」路线）**：GPT-6 Cyber 按风险分级开放、Gemini Carbon 先给防御者，预测后续高危能力（尤其是攻防、自主操作类）会更普遍地以「审核白名单 + 使用审计」而非「付费即开」的方式释放，安全评测透明度之争会加剧。
- **预测 6（资本理性化倒逼交付）**：OpenAI/Anthropic 同周「估值双杀」、Ramp 的「用量涨金额平」，预测 AI 叙事从「规模故事」转向「单位经济与可运维交付」，能证明 Agent 跑稳、跑便宜的团队更受资本青睐。

## 附：本周高频内容速查

| 主题 | 高频关键词（去重） |
| --- | --- |
| 模型 / 开放权重 | LongCat-2.5、Xiaomi-OCR-0、ERNIE 5.5 Flash Base、Mistral Voxtral 3、Apriel Voice 27B、EmbeddingGemma 2、Inkling 2 Small、GPT-6.2 Astra、Claude Mythos 5.5 |
| AI 安全 | GPT-6 Cyber 分级开放、ThinkingGuard、SAFE-PRO、HalluScope、GraphSeal、Benign Skills、DeepSeek 攻防 73%、AI 骗贷 |
| 智能体编排 / 治理 | Droid 1.0 模型无关、A2A 稳定、MCP 后台化、iFixAi、asqav-sdk、uber/ADR、Cloudflare 流量治理、Box Architect、Vercel AI 同事 |
| 多模态 / 视频 | 理解先于渲染、EvoWorld、SleuthVLM、Omni-Encoder、Gemini Omni 1.2 Flash、Images 2.6、LiveFoley、Chronos |
| 端侧 / 本地推理 | Light-MER sub-1B、colibri 分级 MoE、heretic 训练-free、Drex Max v1、AnyModelBot、M3.1 Flash 量化 |
| 具身 / 世界模型 | 代数世界模型、西湖大学研究中心、LeRobot 0.7、Seeing Beyond、SMILE、BOMMA、MUSTARD |
| 算力 / 资本 | 估值双杀（1.25 万亿 / 1.1 万亿）、Ramp 支出骤降、Crusoe→谷歌 170 亿、Vera Rubin、Fal 160 亿、Menlo 89% |
| AI for Science | 肝脏超声 SMILE、工业异常 MUSTARD/OmniAD、WhatIf 政策仿真、PromptBN、Time-R1、Kronos K线 |
| 监管 / 主权 | 欧盟推迟高风险义务、Cohere 政府入股、Claude+Plaid 只读、主权 AI |
