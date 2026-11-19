#!/usr/bin/env python3
"""Build the HW05 performance report PDF from the measured Markdown report."""

from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "23120205_HW05_Performance_Report.pdf"
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`(.+?)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r"<link href='\2' color='#23628d'>\1</link>",
        text,
    )
    return text


def parse_table(lines: list[str], start: int, styles: dict[str, ParagraphStyle]):
    raw = []
    index = start
    while index < len(lines) and lines[index].strip().startswith("|"):
        raw.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
        index += 1
    if len(raw) >= 2 and all(set(cell) <= {"-", ":"} for cell in raw[1]):
        raw.pop(1)
    data = []
    for row_index, row in enumerate(raw):
        style = styles["TableHeader"] if row_index == 0 else styles["TableCell"]
        data.append([Paragraph(inline(cell), style) for cell in row])
    width = 176 * mm
    columns = max(len(row) for row in data)
    table = Table(data, colWidths=[width / columns] * columns, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173b57")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#aebdca")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f6f9")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table, index


def header_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#52697d"))
    canvas.drawString(18 * mm, 10 * mm, "Ngô Gia An - 23120205 | HW05 Performance Testing")
    canvas.drawRightString(192 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def main() -> int:
    pdfmetrics.registerFont(TTFont("Arial", ARIAL))
    pdfmetrics.registerFont(TTFont("Arial-Bold", ARIAL_BOLD))
    base = getSampleStyleSheet()
    styles = {
        "Title": ParagraphStyle(
            "Title", parent=base["Title"], fontName="Arial-Bold", fontSize=22,
            leading=27, textColor=colors.HexColor("#12344d"), spaceAfter=12,
        ),
        "H1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontName="Arial-Bold", fontSize=15,
            leading=19, textColor=colors.HexColor("#12344d"), spaceBefore=10, spaceAfter=7,
        ),
        "H2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="Arial-Bold", fontSize=12,
            leading=15, textColor=colors.HexColor("#23628d"), spaceBefore=8, spaceAfter=5,
        ),
        "Body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Arial", fontSize=9.5,
            leading=13.5, textColor=colors.HexColor("#233746"), spaceAfter=6,
        ),
        "Bullet": ParagraphStyle(
            "Bullet", parent=base["BodyText"], fontName="Arial", fontSize=9.5,
            leading=13, leftIndent=12, firstLineIndent=-8, spaceAfter=3,
        ),
        "Note": ParagraphStyle(
            "Note", parent=base["BodyText"], fontName="Arial", fontSize=9,
            leading=13, leftIndent=8, rightIndent=8, borderColor=colors.HexColor("#f0b44d"),
            borderWidth=1, borderPadding=7, backColor=colors.HexColor("#fff8e7"), spaceAfter=8,
        ),
        "TableCell": ParagraphStyle(
            "TableCell", parent=base["BodyText"], fontName="Arial", fontSize=7.5,
            leading=9.5, textColor=colors.HexColor("#233746"),
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader", parent=base["BodyText"], fontName="Arial-Bold", fontSize=7.5,
            leading=9.5, textColor=colors.white,
        ),
        "Caption": ParagraphStyle(
            "Caption", parent=base["BodyText"], fontName="Arial", fontSize=8,
            leading=10, alignment=TA_CENTER, textColor=colors.HexColor("#52697d"), spaceAfter=8,
        ),
    }

    lines = (ROOT / "docs" / "REPORT.md").read_text(encoding="utf-8").splitlines()
    story = []
    index = 0
    inserted_figures = False
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("| "):
            table, index = parse_table(lines, index, styles)
            story.extend([table, Spacer(1, 5 * mm)])
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["Title"]))
        elif line.startswith("## "):
            heading = line[3:]
            if heading.startswith("6. Load") and not inserted_figures:
                story.append(PageBreak())
                story.append(Paragraph("Measured scenario evidence", styles["H1"]))
                for scenario in ("Load", "Stress", "Spike", "Soak"):
                    path = ROOT / "evidence" / "screenshots" / f"23120205_{scenario}_20261119_evidence.png"
                    story.append(KeepTogether([
                        Image(str(path), width=176 * mm, height=110 * mm),
                        Paragraph(f"Figure: {scenario} raw-JTL/resource summary.", styles["Caption"]),
                    ]))
                story.append(PageBreak())
                inserted_figures = True
            story.append(Paragraph(inline(heading), styles["H1"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), styles["H2"]))
        elif line.startswith("> "):
            story.append(Paragraph(inline(line[2:]), styles["Note"]))
        elif re.match(r"^\d+\. ", line):
            story.append(Paragraph(inline(line), styles["Bullet"], bulletText="•"))
        elif line.startswith("- "):
            story.append(Paragraph(inline(line[2:]), styles["Bullet"], bulletText="•"))
        else:
            story.append(Paragraph(inline(line), styles["Body"]))
        index += 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=17 * mm, leftMargin=17 * mm,
        topMargin=16 * mm, bottomMargin=17 * mm, title="HW05 Performance Testing Report",
        author="Ngô Gia An - 23120205",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
