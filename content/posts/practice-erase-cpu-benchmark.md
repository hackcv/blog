---
title: "实践：纯 CPU 图片擦除三模型实测——LaMa / MI-GAN / Telea 的选型与工程细节"
author: "hackcv"
date: 2026-08-23
section: "practice"
subtype: "optimize"
tags: ["AI", "图像擦除", "ONNX Runtime", "LaMa", "MI-GAN", "实践"]
categories: ["研究简报"]
description: "Intel Mac 纯 CPU + ONNX Runtime 实测 LaMa/MI-GAN/Telea：速度恒定特性、crop vs resize 策略、掩码膨胀羽化，以及三档选型矩阵——全部真实测量。"
---

> **一句话结论**：纯 CPU 能做生产级图片擦除。**LaMa 2.1s/张质量最高做终稿、MI-GAN 0.8s 做快速预览、OpenCV Telea <50ms 处理纯色背景**，三者在同一进程内按场景切换。两个关键工程结论：① 推理耗时**几乎不随输入分辨率线性增长**（2.1s/0.8s 恒定）；② **局部裁剪（crop）显著优于整图缩放（resize）**，能保留山体等高频细节。

## 背景与动机

- **场景**：去水印、去杂物、去文字，机器只有 CPU（Intel Mac x86_64，12 核 / 16GB），无 NVIDIA GPU
- **硬约束**：PyTorch 官方从 2.3 起**不再发布 macOS x86_64 wheel**——GPU 路线与 PyTorch 路线都断，唯一可行是 **ONNX Runtime（CPU 推理）**
- **排除项**：扩散模型（SD Inpainting / BrushNet / FLUX）在 CPU 上 30s~数分钟，Intel Mac 不可用，直接排除

## 三模型实测

| 模型 | 来源 | 大小 | 实测耗时 | 特点 | 适用 |
|---|---|---|---|---|---|
| **LaMa** | WACV 2022（IOPaint 默认） | ~198 MB | **2.1 s** | 大掩膜、纹理重建最强 | 通用擦除、建筑/自然纹理、终稿 |
| **MI-GAN** | ICCV 2023（Picsart） | ~27 MB | **0.8 s** | 快、轻，细纹理略糊 | 快速预览、移动端 |
| **Telea/NS** | OpenCV 内置 | 0 MB | **<50 ms** | 扩散插值、简单背景 | 纯色背景、水印 |

**关键观察：耗时不随分辨率线性增长**——LaMa 稳定 2.1s、MI-GAN 稳定 0.8s（在常规尺寸范围内）。因为模型内部对输入做了固定尺寸处理，分辨率变化主要影响预处理而非推理主体。这让"先小图预览、后大图出图"的工作流成本很低。

## 工程细节（决定擦除质量的关键设计）

### 1. 后端抽象 + 自动策略选择

三模型统一抽象为独立后端（`eraser/backends/`：`lama.py` / `migan.py` / `classic.py`），共享同一掩膜输入与后处理管线。`pipeline.py` 的 `_pick_strategy` 按**输入尺寸 + 掩膜大小**自动选择：

- **crop（局部裁剪）**：按掩膜 bounding box 裁出局部区域推理，保留原图高频细节
- **resize（整图缩放）**：整图压到模型输入尺寸，速度快但**山体、织物等高频纹理被压糊**

实测对比：crop 明显优于 resize（细节保留更完整）。

### 2. 大图分块：overlap + ramp 羽化拼接

超长边图片分块推理后拼接（`eraser/tiling.py`）：

- 块大小 `tile` + 相邻块**重叠 `overlap` 像素**（步长 = tile − overlap，末块贴边保证不越界不留缝）
- 重叠区用 `_ramp` 斜坡权重（线形过渡）混合，避免块间接缝——这是"大图擦除看不出分块痕迹"的关键
- 多块掩膜推理结果再经 `_merge_boxes`（按 IOU 合并）统一处理，避免同一物体被拆成多块重复擦

### 3. 掩膜后处理：膨胀 + 羽化

```bash
# 掩膜膨胀 12px（覆盖边缘残留）+ 羽化 5px（柔和过渡）
python erase.py -i photo.jpg -m mask.png -o out.png --model lama --dilate 12 --feather 5
```

- **膨胀**：掩膜必须比实际物体略大，否则擦除边界留残影——`--dilate 12` 是安全值
- **羽化**：硬边界会产生可见接缝，羽化让过渡自然

### 4. 三档切换的总成本 ≈ 0

同一掩膜、同一进程内切换模型：预览用 MI-GAN（0.8s 看构图），满意后 LaMa 出终稿（2.1s），简单水印自动降级 Telea——三档总体验 ≈ 2s。

## 实测数据

```bash
# 环境：Python 3.13 + onnxruntime，模型 models/ 下
python erase.py -i photo.jpg -m mask.png -o out.png --model lama --strategy crop    # 2.1s
python erase.py -i photo.jpg -m mask.png -o out.png --model migan --strategy resize # 0.8s
python erase.py -i photo.jpg -m mask.png -o out.png --model telea --dilate 12 --feather 5 # <50ms
```

| 指标 | LaMa | MI-GAN | Telea |
|---|---|---|---|
| 耗时（1024² 掩膜） | 2.1 s | 0.8 s | 0.05 s |
| 纹理细节保留 | 最高 | 略糊 | 简单背景可用 |
| 大掩膜（>1/4 图） | 优 | 中 | 差 |

## 适用边界

- **适合**：通用物体擦除、水印/字幕、无 GPU 的本地工具链、批量处理
- **不适合**：超大半图掩膜（需语义补全时建议专用模型）；毫秒级批处理场景建议 GPU
- **取舍**：不追扩散模型——CPU 场景下 LaMa 的 2.1s 与扩散的 30s+，质量差距不足以弥补 15 倍等待

## 复现要点

- 模型来源：IOPaint 官方 ONNX 权重（LaMa big_lama_dyn、MI-GAN）
- 线程配置：onnxruntime 默认线程即可，12 核 CPU 下已满负荷；批量处理可开多进程并行
- 参考实现：项目 README 有 smoke/pipeline/benchmark 三组对比图可对照
