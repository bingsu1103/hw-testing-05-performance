#!/usr/bin/env python3
"""Summarize backend and JMeter CPU/RSS samples from a run evidence CSV."""

from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path


def numeric(rows: list[dict[str, str]], key: str) -> list[float]:
    return [float(row[key] or 0) for row in rows]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} METRICS.csv", file=sys.stderr)
        return 64
    path = Path(sys.argv[1])
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        print("Resource metrics file contains no samples", file=sys.stderr)
        return 2

    print("\n## Resource summary\n")
    print("| Process | Samples | Mean CPU | Peak CPU | Mean RSS | Peak RSS |")
    print("|---|---:|---:|---:|---:|---:|")
    for process in ("backend", "jmeter"):
        cpu = numeric(rows, f"{process}_cpu_pct")
        rss = numeric(rows, f"{process}_rss_kb")
        print(
            f"| {process.title()} | {len(rows)} | {statistics.fmean(cpu):.2f}% | "
            f"{max(cpu):.2f}% | {statistics.fmean(rss) / 1024:.2f} MiB | "
            f"{max(rss) / 1024:.2f} MiB |"
        )
    print("\n### RSS stability check\n")
    print("| Process | First 20 samples | Last 20 samples | Change |")
    print("|---|---:|---:|---:|")
    window = min(20, len(rows))
    for process in ("backend", "jmeter"):
        rss = numeric(rows, f"{process}_rss_kb")
        first = statistics.fmean(rss[:window]) / 1024
        last = statistics.fmean(rss[-window:]) / 1024
        print(f"| {process.title()} | {first:.2f} MiB | {last:.2f} MiB | {last - first:+.2f} MiB |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

