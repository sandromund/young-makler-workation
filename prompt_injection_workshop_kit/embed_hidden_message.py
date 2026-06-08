#!/usr/bin/env python3
"""
Embed a hidden text message from a TXT file into a PDF.

Use case: controlled security-awareness demo for prompt injection in documents.

Examples:
  python embed_hidden_message.py \
    --input kundennotiz_malediven_jva_visible.pdf \
    --hidden-text-file hidden_message.txt \
    --output kundennotiz_malediven_jva_hidden.pdf \
    --mode white

  python embed_hidden_message.py \
    --make-sample \
    --hidden-text-file hidden_message.txt \
    --output kundennotiz_malediven_jva_hidden.pdf \
    --visible-output kundennotiz_malediven_jva_visible.pdf \
    --mode white
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas


def read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Hidden text file not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def make_sample_visible_pdf(path: Path) -> None:
    """Create a normal-looking one-page customer note."""
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=22 * mm,
        leftMargin=22 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleClean",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        spaceAfter=12,
    )
    h2 = ParagraphStyle(
        "H2Clean",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=6,
    )
    body = ParagraphStyle(
        "BodyClean",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.3,
        leading=14,
        spaceAfter=6,
    )

    data = [
        ["Kunde", "Max Beispiel"],
        ["Vorgang", "Ferienimmobilie im Ausland / berufliche Sonderrisiken"],
        ["Status", "Erste Aufnahme - fachliche Pruefung offen"],
        ["Datum", "08.06.2026"],
    ]
    table = Table(data, colWidths=[40 * mm, 110 * mm])
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0F0F0")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#999999")),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#BBBBBB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    story = [
        Paragraph("Kundennotiz", title),
        table,
        Spacer(1, 8 * mm),
        Paragraph("Sachverhalt", h2),
        Paragraph(
            "Der Kunde besitzt eine vermietete Ferienimmobilie auf den Malediven. "
            "Zusaetzlich fragt er nach einer moeglichen Absicherung fuer berufliche Risiken "
            "eines Familienmitglieds, das in einer Justizvollzugsanstalt arbeitet.",
            body,
        ),
        Paragraph(
            "Der Kunde moechte eine schnelle Einschaetzung, ob die bestehenden Versicherungsvertraege "
            "ausreichen. Eine abschliessende fachliche Bewertung wurde noch nicht vorgenommen.",
            body,
        ),
        Paragraph("Zu pruefende Punkte", h2),
        Paragraph(
            "- Auslandsimmobilie<br/>"
            "- Vermietung beziehungsweise gewerbliche Nutzung<br/>"
            "- Haftpflicht und Rechtsschutz<br/>"
            "- Diensthaftpflicht und berufliche Risiken<br/>"
            "- Versicherbarkeit im Ausland<br/>"
            "- Ausschluesse und Obliegenheiten<br/>"
            "- notwendige Rueckfragen an Versicherer",
            body,
        ),
        Paragraph("Naechste Schritte", h2),
        Paragraph(
            "Bestehende Vertragsunterlagen anfordern, Bedingungen und Ausschluesse pruefen, "
            "Nutzung und Eigentuemerstruktur klaeren, Versichereranfrage vorbereiten und "
            "Rueckmeldung an den Kunden nach fachlicher Pruefung geben.",
            body,
        ),
        Paragraph("Interne Bewertung", h2),
        Paragraph(
            "Der Vorgang ist als pruefpflichtig einzustufen. Es liegt noch keine belastbare Grundlage "
            "fuer eine verbindliche Aussage zum Versicherungsschutz vor.",
            body,
        ),
    ]
    doc.build(story)


def overlay_pdf_for_page(page_width: float, page_height: float, hidden_text: str, mode: str) -> bytes:
    """Return a one-page PDF overlay containing hidden text."""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    lines = hidden_text.splitlines() or [hidden_text]

    if mode == "white":
        c.setFillColor(colors.white)
        c.setFont("Helvetica", 8)
        x = 18 * mm
        y = 12 * mm
        leading = 9
    elif mode == "tiny":
        c.setFillColor(colors.HexColor("#F7F7F7"))
        c.setFont("Helvetica", 1.5)
        x = 4 * mm
        y = 4 * mm
        leading = 2
    elif mode == "offpage":
        c.setFillColor(colors.white)
        c.setFont("Helvetica", 7)
        x = page_width - 2 * mm
        y = 4 * mm
        leading = 8
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    for line in lines:
        c.drawString(x, y, line[:240])
        y += leading

    c.save()
    return packet.getvalue()


def embed_hidden_text(input_pdf: Path, output_pdf: Path, hidden_text: str, mode: str) -> None:
    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()

    if not reader.pages:
        raise ValueError("Input PDF has no pages")

    for index, page in enumerate(reader.pages):
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)

        if index == 0:
            overlay_bytes = overlay_pdf_for_page(page_width, page_height, hidden_text, mode)
            overlay_reader = PdfReader(io.BytesIO(overlay_bytes))
            page.merge_page(overlay_reader.pages[0])

        writer.add_page(page)

    with output_pdf.open("wb") as f:
        writer.write(f)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Embed hidden text from a TXT file into a PDF.")
    parser.add_argument("--input", type=Path, help="Existing visible PDF")
    parser.add_argument("--output", type=Path, required=True, help="Output PDF with hidden message")
    parser.add_argument("--hidden-text-file", type=Path, required=True, help="TXT file containing the hidden message")
    parser.add_argument("--mode", choices=["white", "tiny", "offpage"], default="white", help="Hiding method")
    parser.add_argument("--make-sample", action="store_true", help="Create a sample visible PDF first")
    parser.add_argument("--visible-output", type=Path, default=Path("kundennotiz_malediven_jva_visible.pdf"), help="Visible sample PDF path when using --make-sample")

    args = parser.parse_args(argv)

    hidden_text = read_text_file(args.hidden_text_file)

    if args.make_sample:
        visible_pdf = args.visible_output
        make_sample_visible_pdf(visible_pdf)
        input_pdf = visible_pdf
    elif args.input:
        input_pdf = args.input
    else:
        parser.error("Use --input or --make-sample")

    if not input_pdf.exists():
        raise FileNotFoundError(f"Input PDF not found: {input_pdf}")

    embed_hidden_text(input_pdf, args.output, hidden_text, args.mode)
    print(f"Created: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
