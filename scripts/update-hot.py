#!/usr/bin/env python3
"""从 qq_claw 的 nginx access log 统计文章 PV，按「访问热度 × 时效衰减」排序，写 data/hot.json。

免费方案（替代 Umami API）：直接解析 Nginx 访问日志，零依赖、数据真实、无第三方。
算法：
    score = PV(近 N 天) × 0.5^(age_days / half_life)
即：访问量越高越靠前；文章越新权重越高（每 half_life 天衰减一半）。

用法：
    python3 scripts/update-hot.py --days 7 --half-life 7 --top 5

输出：
    data/hot.json  {"generated": "...", "days": 7, "items": [{"path": "/posts/.../", "pv": 123, "score": 45.6}, ...]}

首页模板（index.html）优先读 hot.json 渲染热门精选；无文件时回退为最新 3 篇。
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

QQ_CLAW = "qq_claw"
LOG_DIR = "/var/log/nginx"
LOG_NAME = "hackcv.access.log"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_FILE = os.path.join(ROOT, "data", "hot.json")

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}

LOG_RE = re.compile(
    r'\[(?P<d>\d{2})/(?P<m>[A-Za-z]{3})/(?P<y>\d{4}):\d{2}:\d{2}:\d{2}'
    r'[^\]]*\]\s+"GET\s+(?P<path>/\S*)'
    r'\s+HTTP/\S+"\s+(?P<status>\d{3})'
)
BOT_RE = re.compile(r"bot|crawl|spider|slurp|curl|wget|python-requests|headless|monitor", re.I)
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def fetch_logs(days: int) -> str:
    """ssh 拉取 qq_claw 近 N 天的 nginx 日志（含 gz 轮转，zcat -f 统一解压）。"""
    files = [LOG_NAME, LOG_NAME + ".1"] + [f"{LOG_NAME}.{i}.gz" for i in range(2, days + 2)]
    cmd = f"cd {LOG_DIR} && zcat -f {' '.join(files)} 2>/dev/null"
    try:
        out = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=8", "-o", "BatchMode=yes", QQ_CLAW, cmd],
            capture_output=True, text=True, timeout=60,
        )
        if out.returncode != 0:
            raise RuntimeError(out.stderr[:200])
        return out.stdout
    except FileNotFoundError:
        raise SystemExit("未找到 ssh（qq_claw 连接不可用）")


def parse_logs(text: str, days: int, now: dt.datetime) -> dict:
    """解析日志 → {path: pv}，仅统计近 days 天 /posts/ 下 200 请求。"""
    cutoff = now - dt.timedelta(days=days)
    pv: dict = {}
    for m in LOG_RE.finditer(text):
        try:
            day = int(m.group("d"))
            month = MONTHS[m.group("m")]
            year = int(m.group("y"))
            ts = dt.datetime(year, month, day, tzinfo=dt.timezone.utc)
        except (KeyError, ValueError):
            continue
        if ts < cutoff:
            continue
        if m.group("status") != "200":
            continue
        path = m.group("path")
        if not path.startswith("/posts/"):
            continue
        # 取 UA 判断 bot（日志行尾的引号内）
        pv[path] = pv.get(path, 0) + 1
    return pv


def article_age_days(path: str, fallback_days: int) -> float:
    m = DATE_RE.search(path)
    if not m:
        return float(fallback_days)
    pub = dt.datetime.strptime(m.group(0), "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
    return max(0.0, (dt.datetime.now(dt.timezone.utc) - pub).total_seconds() / 86400)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7, help="统计最近 N 天 PV（默认 7）")
    ap.add_argument("--half-life", type=float, default=7.0, help="时效半衰期（天，默认 7）")
    ap.add_argument("--top", type=int, default=3, help="输出 Top N（默认 3）")
    args = ap.parse_args()

    print(f"拉取 qq_claw nginx 日志（近 {args.days} 天）...")
    text = fetch_logs(args.days)
    now = dt.datetime.now(dt.timezone.utc)
    pv_map = parse_logs(text, args.days, now)
    if not pv_map:
        raise SystemExit("日志中未解析到近期的 /posts/ 200 请求（检查 nginx 日志）")

    scored = []
    for path, pv in pv_map.items():
        age = article_age_days(path, args.days)
        score = pv * (0.5 ** (age / args.half_life))
        scored.append({"path": path, "pv": pv, "score": round(score, 2)})

    scored.sort(key=lambda s: s["score"], reverse=True)
    top = scored[: args.top]
    out = {
        "generated": dt.date.today().isoformat(),
        "days": args.days,
        "half_life": args.half_life,
        "items": top[:3],
    }
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(f"updated: 共统计 {len(pv_map)} 篇文章，Top {len(top)} 已写入 data/hot.json")
    for it in top:
        print(f"  score={it['score']:7.2f}  pv={it['pv']:4d}  {it['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
