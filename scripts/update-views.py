#!/usr/bin/env python3
"""累计统计每篇文章浏览量：解析 nginx access log，增量累加到 data/views.json。

- data/views.json: {"since": "ISO8601", "views": {"/posts/xxx/": 123, ...}}
- 首次运行：解析现有全部日志作为基线
- 之后运行：只解析 since 之后的新日志，增量累加（日志轮转也不丢累计值）

用法：
    python3 scripts/update-views.py            # ssh 拉 qq_claw 日志（本机开发）
    python3 scripts/update-views.py --local   # 直接读本机日志（部署在 qq_claw 时用）
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
OUT_FILE = os.path.join(ROOT, "data", "views.json")

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}

# 日志行: IP - - [23/Aug/2026:23:21:07 +0800] "GET /posts/xxx/ HTTP/1.1" 200 nnn "referer" "UA"
LOG_RE = re.compile(
    r'\[(?P<d>\d{2})/(?P<m>[A-Za-z]{3})/(?P<y>\d{4}):(?P<h>\d{2}):(?P<min>\d{2}):(?P<s>\d{2})'
    r'\s+(?P<tz>[+-]\d{4})\]\s+"GET\s+(?P<path>/\S*)\s+HTTP/\S+"\s+(?P<status>\d{3})'
)


def fetch_logs(local: bool) -> str:
    files = [LOG_NAME, LOG_NAME + ".1"] + [f"{LOG_NAME}.{i}.gz" for i in range(2, 20)]
    if local:
        import gzip
        data = []
        for f in files:
            path = os.path.join(LOG_DIR, f)
            if not os.path.exists(path):
                continue
            try:
                if f.endswith(".gz"):
                    with gzip.open(path, "rb") as fh:
                        data.append(fh.read())
                else:
                    with open(path, "rb") as fh:
                        data.append(fh.read())
            except OSError:
                continue
        return b"".join(data).decode("utf-8", errors="replace")
    cmd = f"cd {LOG_DIR} && zcat -f {' '.join(files)} 2>/dev/null; true"
    out = subprocess.run(
        ["ssh", "-o", "ConnectTimeout=8", "-o", "BatchMode=yes", QQ_CLAW, cmd],
        capture_output=True, text=True, timeout=90,
    )
    return out.stdout


def parse_increment(text: str, since: dt.datetime | None) -> dict:
    """解析日志中 time > since 的 /posts/ 200 请求 → {path: n}"""
    inc: dict = {}
    for m in LOG_RE.finditer(text):
        try:
            tz = m.group("tz")
            tz_off = (int(tz[1:3]) * 60 + int(tz[3:5])) * (-1 if tz[0] == "-" else 1)
            ts = dt.datetime(int(m.group("y")), MONTHS[m.group("m")], int(m.group("d")),
                             int(m.group("h")), int(m.group("min")), int(m.group("s")),
                             tzinfo=dt.timezone(dt.timedelta(minutes=tz_off)))
        except (KeyError, ValueError):
            continue
        if since is not None and ts <= since:
            continue
        if m.group("status") != "200":
            continue
        path = m.group("path")
        if not path.startswith("/posts/"):
            continue
        inc[path] = inc.get(path, 0) + 1
    return inc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", action="store_true", help="直接读本机 nginx 日志（部署机/qq_claw 上使用）")
    args = ap.parse_args()

    # 载入累计数据
    views: dict = {}
    since: dt.datetime | None = None
    if os.path.exists(OUT_FILE):
        try:
            old = json.load(open(OUT_FILE, encoding="utf-8"))
            views = old.get("views", {})
            if old.get("since"):
                since = dt.datetime.fromisoformat(old["since"])
        except (json.JSONDecodeError, ValueError):
            since = None

    print("解析 nginx 日志...")
    text = fetch_logs(args.local)
    inc = parse_increment(text, since)
    for path, n in inc.items():
        views[path] = views.get(path, 0) + n

    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    out = {"since": now, "views": views}
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(f"updated: 增量 {len(inc)} 篇，累计 {len(views)} 篇，总浏览 {sum(views.values())}")
    top = sorted(views.items(), key=lambda kv: kv[1], reverse=True)[:5]
    for p, n in top:
        print(f"  {n:5d}  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
