---
title: "Practice: CPU-Only Image Inpainting — Three Models Benchmarked: LaMa / MI-GAN / Telea Selection and Engineering Details"
author: "hackcv"
date: 2026-08-23
section: "practice"
subtype: "optimize"
tags: ["AI", "Image Inpainting", "ONNX Runtime", "LaMa", "MI-GAN", "Practice"]
categories: ["Research Brief"]
description: "Real measurements on an Intel Mac with pure CPU + ONNX Runtime: LaMa/MI-GAN/Telea speed characteristics, crop-vs-resize strategy, mask dilation/feathering, and a three-tier selection matrix."
---

> **One-line takeaway**: Production-grade image inpainting works without a GPU. **LaMa at 2.1s/image for final output, MI-GAN at 0.8s for quick preview, OpenCV Telea under 50ms for flat backgrounds**, all switchable in one process. Two key engineering findings: ① inference time is **roughly independent of input resolution** (2.1s/0.8s constant); ② **local cropping (crop) clearly beats whole-image resizing (resize)** — preserving high-frequency details like mountains.

## Background & Motivation

- **Scenario**: remove watermarks, objects, text on a CPU-only machine (Intel Mac x86_64, 12 cores / 16GB), no NVIDIA GPU
- **Hard constraint**: PyTorch stopped shipping **macOS x86_64 wheels at 2.3** — both GPU and PyTorch routes are dead; the only viable path is **ONNX Runtime (CPU inference)**
- **Excluded**: diffusion models (SD Inpainting / BrushNet / FLUX) take 30s–minutes on CPU — unusable on Intel Mac, ruled out

## Three-Model Benchmarks

| Model | Source | Size | Measured time | Character | Best for |
|---|---|---|---|---|---|
| **LaMa** | WACV 2022 (IOPaint default) | ~198 MB | **2.1 s** | Strongest with large masks & textures | General inpainting, architecture/nature textures, final output |
| **MI-GAN** | ICCV 2023 (Picsart) | ~27 MB | **0.8 s** | Fast, light; slightly soft on fine texture | Quick preview, mobile |
| **Telea/NS** | OpenCV built-in | 0 MB | **<50 ms** | Diffusion interpolation, simple backgrounds | Flat backgrounds, watermarks |

**Key observation: time does not scale linearly with resolution** — LaMa stays at 2.1s, MI-GAN at 0.8s within normal sizes. The model internally normalizes the input; resolution mainly affects preprocessing, not the inference core. So "small preview first, full-size output later" costs almost nothing.

## Engineering Details (Three Things That Decide Quality)

### 1. Backend abstraction + automatic strategy selection

The three models are unified as separate backends (`eraser/backends/`: `lama.py` / `migan.py` / `classic.py`) sharing the same mask input and post-processing. `_pick_strategy` in `pipeline.py` chooses automatically from **input size + mask extent**:

- **crop (local crop)**: crop the region around the mask bounding box and infer locally — preserves original high-frequency detail
- **resize (whole-image)**: squeeze the full image to model input size — faster, but **mountains, fabric and other high-frequency texture get smeared**

Measured: crop is clearly better (more detail retained).

### 2. Large-image tiling: overlap + ramp feathering

Very long images are tiled and stitched (`eraser/tiling.py`):

- Tile size `tile` + **`overlap` pixels** between neighbors (step = tile − overlap; last tile edge-aligned so nothing is missed or gapped)
- Overlap zones are blended with a `_ramp` linear-weight ramp — this is what makes "no visible tile seams on big images"
- Multi-box masks are merged via `_merge_boxes` (IoU-based) to avoid re-erasing the same object across tiles

### 3. Mask post-processing: dilation + feathering

```bash
# Dilate mask 12px (cover edge residue) + feather 5px (soft transition)
python erase.py -i photo.jpg -m mask.png -o out.png --model lama --dilate 12 --feather 5
```

- **Dilation**: the mask must be slightly larger than the object, or edges leave ghosting — `--dilate 12` is a safe value
- **Feathering**: hard mask edges create visible seams; feathering softens the transition

### 4. Three-tier switching costs ≈ 0

Same mask, same process, switch models: preview with MI-GAN (0.8s to check composition), final with LaMa (2.1s), auto-degrade to Telea for simple watermarks — the whole three-tier experience is ≈ 2s.

## Measured Data

```bash
# Environment: Python 3.13 + onnxruntime, models under models/
python erase.py -i photo.jpg -m mask.png -o out.png --model lama --strategy crop    # 2.1s
python erase.py -i photo.jpg -m mask.png -o out.png --model migan --strategy resize # 0.8s
python erase.py -i photo.jpg -m mask.png -o out.png --model telea --dilate 12 --feather 5 # <50ms
```

| Metric | LaMa | MI-GAN | Telea |
|---|---|---|---|
| Time (1024² mask) | 2.1 s | 0.8 s | 0.05 s |
| Texture detail | Highest | Slightly soft | Flat backgrounds only |
| Large masks (>1/4 image) | Good | Fair | Poor |

## Scope

- **Fits**: general object removal, watermarks/subtitles, GPU-less local toolchains, batch processing
- **Doesn't fit**: >half-image masks (use specialized models for semantic completion); millisecond-latency batch workloads (get a GPU)
- **Trade-off**: skip diffusion — on CPU, LaMa's 2.1s vs diffusion's 30s+ isn't worth 15× the wait for the quality gap

## Reproduction Notes

- Model source: IOPaint official ONNX weights (LaMa big_lama_dyn, MI-GAN)
- Threads: onnxruntime defaults are fine on 12 cores; use multi-process parallelism for batches
- Reference: the project README ships smoke/pipeline/benchmark comparison images to check against
