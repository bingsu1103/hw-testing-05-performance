#!/usr/bin/env python3
"""Render honest scenario evidence summaries from raw JTL and resource CSV files."""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def load_analyzer():
    path = ROOT / "scripts" / "analyze_jtl.py"
    spec = importlib.util.spec_from_file_location("hw05_analyze_jtl", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def line_chart(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], series: list[tuple[str, list[float]]], title: str) -> None:
    x0, y0, x1, y1 = box
    draw.text((x0, y0 - 42), title, font=font(24, True), fill="#18324a")
    draw.rectangle(box, outline="#b8c7d4", width=2)
    values = [value for _, points in series for value in points]
    maximum = max(values) if values else 1
    maximum = maximum or 1
    colors = ["#1565c0", "#ef6c00"]
    for index, (name, points) in enumerate(series):
        if len(points) < 2:
            continue
        coords = []
        for i, value in enumerate(points):
            x = x0 + 12 + (x1 - x0 - 24) * i / (len(points) - 1)
            y = y1 - 12 - (y1 - y0 - 24) * value / maximum
            coords.append((x, y))
        draw.line(coords, fill=colors[index], width=3)
        draw.text((x0 + 18 + index * 360, y0 + 12), f"{name} (max {max(points):.1f})", font=font(18, True), fill=colors[index])
    draw.text((x1 - 165, y1 - 30), f"scale max {maximum:.1f}", font=font(14), fill="#52697d")


def bars(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], values: list[tuple[str, int]], title: str) -> None:
    x0, y0, x1, y1 = box
    draw.text((x0, y0 - 42), title, font=font(24, True), fill="#18324a")
    maximum = max(value for _, value in values) or 1
    row_height = (y1 - y0) / len(values)
    for index, (label, value) in enumerate(values):
        top = y0 + index * row_height + 8
        bottom = top + row_height - 16
        bar_start = x0 + 310
        bar_end = bar_start + (x1 - bar_start - 85) * value / maximum
        draw.text((x0, top + 5), label[:29], font=font(17), fill="#263746")
        draw.rounded_rectangle((bar_start, top, bar_end, bottom), radius=8, fill="#2e7d32")
        draw.text((bar_end + 10, top + 5), f"{value} ms", font=font(17, True), fill="#1b5e20")


def render(scenario: str) -> Path:
    analyzer = load_analyzer()
    stem = f"23120205_{scenario}_20261119"
    overall, labels = analyzer.analyze(ROOT / "results" / f"{stem}.jtl")
    with (ROOT / "evidence" / "resource-metrics" / f"{stem}.csv").open(newline="", encoding="utf-8") as stream:
        resource_rows = list(csv.DictReader(stream))

    image = Image.new("RGB", (1600, 1000), "#f4f7fa")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1600, 125), fill="#12344d")
    draw.text((55, 30), f"HW05 {scenario} - measured evidence", font=font(40, True), fill="white")
    draw.text((55, 82), "Ngô Gia An - 23120205 | 2026-11-17 ICT | raw JTL + 2-second process samples", font=font(20), fill="#d6e6f2")

    cards = [
        ("Samples", f"{overall.samples:,}"),
        ("Errors", f"{overall.errors} ({overall.error_rate_pct:.2f}%)"),
        ("Throughput", f"{overall.throughput_rps:.2f} req/s"),
        ("p95 / p99", f"{overall.p95_ms} / {overall.p99_ms} ms"),
        ("Max", f"{overall.max_ms} ms"),
    ]
    for i, (label, value) in enumerate(cards):
        left = 45 + i * 310
        draw.rounded_rectangle((left, 155, left + 285, 270), radius=16, fill="white", outline="#d0dce6", width=2)
        draw.text((left + 20, 175), label, font=font(18, True), fill="#5b7184")
        draw.text((left + 20, 215), value, font=font(29, True), fill="#12344d")

    p95_values = [(label, metric.p95_ms) for label, metric in labels.items()]
    bars(draw, (55, 340, 775, 700), p95_values, "p95 latency by request label")

    backend_cpu = [float(row["backend_cpu_pct"] or 0) for row in resource_rows]
    jmeter_cpu = [float(row["jmeter_cpu_pct"] or 0) for row in resource_rows]
    line_chart(draw, (840, 340, 1545, 590), [("Backend CPU %", backend_cpu), ("JMeter CPU %", jmeter_cpu)], "CPU samples")
    backend_rss = [float(row["backend_rss_kb"] or 0) / 1024 for row in resource_rows]
    jmeter_rss = [float(row["jmeter_rss_kb"] or 0) / 1024 for row in resource_rows]
    line_chart(draw, (840, 695, 1545, 945), [("Backend RSS MiB", backend_rss), ("JMeter RSS MiB", jmeter_rss)], "Memory samples")

    draw.text((55, 750), "Integrity notes", font=font(24, True), fill="#18324a")
    notes = [
        "• Percentiles: nearest-rank over unmodified JTL elapsed values.",
        "• Resource data: ps samples collected every 2 seconds during this same run.",
        "• HTML report and raw JTL are preserved under reports/ and results/.",
        "• This image is a rendered evidence summary, not an Activity Monitor screenshot.",
    ]
    for i, note in enumerate(notes):
        draw.text((55, 795 + i * 34), note, font=font(18), fill="#344b5e")

    output = ROOT / "evidence" / "screenshots" / f"{stem}_evidence.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    return output


def main() -> int:
    scenarios = sys.argv[1:] or ["Load", "Stress", "Spike", "Soak"]
    for scenario in scenarios:
        print(render(scenario))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

