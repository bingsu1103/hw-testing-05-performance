#!/usr/bin/env python3
"""Analyze a JMeter CSV JTL and optionally enforce performance gates."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Metrics:
    samples: int
    errors: int
    error_rate_pct: float
    min_ms: int
    mean_ms: float
    p50_ms: int
    p90_ms: int
    p95_ms: int
    p99_ms: int
    max_ms: int
    throughput_rps: float


def percentile(values: list[int], percentile_value: float) -> int:
    """Return nearest-rank percentile, matching an auditable spreadsheet formula."""
    if not values:
        raise ValueError("Cannot calculate a percentile without samples")
    ordered = sorted(values)
    rank = max(1, math.ceil((percentile_value / 100.0) * len(ordered)))
    return ordered[rank - 1]


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"timeStamp", "elapsed", "label", "success"}
        fields = set(reader.fieldnames or [])
        missing = required - fields
        if missing:
            raise ValueError(f"Missing JTL columns: {', '.join(sorted(missing))}")
        rows = list(reader)
    if not rows:
        raise ValueError("JTL contains a header but no samples")
    return rows


def calculate(rows: list[dict[str, str]]) -> Metrics:
    elapsed = [int(row["elapsed"]) for row in rows]
    errors = sum(row["success"].strip().lower() != "true" for row in rows)
    starts = [int(row["timeStamp"]) for row in rows]
    ends = [start + duration for start, duration in zip(starts, elapsed)]
    wall_seconds = max((max(ends) - min(starts)) / 1000.0, 0.001)
    return Metrics(
        samples=len(rows),
        errors=errors,
        error_rate_pct=(errors / len(rows)) * 100.0,
        min_ms=min(elapsed),
        mean_ms=statistics.fmean(elapsed),
        p50_ms=percentile(elapsed, 50),
        p90_ms=percentile(elapsed, 90),
        p95_ms=percentile(elapsed, 95),
        p99_ms=percentile(elapsed, 99),
        max_ms=max(elapsed),
        throughput_rps=len(rows) / wall_seconds,
    )


def analyze(path: Path) -> tuple[Metrics, dict[str, Metrics]]:
    rows = load_rows(path)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["label"]].append(row)
    return calculate(rows), {label: calculate(items) for label, items in sorted(grouped.items())}


def markdown(path: Path, overall: Metrics, labels: dict[str, Metrics]) -> str:
    lines = [
        f"# JTL analysis: {path.name}",
        "",
        "Percentiles use the nearest-rank method over the unmodified `elapsed` column.",
        "",
        "| Scope | Samples | Errors | Error rate | Mean | p50 | p90 | p95 | p99 | Max | Throughput |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    def row(name: str, value: Metrics) -> str:
        return (
            f"| {name} | {value.samples} | {value.errors} | {value.error_rate_pct:.2f}% | "
            f"{value.mean_ms:.2f} ms | {value.p50_ms} ms | {value.p90_ms} ms | "
            f"{value.p95_ms} ms | {value.p99_ms} ms | {value.max_ms} ms | "
            f"{value.throughput_rps:.2f} req/s |"
        )

    lines.append(row("Overall", overall))
    lines.extend(row(label.replace("|", "\\|"), value) for label, value in labels.items())
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jtl", type=Path, help="JMeter CSV JTL file")
    parser.add_argument("--baseline", type=Path, help="Baseline JTL for overall p95 comparison")
    parser.add_argument("--max-p95-ms", type=float, help="Fail when overall p95 exceeds this value")
    parser.add_argument("--max-error-rate", type=float, help="Fail when error rate percent exceeds this value")
    parser.add_argument(
        "--max-p95-regression-pct",
        type=float,
        help="Fail when p95 regression versus --baseline exceeds this percentage",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        overall, labels = analyze(args.jtl)
    except (OSError, ValueError, csv.Error) as error:
        print(f"JTL analysis failed: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(
            json.dumps(
                {"file": str(args.jtl), "overall": asdict(overall), "labels": {k: asdict(v) for k, v in labels.items()}},
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(markdown(args.jtl, overall, labels), end="")

    failures: list[str] = []
    if args.max_p95_ms is not None and overall.p95_ms > args.max_p95_ms:
        failures.append(f"p95 {overall.p95_ms} ms > {args.max_p95_ms:g} ms")
    if args.max_error_rate is not None and overall.error_rate_pct > args.max_error_rate:
        failures.append(f"error rate {overall.error_rate_pct:.2f}% > {args.max_error_rate:g}%")
    if args.max_p95_regression_pct is not None:
        if args.baseline is None:
            failures.append("--max-p95-regression-pct requires --baseline")
        else:
            try:
                baseline, _ = analyze(args.baseline)
                regression = ((overall.p95_ms - baseline.p95_ms) / baseline.p95_ms) * 100.0
                if regression > args.max_p95_regression_pct:
                    failures.append(
                        f"p95 regression {regression:.2f}% > {args.max_p95_regression_pct:g}% "
                        f"(baseline {baseline.p95_ms} ms)"
                    )
            except (OSError, ValueError, csv.Error) as error:
                failures.append(f"baseline analysis failed: {error}")

    if failures:
        print("Performance gate failed: " + "; ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

