# KI-Hacks für Makler: Zwischen genial, gefährlich und gerade noch erlaubt

KI verspricht Maklern genau das, was im Alltag fehlt: weniger Handarbeit, schnellere Prozesse und mehr Zeit für Kunden. In dieser Session zeigen wir live, was heute praktisch geht – von besseren Prompts über lauffähige Python-Skripte bis hin zu KI-Dokumenten, die auch einer späteren Prüfung standhalten sollen. Gleichzeitig testen wir die Schattenseite: Wie manipulierbar sind KI-Systeme? Wo geraten Schutzmechanismen an ihre Grenzen? Und ab wann wird ein produktiver Hack zur Haftungsfalle? Ein ehrlicher Praxistest für alle, die KI im Maklerbetrieb nicht nur spannend finden, sondern produktiv, sicher und nachweisbar einsetzen wollen.

[![Repository – QR-Code zum Herunterladen](QR.png)](https://github.com/sandromund/young-makler-workation)

**Repository:** Mit dem Smartphone scannen oder [github.com/sandromund/young-makler-workation](https://github.com/sandromund/young-makler-workation) im Browser öffnen.

**Workshop-Einstieg:** [intro.md](intro.md) – KI-Wachstum, Forschung und Beispiele in Bildern.

---

## Anleitung für Nicht-Entwickler: Mit KI Code entwickeln

Sie müssen kein Programmierer sein, um mit KI eigene Tools, Skripte und Demos zu bauen. Dieses Repository enthält fertige Workshop-Beispiele – und **Cursor** hilft Ihnen beim Verstehen, Anpassen und Erweitern des Codes in natürlicher Sprache.

**Grundprinzip:** Sie beschreiben in Cursor, was Sie möchten („Erkläre mir diese Datei“, „Passe die Suchbegriffe an“, „Baue eine Excel-Ausgabe mit Filter“). Die KI arbeitet direkt in den Projektdateien mit – Sie prüfen das Ergebnis und testen es lokal.

### Was Sie brauchen

| Tool | Wofür |
|------|--------|
| [Cursor](#cursor-ki-code-editor) | Code lesen, bearbeiten und mit KI-Unterstützung entwickeln |
| [Python](#python-installieren) | Die meisten Demos in diesem Projekt (Crawling, PDF, AI Act, lokale LLMs) |
| [Node.js / npm](#nodejs-und-npm-installieren) | Web-Demos mit JavaScript (z. B. DeepInfra-Chat) |
| [Git](#code-herunterladen-mit-git-oder-zip) | Projekt herunterladen und aktuell halten |
| API-Keys | Für Cloud-Dienste (Google Places, DeepInfra) – siehe unten |

---

## Wichtige Links

### Cursor (KI-Code-Editor)

**Download:** [https://cursor.com/](https://cursor.com/)

1. Cursor installieren und starten.
2. **File → Open Folder** und den entpackten Projektordner `young-makler-workation` öffnen.
3. Im Chat (Strg+L bzw. Cmd+L) Fragen stellen, z. B.:
   - *„Erkläre mir den Ordner google-places-lead-radar.“*
   - *„Wie trage ich meinen API-Key ein?“*
   - *„Starte das Skript und sag mir, wenn ein Fehler kommt.“*
4. Cursor kann Terminal-Befehle vorschlagen und Dateien direkt ändern – Änderungen vor dem Speichern kurz prüfen.

### Python installieren

**Download:** [https://www.python.org/downloads/](https://www.python.org/downloads/)

**Windows:**

1. Installer herunterladen und starten.
2. **Wichtig:** Haken setzen bei **„Add Python to PATH“**.
3. Auf „Install Now“ klicken.
4. Prüfen (PowerShell oder Eingabeaufforderung):

```powershell
py -3 --version
```

**macOS / Linux:**

```bash
python3 --version
```

Falls keine Version angezeigt wird: Python von python.org installieren.

**Pakete für dieses Projekt** (einmalig im Projektordner):

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Unter macOS/Linux: `python3 -m venv .venv`, dann `source .venv/bin/activate`.

### Node.js und npm installieren

**npm** ist der Paketmanager für JavaScript-Projekte. Er wird mit **Node.js** mitgeliefert.

**Download:** [https://nodejs.org/](https://nodejs.org/) — **LTS-Version** wählen (empfohlen: 18 oder höher).

**Windows / macOS:** Installer ausführen, Standardoptionen beibehalten.

**Prüfen:**

```powershell
node --version
npm --version
```

**Typischer Ablauf** (Beispiel: DeepInfra-Chat):

```powershell
cd uncensored-ai-api\deepinfra-chat
npm install
npm start
```

- `npm install` — lädt Abhängigkeiten (nur beim ersten Mal oder nach Updates nötig).
- `npm start` — startet den lokalen Webserver.
- Terminal **offen lassen**; mit **Strg+C** beenden.

Details: [uncensored-ai-api/deepinfra-chat/README.md](uncensored-ai-api/deepinfra-chat/README.md)

### Code herunterladen (mit Git oder ZIP)

#### Variante A: ZIP (ohne Git)

1. Repository-Seite auf GitHub im Browser öffnen.
2. **Code → Download ZIP**.
3. ZIP entpacken, Ordner in Cursor öffnen.

#### Variante B: Git (für Updates)

**Git installieren:** [https://git-scm.com/downloads](https://git-scm.com/downloads)

```powershell
git clone https://github.com/sandromund/young-makler-workation.git
cd young-makler-workation
```

Alternativ (BBG Git):

```powershell
git clone https://git.bbg-online.de/bbg-quellcode/young-makler-workation.git
```

Später aktualisieren:

```powershell
git pull
```

**Hinweis:** Die Datei `.env` mit Ihren API-Keys gehört **nicht** ins Repository. Nach dem Download `.env.example` nach `.env` kopieren und Keys eintragen (siehe unten).

---

## API-Keys und Umgebungsvariablen

Im Projektroot liegt eine Vorlage:

```text
.env.example  →  kopieren nach  →  .env
```

Inhalt (Beispiel):

```env
API_KEY_GOOGLE_PLACES=hier_api_key_eintragen
DEEP_INFRA_API_KEY=your_deepinfra_api_key_here
PORT=3000
```

**Wichtig:** `.env` niemals teilen, committen oder in Screenshots zeigen.

---

## Demos in diesem Repository

| Ordner | Inhalt | Technologie |
|--------|--------|-------------|
| [google-places-lead-radar](google-places-lead-radar/) | Regionale B2B-Recherche über Google Places → Excel | Python |
| [local-llm](local-llm/) | Lokale KI mit LM Studio und MCP-Tools | Python + LM Studio |
| [uncensored-ai-api/deepinfra-chat](uncensored-ai-api/deepinfra-chat/) | Chat im Browser über Cloud-API | Node.js + DeepInfra |
| [ai_act_web_tool](ai_act_web_tool/) | AI-Act-Fragebogen im Browser | Python |
| [prompt_injection_workshop_kit](prompt_injection_workshop_kit/) | Demo: versteckte Prompts in PDFs | Python |

Ausführliche Anleitungen stehen in den jeweiligen `README.md`-Dateien der Unterordner.

---

## Crawling-Demo: Google Places API (API-Key)

**Projekt:** [google-places-lead-radar](google-places-lead-radar/)

Das ist **kein** inoffizieller Google-Maps-Scraper, sondern die offizielle **Google Places API** – stabiler und für Workshops besser geeignet.

### Places API aktivieren

Direktlink zur API-Bibliothek (Beispielprojekt):

[https://console.cloud.google.com/apis/library/places.googleapis.com](https://console.cloud.google.com/apis/library/places.googleapis.com?project=dkm-app-1e302)

**Schritte:**

1. Mit Google-Konto anmelden: [Google Cloud Console](https://console.cloud.google.com/)
2. Projekt wählen oder **Neues Projekt** anlegen.
3. **Places API** aktivieren (Link oben oder unter *APIs & Dienste → Bibliothek*).
4. **Abrechnung** hinterlegen (Google Maps Platform kann Kosten verursachen – Budget/Limits setzen).
5. Unter *APIs & Dienste → Anmeldedaten → Anmeldedaten erstellen → API-Schlüssel* einen Key erzeugen.
6. Key in `.env` eintragen:

```env
API_KEY_GOOGLE_PLACES=Ihr_API_Key
```

7. Suchbegriffe in `google-places-lead-radar/input.txt` eintragen.
8. Skript starten:

```powershell
cd google-places-lead-radar
py -3 main.py
```

Excel-Ausgabe liegt in `google-places-lead-radar/output/`.

**Ausführliche Schritt-für-Schritt-Anleitung:** [google-places-lead-radar/README.md](google-places-lead-radar/README.md)

---

## Lokale KIs: LM Studio

**Website:** [https://lmstudio.ai/](https://lmstudio.ai/)

Mit LM Studio laufen Sprachmodelle **offline auf Ihrem Rechner** – ohne Cloud-API und ohne laufende API-Kosten. Ideal, um zu zeigen, wie KI lokale Python-Funktionen (MCP-Tools) aufrufen kann.

**Projekt:** [local-llm](local-llm/)

**Kurzablauf:**

1. LM Studio installieren und ein Modell laden (z. B. Qwen, Gemma – mit Tool-Calling-Unterstützung).
2. Tab **Developer → Local Server → Start Server** (Standard: `http://localhost:1234/v1`).
3. Python-Umgebung einrichten und MCP-Server starten (siehe [local-llm/README.md](local-llm/README.md)).
4. In LM Studio unter **Chat → Program → Install → Edit mcp.json** die generierte Konfiguration einbinden.
5. Im Chat testen, z. B.: *„Nutze das verfügbare Tool und addiere 17 und 25.“*

---

## Demo-APIs: DeepInfra (Cloud-KI im Browser)

**Website:** [https://deepinfra.com/](https://deepinfra.com/)

DeepInfra stellt verschiedene Open-Source-Modelle über eine API bereit – günstig und schnell für Demos, ohne eigene GPU.

**Projekt:** [uncensored-ai-api/deepinfra-chat](uncensored-ai-api/deepinfra-chat/)

### API-Key holen

1. Auf [deepinfra.com](https://deepinfra.com/) registrieren.
2. Im Dashboard unter **API Keys** einen neuen Key erstellen.
3. In der `.env` im **Repository-Root** eintragen:

```env
DEEP_INFRA_API_KEY=dein_deepinfra_api_key
PORT=3000
```

### Chat starten

```powershell
cd uncensored-ai-api\deepinfra-chat
npm install
npm start
```

Browser öffnen: [http://localhost:3000](http://localhost:3000)

**Hinweis:** Der API-Key liegt bewusst **nicht** im Frontend, sondern nur auf dem kleinen lokalen Server – so bleibt er beim Workshop nicht für alle sichtbar.

---

## Weitere nützliche Links

| Ressource | Link |
|-----------|------|
| Hugging Face (Modelle & Datasets) | [https://huggingface.co/](https://huggingface.co/) |
| Kaggle (Datensätze & Notebooks) | [https://www.kaggle.com/](https://www.kaggle.com/) |
| Google Cloud SDK (optional, für fortgeschrittene API-Key-Erzeugung) | [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install) |

---

## Typische erste Schritte (Checkliste)

- [ ] Cursor installieren und Projektordner öffnen
- [ ] Python installieren (`py -3 --version` prüfen)
- [ ] Optional: Node.js installieren (für DeepInfra-Chat)
- [ ] `.env.example` nach `.env` kopieren
- [ ] Benötigte API-Keys eintragen (Google Places und/oder DeepInfra)
- [ ] Im Projektroot: `pip install -r requirements.txt`
- [ ] Eine Demo aus der Tabelle oben wählen und deren README folgen
- [ ] Bei Fragen: Cursor-Chat nutzen oder README im jeweiligen Unterordner lesen

---

## Sicherheit und Datenschutz (Kurz)

- API-Keys und `.env`-Dateien **nicht** teilen oder ins Internet stellen.
- Google Places und DeepInfra können **Kosten** verursachen – Limits und Budgets setzen.
- Gesammelte Unternehmensdaten **manuell prüfen**; keine Massenwerbung ohne rechtliche Klärung.
- Prompt-Injection-Demos nur in **geschlossenen Workshop-Umgebungen** zeigen.

Bei rechtlichen Fragen zu KI, Datenschutz oder AI Act: Fachliche Beratung einholen – die Demos hier sind technische Beispiele, keine Rechtsberatung.
