# AI-Act Web-Tool

Dieses Mini-Tool lädt eine JSON-Fragenstruktur, zeigt daraus einen Web-Fragebogen an und speichert die Antworten wieder in derselben Struktur.

## Dateien

- `index.html` – Oberfläche
- `style.css` – Layout
- `app.js` – Logik zum Einlesen, Anzeigen und Speichern
- `server.py` – lokaler Webserver zum automatischen Laden/Speichern von JSON
- `questions.json` – Standard-Fragenstruktur (wird beim Start geladen)
- `questions_ai_act_v2_default.json` – erweiterte Fragenstruktur

## Nutzung

1. In den Ordner `ai_act_web_tool` wechseln.
2. Server starten:

```powershell
py -3 server.py
```

3. Im Browser `http://127.0.0.1:8080/index.html` öffnen.
4. Beim Start wird automatisch `questions.json` aus demselben Ordner geladen.
5. Fragen beantworten und mit **Speichern** zurück in dieselbe Datei schreiben.
6. Über die Dropdown-Liste können andere JSON-Dateien im Ordner geladen werden.
7. Die gespeicherte JSON später mit Python einlesen und daraus Word-Dokumente erzeugen.

## Alternative ohne Server

In Chrome/Edge können Sie einmal **Ordner verknüpfen** und danach JSON-Dateien direkt aus dem Tool-Ordner laden und speichern.

## Wichtig

- `index.html` direkt per Doppelklick öffnen reicht nicht für automatisches Laden/Speichern (Browser-Sicherheit).
- Nutzen Sie `py -3 server.py` oder die Ordner-Verknüpfung in Chrome/Edge.

## JSON-Prinzip

Jede Frage hat mindestens:

```json
{
  "id": "company_name",
  "label": "Name des Unternehmens",
  "type": "text",
  "required": true,
  "answer": ""
}
```

Unterstützte Fragetypen:

- `text`
- `textarea`
- `select`
- `radio`
- `checkbox`
- `date`
- `number`
