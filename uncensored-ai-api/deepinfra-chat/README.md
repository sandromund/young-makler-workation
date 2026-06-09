# DeepInfra Chat

Lokale Webapp zum Chatten mit KI-Modellen über [DeepInfra](https://deepinfra.com). Das Frontend ist reines HTML, CSS und JavaScript. Ein kleiner Express-Server liest den API-Key aus der zentralen `.env`-Datei im Repository-Root und leitet Anfragen sicher an DeepInfra weiter.

## Voraussetzungen

- **Node.js 18 oder höher** (für natives `fetch` im Backend)
- Ein **DeepInfra-API-Key** ([deepinfra.com](https://deepinfra.com))

## Schnellstart

### 1. Projektordner öffnen

```powershell
cd uncensored-ai-api\deepinfra-chat
```

### 2. Abhängigkeiten installieren

```powershell
npm install
```

Nur beim ersten Mal nötig.

### 3. Umgebungsvariablen einrichten

Im Repository-Root `.env.example` nach `.env` kopieren (falls noch nicht vorhanden):

```powershell
copy ..\..\.env.example ..\..\.env
```

API-Key in `..\..\.env` eintragen:

```env
DEEP_INFRA_API_KEY=dein_deepinfra_api_key
PORT=3000
```

Alternativ funktioniert auch `DEEPINFRA_API_KEY` (ohne Unterstrich).

### 4. Server starten

```powershell
npm start
```

Im Terminal erscheint:

```text
DeepInfra Chat läuft unter http://localhost:3000
```

**Das Terminal offen lassen** — mit **Strg + C** wird der Server beendet.

### 5. Im Browser öffnen

```text
http://localhost:3000
```

**Wichtig:** Die Seite nicht per Doppelklick auf `index.html` öffnen (`file://…`). Ohne laufenden Server funktionieren Chat und Einstellungen nicht.

## Bedienung

- **Modell:** Im Dropdown zwischen verfügbaren DeepInfra-Modellen wählen
- **System-Prompt:** Im Textfeld anpassen — steuert das Verhalten der KI
- **Chat:** Nachricht eingeben und **Senden** klicken oder **Enter** drücken (Shift + Enter für Zeilenumbruch)
- **Antworten:** KI-Antworten werden als Markdown gerendert (Listen, Code-Blöcke, Überschriften usw.)

Verfügbare Modelle und der Standard-System-Prompt können in `config.js` angepasst werden.

## Server neu starten

Nach Änderungen an `config.js` oder `server.js`:

1. Im Terminal **Strg + C** drücken
2. Erneut `npm start` ausführen
3. Browser mit **Strg + F5** neu laden

Falls Port 3000 blockiert ist:

```powershell
Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { Stop-Process -Id $_ -Force }
npm start
```

## Häufige Probleme

| Problem | Lösung |
|--------|--------|
| „Server nicht erreichbar“ | `npm start` ausführen und **http://localhost:3000** öffnen |
| Konfiguration lädt nicht | Alten Server beenden (Strg + C), neu starten, Hard-Reload (Strg + F5) |
| `npm start` im falschen Ordner | In `deepinfra-chat` wechseln, nicht im Repo-Root |
| Kein API-Key | `.env` im Repository-Root anlegen und `DEEP_INFRA_API_KEY` setzen |

## Warum kein API-Key im Frontend?

Eine reine `index.html` im Browser kann keine `.env`-Datei sicher einlesen. Stünde der Key im JavaScript, wäre er für jeden sichtbar, der die Seite oder den Quellcode aufruft. Der Express-Server hält den Key auf dem Server und leitet nur Chat-Anfragen weiter — das Frontend kennt keinen API-Key.

## Projektstruktur

```text
deepinfra-chat/
├─ index.html      Frontend
├─ style.css       Layout und Chat-Styles
├─ app.js          Chat-Logik (Frontend)
├─ server.js       Express-Server und API-Proxy
├─ config.js       Modelle, System-Prompt, API-Einstellungen
└─ package.json    npm-Abhängigkeiten

../.env.example    Vorlage für Umgebungsvariablen (Repository-Root)
../../.env         API-Key (nicht committen)
```

## Konfiguration

| Datei | Inhalt |
|-------|--------|
| `../../.env` | API-Key, Port |
| `config.js` | Modell-Liste, Standard-Modell, System-Prompt, Temperatur, max. Tokens |

Temperatur und maximale Token-Anzahl liegen in `config.js`. Modell und System-Prompt können zusätzlich direkt in der Weboberfläche geändert werden.
