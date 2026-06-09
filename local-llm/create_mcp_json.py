"""
create_mcp_json.py

Erstellt automatisch eine mcp.json für LM Studio.

Das Skript geht davon aus, dass sich diese Datei im gleichen Ordner wie server.py befindet.

Ausführen:
    python create_mcp_json.py

Ergebnis:
    Es wird eine Datei mcp.json im aktuellen Projektordner erstellt.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def build_mcp_config(
    server_name: str = "demo-tools",
    server_file_name: str = "server.py",
) -> dict:
    """
    Baut die MCP-Konfiguration für LM Studio.

    Args:
        server_name: Name des MCP-Servers in LM Studio.
        server_file_name: Dateiname des Python-MCP-Servers.

    Returns:
        Dictionary mit der MCP-Konfiguration.
    """
    project_dir = Path(__file__).resolve().parent
    server_path = project_dir / server_file_name
    python_path = Path(sys.executable).resolve()

    if not server_path.exists():
        raise FileNotFoundError(
            f"Die Datei '{server_file_name}' wurde nicht gefunden: {server_path}"
        )

    return {
        "mcpServers": {
            server_name: {
                "command": str(python_path),
                "args": [
                    str(server_path)
                ],
            }
        }
    }


def write_mcp_json(config: dict, output_file_name: str = "mcp.json") -> Path:
    """
    Schreibt die MCP-Konfiguration als JSON-Datei.

    Args:
        config: MCP-Konfiguration als Dictionary.
        output_file_name: Name der Ausgabedatei.

    Returns:
        Pfad zur erzeugten JSON-Datei.
    """
    project_dir = Path(__file__).resolve().parent
    output_path = project_dir / output_file_name

    output_path.write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return output_path


def main() -> None:
    config = build_mcp_config()
    output_path = write_mcp_json(config)

    print("mcp.json wurde erstellt.")
    print(f"Pfad: {output_path}")
    print()
    print("Inhalt:")
    print(json.dumps(config, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
