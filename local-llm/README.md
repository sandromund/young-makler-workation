# LM Studio MCP Demo mit Python

Diese Demo zeigt, wie Sie einen lokalen Python-MCP-Server mit LM Studio verbinden und anschließend in der LM-Studio-Chat-UI Funktionen aufrufen können.

## Ziel der Demo

Sie können in LM Studio natürlich schreiben, zum Beispiel:

```text
Nutze das verfügbare Tool und addiere 17 und 25.
```

oder:

```text
Berechne einen Lead-Score für "Muster Makler GmbH" mit 42 Mitarbeitenden und hohem Interesse.
```

LM Studio startet dann den lokalen Python-MCP-Server und ruft die passende Funktion auf.

---

## Projektstruktur

Empfohlene Struktur:

```text
lmstudio-mcp-demo/
├── server.py
├── create_mcp_json.py
├── mcp.json
└── README.md
```

---

## Voraussetzungen

- [LM Studio](https://lmstudio.ai/) (muss zuerst installiert und eingerichtet sein)
- Python 3.10 oder neuer
- Ein lokal geladenes Modell in LM Studio, das Tool Calling gut unterstützt
- Python-Pakete aus `requirements.txt` im Repository-Root (u. a. `mcp`, `openai`)

---

## LM Studio installieren

LM Studio ist die lokale Laufzeitumgebung für die Demo. Ohne installiertes und laufendes LM Studio funktionieren weder die Chat-UI noch die OpenAI-kompatible API.

1. **Herunterladen:** [https://lmstudio.ai/](https://lmstudio.ai/) — für Windows, macOS oder Linux
2. **Installieren** und LM Studio starten
3. **Modell laden:** Im Tab *Search* oder *My Models* ein Modell herunterladen und laden (z. B. Gemma, Qwen oder ein anderes Modell mit Tool-Calling-Unterstützung)
4. **Lokalen Server starten:** Im Tab *Developer* → *Local Server* → **Start Server**  
   Standard-URL: `http://localhost:1234/v1`

Kurztest, ob der Server läuft:

```powershell
Invoke-WebRequest http://localhost:1234/v1/models
```

Wenn JSON mit Modellnamen zurückkommt, ist LM Studio bereit.  
Skripte wie `main.py`, die die OpenAI-kompatible API nutzen, erwarten genau diese URL.

---

## Installation

> **Reihenfolge:** Zuerst [LM Studio](#lm-studio-installieren) installieren und den lokalen Server starten, danach die Python-Umgebung einrichten.

Virtuelle Umgebung und Abhängigkeiten im Projektordner `local-llm`:

### Windows

```powershell
cd local-llm
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
cd local-llm
python3 -m venv .venv
source .venv/bin/activate
```

Abhängigkeiten installieren:

```bash
pip install -r ../requirements.txt
```

---

## Beispiel: MCP-Server anlegen

Erstellen Sie eine Datei `server.py`:

```python
from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("Demo Tools")


@mcp.tool()
def addiere(a: int, b: int) -> int:
    """Addiert zwei Zahlen."""
    return a + b


@mcp.tool()
def erstelle_demo_text(thema: str, zielgruppe: str = "Versicherungsmakler") -> str:
    """Erstellt einen kurzen Demo-Text zu einem Thema für eine Zielgruppe."""
    return (
        f"Demo-Text zum Thema '{thema}' für {zielgruppe}:\n\n"
        f"In dieser Demo zeigen wir, wie ein lokales Sprachmodell über MCP "
        f"gezielt externe Python-Funktionen aufrufen kann."
    )


@mcp.tool()
def aktueller_zeitstempel() -> str:
    """Gibt den aktuellen lokalen Zeitstempel zurück."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@mcp.tool()
def lead_score(firmenname: str, mitarbeiter: int, interesse: str) -> dict:
    """Berechnet einen einfachen Demo-Lead-Score."""
    score = 0

    if mitarbeiter >= 100:
        score += 40
    elif mitarbeiter >= 25:
        score += 25
    else:
        score += 10

    if interesse.lower() in ["hoch", "sehr hoch"]:
        score += 40
    elif interesse.lower() == "mittel":
        score += 25
    else:
        score += 10

    if "versicherung" in firmenname.lower() or "makler" in firmenname.lower():
        score += 20

    return {
        "firmenname": firmenname,
        "score": min(score, 100),
        "einschaetzung": "heißer Lead" if score >= 75 else "prüfen" if score >= 45 else "niedrige Priorität",
    }


if __name__ == "__main__":
    mcp.run()
```

---

## `mcp.json` automatisch erzeugen

Nutzen Sie das Skript `create_mcp_json.py`, um die Datei `mcp.json` automatisch zu erstellen:

```bash
python create_mcp_json.py
```

Das Skript erkennt automatisch:

- den aktuellen Projektordner
- den Python-Interpreter
- die Datei `server.py`
- das Betriebssystem

Danach liegt eine fertige `mcp.json` im Projektordner.

---

## Beispiel für erzeugte `mcp.json`

Die Datei sieht ungefähr so aus:

```json
{
  "mcpServers": {
    "demo-tools": {
      "command": "/absoluter/pfad/zur/python",
      "args": [
        "/absoluter/pfad/zur/server.py"
      ]
    }
  }
}
```

Unter Windows werden die Pfade automatisch korrekt escaped.

---

## MCP-Server in LM Studio einbinden

In LM Studio:

```text
Chat → rechte Seitenleiste → Program → Install → Edit mcp.json
```

Dann den Inhalt der erzeugten `mcp.json` einfügen oder übernehmen.

Falls LM Studio bereits eine bestehende `mcp.json` verwendet, ergänzen Sie nur den Block innerhalb von `"mcpServers"`.

---

## Test in LM Studio

Beispiele für Prompts:

```text
Nutze das verfügbare Tool und addiere 17 und 25.
```

```text
Erstelle mit dem Demo-Tool einen kurzen Text zum Thema MCP-Integration für Versicherungsmakler.
```

```text
Berechne einen Lead-Score für "Muster Makler GmbH" mit 42 Mitarbeitenden und hohem Interesse.
```

---

## Fehlerbehebung

### Verbindungsfehler (`APIConnectionError`, `WinError 10061`)

LM Studio läuft nicht oder der lokale Server ist nicht gestartet.

- LM Studio öffnen und unter *Developer* → *Local Server* den Server starten
- Prüfen, ob `http://localhost:1234/v1/models` erreichbar ist
- Falls LM Studio einen anderen Port anzeigt, `base_url` in `main.py` anpassen

### Tool wird in LM Studio nicht angezeigt

- Prüfen Sie, ob die `mcp.json` valides JSON ist.
- Starten Sie LM Studio neu.
- Prüfen Sie, ob die Pfade absolut sind.

### Python-Server startet nicht

Testen Sie im Terminal:

```bash
python server.py
```

Wenn ein Fehler erscheint, muss dieser zuerst behoben werden.

### Modell ruft kein Tool auf

Formulieren Sie expliziter:

```text
Nutze das verfügbare MCP-Tool ...
```

Setzen Sie außerdem die Temperatur eher niedrig, zum Beispiel auf `0` bis `0.3`.

---

## Hinweis für Demos

Für eine Live-Demo eignen sich besonders diese drei Funktionen:

- `addiere()` für einen einfachen technischen Test
- `erstelle_demo_text()` für sichtbaren Nutzwert
- `lead_score()` für eine strukturierte Business-Logik

Damit zeigen Sie schnell, dass LM Studio nicht nur Text generiert, sondern echte Python-Funktionen ausführen kann.
