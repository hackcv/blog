---
title: "Practice: Text & Mosaic Auto-Erase + Enhancement — a Full Image Pipeline on CPU"
author: "hackcv"
date: 2026-08-23
section: "practice"
subtype: "verify"
tags: ["AI", "OCR", "Image Inpainting", "PP-OCRv4", "Mosaic Detection", "Practice"]
categories: ["Research Brief"]
description: "PP-OCRv4 DBNet text detection + pure-CV mosaic detection + multi-source mask OR-merging + LaMa inpainting, then an optional analyze→repair→upscale→refine four-stage enhancer — all CPU; includes real color-fidelity debugging notes."
---

> **One-line takeaway**: An end-to-end CPU-only image pipeline — **PP-OCRv4 DBNet locates text (0.2–0.5s) + pure-CV mosaic detection (real-time) + OR-merged masks into LaMa inpainting (2.1s)**, then optionally a four-stage enhancer (analyze → repair → upscale → refine). Measured: subtitle-bar workflow ≈ **3s/frame at 1920×1080**.

## Background & Motivation

- **Scenario**: batch-remove subtitles/watermarks/annotations, de-pixelation of privacy mosaics, old-photo rescue
- **Pain**: full OCR (with recognition branch) is big and slow; mosaic detection is usually a trained model; and post-erase quality often needs enhancement — **no complete CPU-only loop existed**
- **Constraint**: same ONNX Runtime CPU route as the benchmark article

## Core Approach (Three Layers)

### Layer 1: Detection (auto-generating masks)

**Text detection (PP-OCRv4 DBNet)**:
- Detection branch only (DB text detection), no recognition — model ~4.5 MB, 0.2–0.5s on CPU
- Text polygons → binary mask → dilate per box to cover stroke edges

**Mosaic detection (pure CV, zero models)**:
- Uses the visual signature of mosaics: **block-grid + missing local high-frequency** — grid-gradient consistency decides
- `--mosaic-grid-thr` controls strictness (0.7–0.9 is safe for most images; 0.9 for face censor)
- Real-time (milliseconds), no model loading

### Layer 2: Mask merge + inpainting

- Multi-source masks (text + mosaic + manual) **OR-merged** into one total mask
- Unified `--dilate + --feather`, then LaMa (model selection in the benchmark article)
- `--roi x,y,w,h` restricts detection — erase only the subtitle bar, avoid touching the subject

**Detection params (real values)**: DBNet inference threshold `thresh=0.2`, box filter `box_thresh=0.35`, `unclip_ratio=1.8` — the 1.8× outward expansion of text boxes is exactly what covers stroke-edge residue, the key to clean text removal.

### Layer 3 (optional): four-stage enhancer

Post-erase, `enhance.py` runs **analyze → repair → upscale → refine** (all ONNX Runtime CPU):

| Stage | What | Key models (CPU-verified) |
|---|---|---|
| Analyze | NIMA quality score + photo/anime classification | NIMA mobilenet |
| Repair | De-JPEG / denoise / de-blur | 1xDeJPG/1xDeNoise (PLKSR), 1x-hurrdeblur (0.18 MB, very fast) |
| Upscale | 2x/4x super-resolution | SPAN-4x (1.7 MB fastest), Real-ESRGAN general-fast (5 MB, solid detail), Real-CUGAN (anime) |
| Refine | Face restoration | YOLOv8n-face 5-keypoints → GPEN-BFR-512 (284 MB) |

Presets: `fast` (sharpen only) / `balanced` (default 2x SPAN) / `quality` (4x Real-ESRGAN + full repair + faces) / `anime`.

## Key Debugging Note: Color Fidelity (upscaling must not change color)

Early `quality` (4x + faces) output was **dark and color-shifted**. Two root causes, both fixed:

1. **White-balance false triggers**: the old criterion estimated color cast from full-image channel-mean spread (threshold 12), misjudging sunsets/greenery/red brick — images with legitimate dominant tints — as cast and auto-white-balancing them. Fix: estimate light-source cast only on **pixels that should be neutral** (low saturation), threshold raised to 22 — normal photos read <10, never trip it; WB gains clamped (`max_gain=1.30` + luminance preservation) so real casts still get fixed (tungsten 60→12).

2. **Upscaler channel bias**: measured `SPAN-4x.onnx` output ≈ `0.958·in + bias` (bias≈R−0.8/G+3.3/B+6.1) — darkens ~4% overall and shifts red down/blue up; that's the "colors change the moment you upscale." Fix: generic **low-frequency alignment** (`enhance.align_low_freq`) — an upscaler should only add high frequency; overall tone/color should equal the input, so pull the output's low frequency back to the input's. Near no-op for clean Real-ESRGAN/Real-CUGAN (bias <1) — not a magic constant for SPAN.

After the fix, `quality`/`balanced` channel gains return to ~1.000 (max deviation <0.005). `--keep-color` hands full control to the user (Web UI: "keep original color" checkbox, on by default).

## Measured Data

```bash
# Detect + inpaint
python erase.py -i frame.jpg -o out.png --detect-text                      # whole-image text (watermark)
python erase.py -i frame.jpg -o out.png --detect-text --roi 50,450,1020,180 # subtitle bar only
python erase.py -i frame.jpg -o out.png --detect-mosaic --mosaic-grid-thr 0.9
python erase.py -i frame.jpg -o out.png --detect-text --detect-mosaic      # OR-merged masks

# Erase + enhance combo
python erase.py -i text.jpg -o erased.png --detect-text --enhance --enhance-preset balanced
python enhance.py -i old.jpg -o out.png --preset quality --keep-color      # old-photo rescue, keep color
```

| Step | Time (CPU) |
|---|---|
| DBNet text detection | 0.2 ~ 0.5 s/frame |
| Mosaic detection (pure CV) | real-time (ms) |
| LaMa inpainting | ~2.1 s/frame |
| **Subtitle-bar full workflow** | **≈3 s/frame (1920×1080)** |
| Enhance balanced (2x) | seconds; quality (4x+faces) tens of seconds |

## Scope & Trade-offs

- **Fits**: subtitle/watermark removal, privacy mosaics, video-frame batch cleanup, full erase-then-enhance loops
- **Doesn't fit**: curved artistic text (complex masks blur when inpainting), <12px tiny text (DBNet misses), publication-grade color-critical work (manual color grading needed)
- **Trade-off**: detection-only DBNet trades recognition for speed; if you need "what does the text say" (e.g., sensitive-word gating), add the recognition branch — but latency rises significantly. Pick per need

## Reproduction Notes

- Detection model: PP-OCRv4 DBNet ONNX (~4.5 MB); enhancer models ≈1 GB, fetched by `scripts/fetch_enhance_models.py` from **hf-mirror.com**
- Verification: `scripts/test_color_fidelity.py` (seconds; covers false-trigger/true-cast/clamp/keep-color)
- Environment: Python 3.13 + OpenCV 5.0 + onnxruntime, pure CPU
