"""
Optionales Hilfsskript: API-Key testweise per Google Cloud API Keys API erstellen.

Wichtig:
- Das Skript ist nur für Test-/Workshop-Umgebungen gedacht.
- Es benötigt Google Application Default Credentials.
- Der erzeugte Key sollte danach in der Google Cloud Console eingeschränkt werden.
- API-Keys dürfen nicht veröffentlicht oder in Git-Repositories gespeichert werden.
"""

import os
from pathlib import Path

from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPO_ROOT / ".env"


def create_api_key(project_id: str, display_name: str) -> str:
    """Erzeugt einen neuen API-Key in einem Google-Cloud-Projekt."""
    client = api_keys_v2.ApiKeysClient()
    parent = f"projects/{project_id}/locations/global"

    key = Key(display_name=display_name)
    request = api_keys_v2.CreateKeyRequest(parent=parent, key=key)

    operation = client.create_key(request=request)
    created_key = operation.result()

    key_string_request = api_keys_v2.GetKeyStringRequest(name=created_key.name)
    key_string_response = client.get_key_string(request=key_string_request)

    return key_string_response.key_string


def set_env_value(key: str, value: str) -> None:
    """Setzt oder aktualisiert einen Eintrag in der zentralen .env-Datei."""
    lines: list[str] = []
    found = False

    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith(f"{key}=") or stripped.startswith(f"{key} "):
                lines.append(f"{key}={value}")
                found = True
            else:
                lines.append(line)

    if not found:
        if lines and lines[-1].strip():
            lines.append("")
        lines.append(f"{key}={value}")

    ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    print("Test-API-Key-Erzeugung startet...")

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()

    if not project_id:
        print("Fehler: Die Umgebungsvariable GOOGLE_CLOUD_PROJECT fehlt.")
        print("Beispiel Windows PowerShell:")
        print('$env:GOOGLE_CLOUD_PROJECT="ihr-projekt-id"')
        print("Beispiel macOS/Linux:")
        print('export GOOGLE_CLOUD_PROJECT="ihr-projekt-id"')
        return

    try:
        api_key = create_api_key(project_id, "workshop-google-places-test-key")
    except Exception as error:
        print("Fehler beim Erzeugen des API-Keys.")
        print(error)
        print("Prüfen Sie: Anmeldung per gcloud, Berechtigungen, aktivierte API Keys API und Projekt-ID.")
        return

    set_env_value("API_KEY_GOOGLE_PLACES", api_key)

    print(f"Fertig. Der API-Key wurde in {ENV_FILE} geschrieben.")
    print("Bitte schränken Sie den Key in der Google Cloud Console auf die Places API ein.")


if __name__ == "__main__":
    main()
