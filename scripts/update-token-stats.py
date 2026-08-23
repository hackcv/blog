#!/usr/bin/env python3
"""扫描 content/posts/*.md 中的 Token 消耗统计，汇总写入 data/token-stats.json。

用法（每次发布新简报后执行，或接入简报生成流程末尾）：
    python3 scripts/update-token-stats.py

输出：
    data/token-stats.json  {"total": 1921500, "count": 30, "avg": 64050, "updated": "2026-08-23", ...}

about 页（layouts/_default/about.html）优先读取该文件展示累计/平均 Token 消耗；
文件缺失或为空时回退为构建时全站扫描正文。
"""
import datetime
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_GLOB = os.path.join(ROOT, "content", "posts", "*.md")
OUT_FILE = os.path.join(ROOT, "data", "token-stats.json")

# 兼容两种写法：'总消耗约 78,000 tokens' 与 '总消耗约 42k tokens'
TOKEN_RE = re.compile(r"总消耗约 ([\d,]+k?) tokens")


def parse_token(text: str) -> int:
    m = TOKEN_RE.search(text)
    if not m:
        return 0
    num = m.group(1)
    if num.endswith("k"):
        return int(num[:-1].replace(",", "")) * 1000
    return int(num.replace(",", ""))


def main() -> int:
    total, count = 0, 0
    for f in sorted(glob.glob(POSTS_GLOB)):
        with open(f, encoding="utf-8") as fh:
            v = parse_token(fh.read())
        if v:
            total += v
            count += 1

    stats = {
        "total": total,
        "count": count,
        "avg": total // count if count else 0,
        "updated": datetime.date.today().isoformat(),
        "note": "自动生成：scripts/update-token-stats.py，请勿手改",
    }
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, ensure_ascii=False, indent=2)
    print(f"updated: total={total:,} tokens / count={count} / avg={stats['avg']:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
