# hackcv

陶土叙事风格的 AI 资讯站点 Hugo 主题。三栏目内容模型（**资讯 / 精读 / 实践**），内置自动栏目推断、Fuse.js 全站搜索、giscus 评论（GitHub Discussions）。

## 特性

- **三栏目内容模型**：文章按 `section`（`news` / `deep` / `practice`）与 `subtype`（`daily` / `weekly` / `paper` / `algorithm` / `code` / `perf`）归类；未显式声明的老文章由主题自动推断（`partials/content-meta.html`）
- **Fuse.js 全站搜索**：`/search/` 页面基于 `index.json`，支持栏目过滤与热门标签
- **giscus 评论**：GitHub Discussions 驱动，自定义主题 CSS
- **陶土叙事配色**：陶土橙（资讯）+ 深青（精读）+ 橄榄绿（实践），移动优先，WCAG AA 对比度
- **多语言**：zh-cn / en 双语

## 快速开始

```bash
# 1. 复制 exampleSite 作为站点骨架
cp -r themes/hackcv/exampleSite mysite
cd mysite

# 2. 用主题构建（exampleSite 的 themesDir 指向父级）
hugo --themesDir ../.. --minify

# 3. 本地预览
hugo server --themesDir ../.. -D
```

## 内容模型

### 三栏目

| section | 栏目 | 默认 subtype | 配色 |
|---|---|---|---|
| `news` | 资讯 | `daily` | 陶土橙 |
| `deep` | 精读 | `paper` | 深青 |
| `practice` | 实践 | `code` | 橄榄绿 |

在文章 front matter 中显式声明：

```yaml
---
title: "论文精读：xxx"
section: "deep"        # news | deep | practice
subtype: "paper"       # daily|weekly / paper|algorithm / code|perf
featured: true         # 首页热门精选
date: 2026-08-23
tags: ["AI", "论文"]
categories: ["研究简报"]
---
```

**栏目推断**（老文章零改动）：未写 `section` 时，主题按文件名/标题自动归类——`research-brief-*` 归资讯/每日简报，含 `week` 归资讯/每周总结，标题含"精读/解读/论文"归精读，含"实践/复现/性能"归实践。三个栏目页（`/news/` `/deep/` `/practice/`）由 `content/<section>/_index.md` 提供（见 exampleSite）。

### 关于页

`content/about.md` 使用 `layout: "about"`，模板内置：Hero、使命、三大栏目卡（计数自动统计）、内容原则、更新节奏、关于我（含 Token 消耗统计，从简报正文"总消耗约 N tokens"行自动汇总）。

## 页面

| 路径 | 模板 |
|---|---|
| `/` | `layouts/index.html`（Hero + 内容总览 + 热门精选 + 最新混合流） |
| `/news/` `/deep/` `/practice/` | `layouts/_default/column.html` |
| `/search/` | `content/search.md`（layout: search）+ `layouts/search.html` |
| `/about/` | `content/about.md`（layout: about）+ `layouts/_default/about.html` |
| 文章详情 | `layouts/_default/single.html`（文章头 + 正文 + 标签 + prev/next + giscus） |

## 配置

```toml
[params]
description = "站点描述"
github = "https://github.com/xxx"
email = "hello@xxx.com"
twitter = "xxx"
comments = true            # 文章页 giscus 评论区开关

[params.analytics]
umamiWebsiteId = "xxx"     # Umami 统计
umamiSource = "https://cloud.umami.is/script.js"
```

### giscus 评论

`single.html` 内置 giscus 脚本，开箱前需替换为你的仓库：

```html
data-repo="你的仓库"
data-repo-id="你的仓库 ID"
data-category="Announcements"
data-category-id="你的分类 ID"
```

### 搜索

搜索页基于 `index.json`（`layouts/index.json`，已含 section/subtype 字段）+ 主题自带 `static/js/fuse.min.js`，无需构建步骤。

## 开发

```bash
# 主题自测（exampleSite）
cd themes/hackcv/exampleSite
hugo server --themesDir ../.. -D
```

- 样式：`assets/css/main.css`（CSS 变量令牌驱动，见 `:root`）
- 栏目推断：`layouts/partials/content-meta.html`
- 三栏目配色：`--primary-*`（资讯）/ `--deep-*`（精读）/ `--practice-*`（实践）

## License

[MIT](LICENSE) © hackcv
