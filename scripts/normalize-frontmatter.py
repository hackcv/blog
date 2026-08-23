#!/usr/bin/env python3
"""规范化 content/posts/*.md 的 front matter：
- author 统一为 "hackcv"（无则补，有则替换）
- 研究简报类（research-brief-*）：categories 统一为 ["研究简报"]，tags 统一基底 + 同义词规范化
- 非简报类：仅补 author，tags/categories 保留
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "content", "posts", "*.md")

BASE_DAILY = ["AI", "大模型", "Agent", "每日简报"]
BASE_WEEKLY = ["AI", "大模型", "Agent", "每周总结"]
SYNONYMS = {
    "人工智能": "AI",
    "LLM": "大模型",
    "音视频": "音视频处理",
    "研究简报": "每日简报",
}


def norm_tags(fm: str, fname: str) -> str:
    m = re.search(r"^tags:\s*\[(.*?)\]", fm, re.M | re.S)
    if not m:
        return fm
    tags = [t.strip().strip('"\'') for t in m.group(1).split(",") if t.strip()]
    tags = [SYNONYMS.get(t, t) for t in tags]
    base = BASE_WEEKLY if "week" in fname else BASE_DAILY
    seen, out = set(), []
    for t in base + tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return re.sub(
        r"^tags:.*$",
        "tags: " + json.dumps(out, ensure_ascii=False),
        fm,
        flags=re.M,
    )


def main() -> int:
    changed = 0
    for path in sorted(glob.glob(POSTS)):
        fname = os.path.basename(path)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            print(f"skip (no front matter): {fname}")
            continue
        fm, body = m.group(1), text[m.end():]
        orig = fm

        # author 统一
        if re.search(r"^author:", fm, re.M):
            fm = re.sub(r'^author:.*$', 'author: "hackcv"', fm, flags=re.M)
        else:
            fm = re.sub(
                r"^(title:.*)$", r'\1\nauthor: "hackcv"', fm, count=1, flags=re.M
            )

        is_brief = "research-brief" in fname
        if is_brief:
            fm = re.sub(
                r'^categories:.*$', 'categories: ["研究简报"]', fm, flags=re.M
            )
            fm = norm_tags(fm, fname)

        if fm != orig:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(f"---\n{fm}\n---\n{body}")
            changed += 1
    print(f"normalized {changed}/{len(glob.glob(POSTS))} posts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
