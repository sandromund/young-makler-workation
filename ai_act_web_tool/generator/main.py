from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path

from .build_documents import build_document
from .document_router import select_documents
from .json_loader import load_answers, load_raw_json

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = ROOT / "output" / "documents"
DEFAULT_ZIP_PATH = ROOT / "output" / "ai_act_documentation_package.zip"


def generate_documents(
    input_path: Path,
    output_dir: Path | None = None,
    zip_path: Path | None = None,
    create_zip: bool = True,
) -> dict:
    input_path = input_path.resolve()
    output_dir = (output_dir or DEFAULT_OUTPUT_DIR).resolve()
    zip_path = (zip_path or DEFAULT_ZIP_PATH).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"JSON-Datei nicht gefunden: {input_path}")

    raw_json = load_raw_json(input_path)
    answers = load_answers(input_path)
    selected = select_documents(answers)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    for filename in selected:
        build_document(filename, raw_json, answers, output_dir)
        created.append(filename)

    zip_url = None
    if create_zip:
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file_path in sorted(output_dir.glob("*.docx")):
                archive.write(file_path, arcname=file_path.name)
        zip_url = f"/output/{zip_path.name}"

    return {
        "ok": True,
        "count": len(created),
        "documents": created,
        "output_dir": str(output_dir.relative_to(ROOT)).replace("\\", "/"),
        "zip": zip_url,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="AI-Act Word-Dokumente aus questions.json erzeugen")
    parser.add_argument("--input", required=True, help="Pfad zur questions.json")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_DIR), help="Ausgabeordner für DOCX-Dateien")
    parser.add_argument("--zip", action="store_true", help="Zusätzlich ZIP-Paket erstellen")
    args = parser.parse_args()

    result = generate_documents(
        input_path=Path(args.input),
        output_dir=Path(args.output),
        create_zip=args.zip,
    )
    print(f"{result['count']} Dokumente erstellt in {result['output_dir']}")
    if result.get("zip"):
        print(f"ZIP: {result['zip']}")


if __name__ == "__main__":
    main()
