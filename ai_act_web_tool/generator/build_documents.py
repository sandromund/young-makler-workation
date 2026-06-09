from __future__ import annotations

from pathlib import Path
from typing import Any

from .docx_utils import (
    add_bullet_list,
    add_disclaimer,
    add_key_value_table,
    add_metadata_table,
    add_section,
    create_document,
    format_answer_value,
    save_document,
)
from .mappings import DOCUMENT_CONFIG


def build_document(
    filename: str,
    raw_json: dict[str, Any],
    answers: dict[str, str],
    output_dir: Path,
) -> Path:
    config = DOCUMENT_CONFIG[filename]
    doc = create_document(config["title"])

    add_metadata_table(doc, answers)

    add_section(
        doc,
        "Zweck des Dokuments",
        config["purpose"],
    )

    summary = _build_summary(config["sections"], raw_json, answers)
    add_section(doc, "Zusammenfassung", summary)

    add_section(doc, "Relevante Angaben aus dem Fragebogen", "")
    _add_questionnaire_tables(doc, config["sections"], raw_json)

    assessment = _build_assessment(config["sections"], answers)
    add_section(doc, "Bewertung / Einordnung", assessment)

    open_points = answers.get("documentation_governance.open_points", "")
    add_section(
        doc,
        "Offene Punkte",
        open_points or "Keine offenen Punkte dokumentiert.",
    )

    next_steps = _build_next_steps(answers)
    add_section(doc, "Empfohlene nächste Maßnahmen", "")
    add_bullet_list(doc, next_steps)

    add_disclaimer(doc)

    output_path = output_dir / filename
    save_document(doc, str(output_path))
    return output_path


def _sections_by_id(raw_json: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {section["id"]: section for section in raw_json.get("sections", [])}


def _build_summary(section_ids: list[str], raw_json: dict[str, Any], answers: dict[str, str]) -> str:
    parts: list[str] = []
    sections = _sections_by_id(raw_json)

    company = answers.get("company.company_name", "")
    system = answers.get("ai_system_profile.ai_system_name", "")
    if company or system:
        parts.append(f"Dieses Dokument bezieht sich auf {company or 'das Unternehmen'} und das KI-System {system or '—'}.")

    for section_id in section_ids:
        section = sections.get(section_id)
        if section and section.get("description"):
            parts.append(section["description"])

    risk = answers.get("risk_classification.preliminary_risk_result", "")
    if risk:
        parts.append(f"Vorläufiges Risikoergebnis: {risk}.")

    return "\n\n".join(parts) if parts else "Es liegen strukturierte Angaben aus dem Fragebogen vor."


def _add_questionnaire_tables(doc, section_ids: list[str], raw_json: dict[str, Any]) -> None:
    sections = _sections_by_id(raw_json)

    for section_id in section_ids:
        section = sections.get(section_id)
        if not section:
            continue

        doc.add_heading(section.get("title", section_id), level=2)
        rows: list[tuple[str, str]] = []
        for question in section.get("questions", []):
            label = question.get("label", question.get("id", ""))
            value = format_answer_value(question.get("answer"))
            rows.append((label, value))

        if rows:
            add_key_value_table(doc, rows)


def _build_assessment(section_ids: list[str], answers: dict[str, str]) -> str:
    role = answers.get("role_assessment.primary_role", "")
    risk = answers.get("risk_classification.preliminary_risk_result", "")
    personal_data = answers.get("data_governance.personal_data_processed", "")

    lines = [
        "Auf Basis der eingegebenen Informationen ergibt sich eine vorläufige Einschätzung.",
    ]
    if role:
        lines.append(f"Primäre Rolle nach AI Act: {role}.")
    if risk:
        lines.append(f"Risikoeinordnung: {risk}.")
    if personal_data:
        lines.append(f"Personenbezogene Daten: {personal_data}.")

    if "risk_classification" in section_ids:
        reasoning = answers.get("risk_classification.risk_classification_reasoning", "")
        if reasoning:
            lines.append(reasoning)

    return "\n\n".join(lines)


def _build_next_steps(answers: dict[str, str]) -> list[str]:
    steps = [
        "Fachliche, technische, datenschutzrechtliche und rechtliche Prüfung der Dokumentation.",
        "Offene Punkte schließen und Verantwortlichkeiten bestätigen.",
    ]

    if answers.get("documentation_governance.next_review_date"):
        steps.append(f"Nächste Review-Terminierung: {answers['documentation_governance.next_review_date']}.")

    if answers.get("risk_classification.preliminary_risk_result") in {
        "Hochrisiko-Indikation möglich",
        "Verbotene Praxis möglich",
        "Unklar / rechtliche Prüfung erforderlich",
    }:
        steps.append("Vertiefte rechtliche Prüfung der Risikoklassifizierung und Pflichten einplanen.")

    if answers.get("data_governance.personal_data_processed") == "Ja":
        steps.append("DSGVO-/DSFA-Anforderungen mit Datenschutz abstimmen.")

    return steps
