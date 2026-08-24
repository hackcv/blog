---
title: "实践：文字与马赛克自动擦除 + 画质增强——一条 CPU 上的完整图像处理流水线"
author: "hackcv"
date: 2026-08-23
section: "practice"
subtype: "verify"
tags: ["AI", "OCR", "图像擦除", "PP-OCRv4", "马赛克检测", "实践"]
categories: ["研究简报"]
description: "PP-OCRv4 DBNet 文字检测 + 纯 CV 马赛克检测 + 多来源掩码 OR 合并 + LaMa 擦除，再接「分析→修复→放大→精修」画质增强四阶段，全程 CPU；含色彩保真踩坑实录。"
---

> **一句话结论**：一套纯 CPU 的端到端图像处理流水线——**PP-OCRv4 DBNet 定位文字（0.2~0.5s）+ 纯 CV 检测马赛克（实时）+ 掩码 OR 合并交给 LaMa 擦除（2.1s）**，之后可选接「分析→修复→放大→精修」四阶段画质增强。实测字幕条场景全流程 ≈3s/帧（1920×1080）。

## 背景与动机

- **场景**：批量去字幕/水印/标注、隐私打码去除、老照片抢救
- **痛点**：全量 OCR（含识别分支）又大又慢；马赛克检测常被做成要训练的模型；擦除后画质往往需要增强——**没有一个纯 CPU 可跑的完整闭环**
- **约束**：与擦除基准篇相同——ONNX Runtime CPU 路线

## 核心思路（三层流水线）

### 第一层：检测（自动生成掩码）

**文字检测（PP-OCRv4 DBNet）**：
- 只用**检测分支**（DB 文本检测），不跑识别——模型 ~4.5 MB、CPU 0.2~0.5s/张
- 输出文字多边形框 → 转二值掩码 → 按框膨胀覆盖笔画边缘

**马赛克检测（纯 CV，零模型）**：
- 基于马赛克的视觉特征：**块状网格 + 局部高频缺失**——用网格梯度一致性判定
- `--mosaic-grid-thr` 控制严格度（0.7~0.9 是多数图的安全区间，人脸打码建议 0.9）
- CPU 实时（毫秒级），无需加载任何模型

### 第二层：掩码合并 + 擦除

- 多来源掩码（文字 + 马赛克 + 手动涂抹）**按位 OR** 合并为一张总掩码
- 统一 `--dilate + --feather` 后交给 LaMa（三模型选型见基准篇）
- `--roi x,y,w,h` 限定检测区域——只擦字幕条，避免误伤画面主体
- 多个文字框先经 `_merge_boxes`（IOU 合并）减少碎片掩码；再统一膨胀

**检测参数（真实实现值）**：DBNet 推理阈值 `thresh=0.2`、框过滤 `box_thresh=0.35`、`unclip_ratio=1.8`（文字框外扩比例）——`unclip_ratio 1.8` 意味着文字框在生成掩码时向外扩 1.8 倍，正好补足笔画边缘残留，是"文字擦干净"的关键参数。

### 第三层（可选）：画质增强四阶段

擦除后接 `enhance.py` 的**「分析 → 修复 → 放大 → 精修」**流水线（全部 ONNX Runtime CPU）：

| 阶段 | 做什么 | 关键模型（CPU 验证） |
|---|---|---|
| 分析 | NIMA 画质评分 + 实拍/二次元判别 | NIMA mobilenet（~MB级） |
| 修复 | 去 JPEG 伪影 / 去噪 / 去运动模糊 | 1xDeJPG/1xDeNoise（PLKSR）、1x-hurrdeblur（0.18 MB，极快） |
| 放大 | 超分 2x/4x | SPAN-4x（1.7 MB 最快）、Real-ESRGAN general-fast（5 MB 细节扎实）、Real-CUGAN（二次元） |
| 精修 | 人脸修复 | YOLOv8n-face 检测 5 关键点 → GPEN-BFR-512（284 MB） |

预设：`fast`（仅锐化）/ `balanced`（默认 2x SPAN）/ `quality`（4x Real-ESRGAN + 全修复 + 人脸）/ `anime`。

## 关键踩坑：色彩保真（放大不该改变颜色）

早期 `quality`（4x + 人脸）后**整体偏色发暗**，根因两处：

1. **白平衡误触发**：旧判据用"全图三通道均值极差"估色偏（阈值 12），把夕阳/绿植/红砖这类**本来就有主色调**的照片误判成偏色而去自动白平衡。修复：只在**本该中性（低饱和）**的像素上估光源色偏，阈值提到 22——正常照片读数普遍 <10，够不到阈值，默认不动色彩；白平衡加护栏（增益限幅 1.30 + 保亮度），真偏色仍能修（钨丝灯 60→12）。

2. **超分模型自带通道偏置**：实测 `SPAN-4x.onnx` 输出 `≈0.958·in + bias`（bias≈R−0.8/G+3.3/B+6.1），整体压暗约 4% 且红降蓝升——"一放大颜色就变了"的根因。修法：**低频对齐**（`enhance.align_low_freq`）——超分只该补高频，整体明暗/色彩应等于输入，把输出低频拉回输入低频即可；对本身干净的 Real-ESRGAN（偏置 <1）近似无操作，不是给 SPAN 写死的魔法数。

修复后 `quality`/`balanced` 通道增益回到 ~1.000（最大偏离 <0.005）。`--keep-color` 可彻底交给用户手控。

## 实测数据

```bash
# 检测 + 擦除
python erase.py -i frame.jpg -o out.png --detect-text                      # 整图文字（去水印）
python erase.py -i frame.jpg -o out.png --detect-text --roi 50,450,1020,180 # 只擦字幕条
python erase.py -i frame.jpg -o out.png --detect-mosaic --mosaic-grid-thr 0.9
python erase.py -i frame.jpg -o out.png --detect-text --detect-mosaic      # 掩码 OR 合并

# 擦除 + 增强 组合
python erase.py -i text.jpg -o erased.png --detect-text --enhance --enhance-preset balanced
python enhance.py -i old.jpg -o out.png --preset quality --keep-color      # 老照片抢救保色
```

| 步骤 | 耗时（CPU） |
|---|---|
| DBNet 文字检测 | 0.2 ~ 0.5 s/帧 |
| 马赛克检测（纯 CV） | 实时（毫秒级） |
| LaMa 擦除 | ~2.1 s/帧 |
| **字幕条全流程** | **≈3 s/帧（1920×1080）** |
| 增强 balanced（2x） | 秒级；quality（4x+人脸）数十秒 |

## 适用边界与取舍

- **适合**：去字幕/水印/标注、隐私打码、视频帧批量清理、擦除后画质增强的完整闭环
- **不适合**：曲形艺术字（掩码复杂擦除易糊）、<12px 小字（DBNet 易漏）、对色彩绝对敏感的出版级场景（需人工校色）
- **取舍**：只用 DBNet 检测分支换速度；需要"识别文字内容"（如敏感词判定）再接识别分支，但延迟显著增加——按需取舍

## 复现要点

- 检测模型：PP-OCRv4 DBNet ONNX（~4.5 MB），增强模型约 1 GB 由 `scripts/fetch_enhance_models.py` 从 **hf-mirror.com** 拉取
- 验证脚本：`scripts/test_color_fidelity.py`（秒级，覆盖误触发/真偏色/护栏/keep-color 四类）
- 环境：Python 3.13 + OpenCV 5.0 + onnxruntime，纯 CPU
