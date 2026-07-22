---
title: "从 hackcv.com 到 ai.hackcv.com：用 WorkBuddy 五天把静态博客重做成 AI 聚合站"
date: 2026-07-22T20:30:00+08:00
author: "小麦"
description: "一个不会 TypeScript、审美也一般的人，如何用 WorkBuddy 参考 aihot.virxact.com，把 hackcv.com 重做成 ai.hackcv.com。"
categories: ["随笔"]
tags: ["WorkBuddy", "AI", "hackcv", "折腾"]
cover: "/images/comparison.png"
draft: false
---

# 从 hackcv.com 到 ai.hackcv.com：一个不会 TypeScript、审美也一般的人，用 WorkBuddy 五天把静态博客重做成 AI 聚合站

> 副标题：全程由 WorkBuddy 生成代码 + 部署上线，参考了 aihot.virxact.com 的架构；赶上了 Hy3 的免费周期，试错零成本。

`ai.hackcv.com` 现在已经上线了，和它原来的兄弟站 `hackcv.com` 摆在一起，对比一目了然。借着这次"能对比了"的节点，我把整个改造过程写下来——它不是一篇技术教程（我没资格写），而是一份**真实的过程记录**：一个对 TypeScript 几乎零基础、审美也谈不上专业的人，是怎么在 WorkBuddy 的帮助下，把一个 Hugo 静态站重做成带 API、带 LLM 精选、能自己跑在云服务器上的 Next.js 聚合站的。

下面所有时间点、数字、命令结果，都来自 2026-07-10 到 07-14 这五天的工作日志，没有编造。

---

## 一、两个站摆在一起：改造前 vs 改造后

| 维度 | hackcv.com（改造前） | ai.hackcv.com（改造后） |
| --- | --- | --- |
| 技术栈 | Hugo 0.123.7 纯静态站 + nginx | Next.js 14（App Router）+ PostgreSQL 16 + Prisma |
| 内容形态 | 每日 AI 简报（论文 / 项目 / 资讯各 8 条） | 多源聚合 + LLM 精选 + 热度榜 |
| 数据接口 | 仅 RSS / JSON Feed | 9+ 个公开 REST API（items / daily / dailies / hot / search / tags / img-proxy …） |
| 精选与排序 | 无 | LLM 打分（0–100）+ 热度（信源数 × 精选分 × 时间衰减） |
| 信源 | 不展示 | 19–20 个（arXiv / GitHub / HN / 36氪 / 量子位 + YouTube 10 频道 + NVIDIA 等） |
| 搜索 | 无 | 全文搜索 + 标签 / 分类筛选 |
| 运营后台 | 无 | 条目 / 简报 / 信源 / LLM 状态 / token 统计 / 日志分析 / 更新日志 |
| 安全 | 无 | nginx + 分层限流 + HMAC 图片代理 + 后台鉴权 |
| 移动端 | 响应式静态页 | 底部导航 + 半屏速览 |
| SEO | sitemap / robots | sitemap + robots + OG 图 + 结构化数据 + 4 种 RSS Feed + llms.txt |
| 部署 | nginx 静态托管 | 腾讯云 Ubuntu + Nginx + systemd + certbot + crontab（含 Docker 方案） |

一句话总结：**从"一个每天更新的静态简报页"，变成了"一个有数据接口、能自动精选、能后台运营、能上云的独立产品"。**

![升级对照图](/images/comparison.png)

---

## 二、参考对象：aihot.virxact.com

这次重构不是闭门造车。7 月 10 号那天，WorkBuddy 把 `https://aihot.virxact.com` 扒了个底朝天——技术栈（Next.js App Router + MongoDB + EdgeOne CDN + nginx）、公开 API 端点（`/api/public/` 下的 items / daily / dailies / img-proxy，带 HMAC 签名）、页面结构（首页精选流 / 全部动态 / 日报 / 详情 / 接入文档 / 19 个主题页）、五大版块（ai-models / ai-products / industry / paper / tip），甚至连它的精选算法（Claude Fable 5 做摘要和打分）、安全机制（EdgeOne JS Challenge + UA 黑名单 + 分层限流）都整理成了分析报告。

然后**直接以 AI HOT 的架构为蓝本，给 hackcv.com 设计了完整重构方案**：Hugo 静态站 → Next.js 14（SSR/ISR）+ 数据库；补齐 9 个 REST 端点；引入 LLM 精选打分；多源信源；EdgeOne + nginx + 限流 + HMAC 图片代理；移动端底部导航；4 种 RSS Feed + 全套 SEO。

换句话说，我从一开始就不是在"从零发明"，而是在"照着一个跑得通的成熟架构，改出自己的版本"。这对新手极其重要——**你不需要先想清楚架构，先找一个对的参考对象，让工具帮你拆。**

![WorkBuddy 正在分析 aihot.virxact.com 架构](/images/screenshot-01-workbuddy-analyzing-aihot.png)
*图：7 月 10 号 WorkBuddy 正式拆解 aihot.virxact.com 的技术栈、API 端点、页面结构与安全机制——右侧面板同步写入当天工作日志。*

---

## 三、我不会 TypeScript，但站是用 TypeScript 写的

这是整件事里最违和、也最关键的一点。

新站是 **Next.js 14 + TypeScript + Prisma**——纯纯的 TS 项目。而我个人的 TS 水平，大概等于"知道 `<Type>` 尖括号是干啥的，但让我自己写一个 client component 的 hooks 顺序，我必翻车"。

证据就在日志里。比如 7 月 11 号修过这么一个 bug：退出登录时报 `Rendered fewer hooks than expected`。根因是 `admin/layout.tsx` 在 `useState` 之后、`useEffect` **之前**插了一个 early return，导致登录页和其他后台页走的 hook 数量不一致——这是 React/TS 里非常典型的坑。我（用户）看到的就是"退出登录报错了"；WorkBuddy 定位到是 hooks 顺序问题，把 early return 挪到所有 hook 声明之后，修好了。

再比如这五天里我下过的指令，全是这种大白话：

- "设计一个图标，更新到网站上。"
- "存量重跑下打分。"
- "管理后台新增 nginx 日志解析分析工具。"
- "修复 24h 趋势图没有数字，坐标轴是空的。"

没有一行是我写的 `.tsx` 或 `.ts`。WorkBuddy 把我这些口语化需求，翻译成了 `prisma/schema.prisma`、`src/lib/repository.ts`、`src/app/admin/logs/page.tsx` 这种具体文件。最后 git 提交的作者写的是 `cvley`，但真正"写代码"的是 WorkBuddy。

**我不会 TS，但项目是 TS 写的——这件事能成立，唯一的前提是：写 TS 的活儿不在我身上。**

![.next 被成批丢进废纸篓（部分）](/images/screenshot-02-next-trash-partial.png)
![.next 完整目录 204 项 / 1.9MB 被清理](/images/screenshot-03-next-trash-full.png)
*图：7 月 11 号某次重新编译后，整个 `.next` 目录被清空、成批丢进废纸篓——204 个文件、61 个文件夹、1.9 MB。第一次看到这阵仗，我有点慌。*

> **❓ 当时一个挥之不去的疑问：每次编译都删掉一两百个文件，这种"频繁创建又删除"正常吗？会不会把我的磁盘写坏？**
>
> 后来弄明白了，这其实是 TS / Next.js 开发的日常，**完全正常**：
> - **`.next` 是构建缓存，不是源码。** 它每次重新编译（尤其改了配置、或手动清缓存救急时）会把旧的 `.next` 整个删掉、再生成一版新的——所以废纸篓里才会一下子出现一两百个文件。我那两张截图，就是重编译后 `.next` 整目录进废纸篓的瞬间。
> - **丢进废纸篓几乎不写盘。** 这一步只是"同一块磁盘内的移动"（元数据操作）；真正写盘的是下一次编译重新生成 `.next`，但一次也就几 MB。
> - **磁盘寿命不用操心。** 现在 Mac 用的 SSD 按 TBW（总写入字节）算寿命，普遍是几百 TB 量级。即便一天编译 100 次、每次写 10MB，一年也就 ~365GB，离"写坏"差着两三个数量级。
>
> 所以结论很朴实：**别怕它删，那是它在"重新生成"，不是"在磨损你的电脑"。** 我当时那个担心，算是新手特有的、可爱又多余的焦虑——但这个问题本身，恰好说明了一个不会 TS 的人，第一次窥见"工程化开发"时的真实反应。

---

## 四、审美一般，但我能看出"不对"

第二个违和点：我审美一般。但好在我至少是个"能看出哪里不对"的普通用户，而这恰恰够用了。

最典型的例子是站点的 favicon。日志里记着它来来回回改了三轮：先做了"h + 右上角星点"；我觉得要体现"聚合"，让 WorkBuddy 改成"3 个信源小点汇流到 h"；结果看预览后又说"改回原来只有一个点的"——于是又回退。整个过程我一个 SVG 路径都没碰，全靠"看预览、说感觉"。

还有那个 24h 访问趋势图：第一版只有悬停才显示数字、坐标轴是空的，我说"没有数字，坐标轴是空的"，WorkBuddy 就给每根柱子加了数值、补了 Y 轴峰值刻度和 X 轴时间刻度。

这给我的启发是：**审美可以外包给迭代，但判断权必须留给自己。** 我不需要成为设计师，我只需要是个还能分辨"顺不顺眼"的普通访客。工具负责把"高级一点 / 别这么挤 / 坐标轴补上数字"翻译成具体改动，我负责在每次预览后说"还差点意思"或"就这个"。

---

## 五、Hy3 的免费周期：让我敢反复试错

这次改造全程跑在 **Hy3** 上，而且恰好赶上了它的**免费周期**。

这一点听起来不起眼，对结果的影响却是决定性的。一个不会 TS、也不敢一次写对的人，最怕的不是"难"，是"错了要付出代价"——额度焦虑会让你不敢让模型重写第三版、不敢把 207 条数据全量重打分、不敢为了一个图标来回改四轮。

免费周期把试错成本压到了零：

- 看不懂报错？贴给模型，它解释。
- 生成的东西跑不起来？让它改，再跑。
- 207 条存量数据重打分（rescore），写回 206 条、均分 80.6——这一波如果计费，我可能就偷懒跳过了；免费期里，直接全量跑。
- favicon 改了三版？免费期，改就是了。

**免费周期真正放大的不是"省钱"，是容错率。** 新手能推进项目，靠的就是"错了也不心疼"。

![Hy3 模型选择器：限时免费 高 0.00x ✓](/images/screenshot-04-hy3-free-period.png)
![Hy3 上下文用量 60.2%（115.6K / 192.0K）](/images/screenshot-05-hy3-context-usage.png)
*图：改造期间模型选择器显示 Hy3 正处于「限时免费」周期（费用倍率 0.00x），单次对话上下文消耗已达 60.2%——如果按计费跑，光 rescore 全量重打分 207 条就要花掉不少；免费期里直接跑，零犹豫。*

---

## 六、五天时间线（真实日志提炼）

![五天改造时间线](/images/timeline.png)

| 日期 | 关键动作 | 可验证结果 |
| --- | --- | --- |
| 7/10 | 分析 aihot.virxact.com；设计重构方案；JSON 文件存储 → PostgreSQL 16 + Prisma | `next build` 通过，33 条路由 |
| 7/11 | 修 3 个运行时崩溃；验证真实采集管线；接 SiliconFlow；8 家 LLM + token 统计；存量重打分；favicon 设计迭代 | 9 源入库，DB 30→207 条；rescore 206/207，均分 80.6 |
| 7/12 | 品牌图标全站上线；分类页崩溃修复 + 24 篇 paper 回填；采集节流 + 定时；更新日志可后台编辑；域名切到 `ai.hackcv.com` | 定时采集区分"每小时新闻 / 每 24h 论文" |
| 7/13 | 开发者中心 / CLI / Skill 页面；commit 并 push GitHub；**部署到腾讯云 qq_claw，`ai.hackcv.com` HTTPS 上线**；修 /daily 404；YouTube 接入（129 条视频）；nginx 日志分析（子站 + 主站双 tab）；24h 图补数字 | 全站页面 / API / feed / sitemap 均 200；certbot 证书自动续期 |
| 7/14 | 补 /hot 热度榜页面（修日志工具暴露的 404） | `npm run build` 通过，导航新增"热门"入口 |

注意 7/13 那一行：**部署是 WorkBuddy 通过 SSH 连到一台腾讯云 Ubuntu 服务器，自己写 Nginx 配置、systemd 服务、certbot 证书、crontab 定时采集，一步步把站跑起来的。** 我这边不是在本地点点鼠标，而是对着对话框说"部署到那台服务器"，剩下的 `nginx -t` / `migrate deploy` / `systemctl restart` 全是它干的。

---

## 七、结果：ai.hackcv.com 真的上线了

回头看，这个项目能跑通，靠的是四件事叠在一起：

1. **参考对象对**：aihot.virxact.com 给了现成可抄的架构，WorkBuddy 负责拆解和本地化。
2. **Hy3 免费周期**：给了随便试错的底气，favicon 能改三版、207 条能全量重打分。
3. **WorkBuddy 把"写代码 + 修 bug + 部署"整套动作接住了**：我只要动嘴说"想要什么""哪里不对"。
4. **我老老实实承认短板**：不会 TS、审美一般——反而把执行权彻底交给工具，自己只保留"判断对不对"的那部分。

最终 `ai.hackcv.com` 上线，原 `hackcv.com` 博客保持不变。整个过程里，我个人贡献的"技术含量"接近于零，但"项目完成度"是百分之百。

---

## 八、写给和你一样的人

如果你也符合下面任意一条，建议你照这条路试一次：

- 想做个站 / 改个站，但被"我得先学前端 / 先学 TS"劝退过；
- 对 TypeScript、构建、部署这些词有本能的恐惧；
- 自己审美说不清，但别人的东西好不好一眼能看出来。

别等"学会了再动手"。趁 Hy3 这类模型还有免费周期、趁 WorkBuddy 这种工具已经能把"生成 → 修复 → 部署"打通，**先动手，边做边学，甚至不学也行**。

我就是活例子：一个 TS 不会、审美一般的人，用 WorkBuddy 参考 aihot.virxact.com，把 hackcv.com 重做成 ai.hackcv.com，而且——它真的在 https://ai.hackcv.com 跑着呢。

你要做的，可能只是先打开对话框，说一句："帮我把这个站，照着那个参考站，改一版。"

---

*记录于 ai.hackcv.com 上线之后。全文时间点、数字、部署结果均取自 2026-07-10 至 07-14 的工作日志；改造全程由 WorkBuddy 生成代码与部署，模型运行于 Hy3 免费周期内，参考架构取自 aihot.virxact.com。*
