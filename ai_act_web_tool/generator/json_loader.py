from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_raw_json(json_path: Path) -> dict[str, Any]:
    with json_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_answers(json_path: Path) -> dict[str, str]:
    data = load_raw_json(json_path)
    answers: dict[str, str] = {}

    for section in data.get("sections", []):
        section_id = section.get("id", "")
        for question in section.get("questions", []):
            question_id = question.get("id", "")
            key = f"{section_id}.{question_id}"
            answers[key] = _format_answer(question.get("answer"))

    return answers


def _format_answer(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if str(item).strip())
    return str(value).strip()
