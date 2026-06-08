# Prompt: Lokale DeepInfra-KI-Webapp mit HTML, CSS und JavaScript erstellen

Erstelle ein kleines lokales Webprojekt, mit dem ich eine `index.html` im Browser öffnen kann und über eine Eingabemaske mit einer KI von DeepInfra chatten kann.

Wichtig: Der API-Key darf **nicht** direkt im Frontend stehen. Eine reine Browser-Datei kann eine `.env`-Datei nicht sicher einlesen. Deshalb soll ein kleiner lokaler Node.js-Server erstellt werden, der die `.env` einliest und die Anfrage sicher an DeepInfra weiterleitet. Das Frontend ruft nur den lokalen Server auf.

## Ziel

Erstelle folgende Dateien:

```text
deepinfra-chat/
├─ index.html
├─ style.css
├─ app.js
├─ server.js
├─ config.js
├─ package.json
├─ .env.example
└─ README.md
```

## Technische Anforderungen

- Frontend: HTML, CSS und Vanilla JavaScript
- Backend: Node.js mit Express
- `.env` wird über `dotenv` eingelesen
- DeepInfra wird über die OpenAI-kompatible Chat-Completions-API angesprochen
- API-Endpunkt: `https://api.deepinfra.com/v1/openai/chat/completions`
- Modell: `meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo`
- Modell, API-URL, Temperatur und maximale Tokens sollen in `config.js` stehen
- Der API-Key steht ausschließlich in `.env`
- Das Frontend soll keine API-Keys kennen
- Die Anwendung soll lokal unter `http://localhost:3000` laufen
- Zusätzlich soll die `index.html` sauber im Browser dargestellt werden

## Inhalt der `.env.example`

```env
DEEP_INFRA_API_KEY=your_deepinfra_api_key_here
PORT=3000
```

Hinweis: Falls der Code intern lieber `DEEPINFRA_API_KEY` nutzt, soll zusätzlich geprüft werden, ob `DEEP_INFRA_API_KEY` gesetzt ist. Unterstütze beide Varianten, damit folgende Schreibweise funktioniert:

```env
DEEP_INFRA_API_KEY=***
```

## Inhalt der `config.js`

Erstelle eine zentrale Konfigurationsdatei:

```js
const config = {
  deepinfra: {
    apiUrl: 'https://api.deepinfra.com/v1/openai/chat/completions',
    model: 'meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo',
    temperature: 0.7,
    maxTokens: 1024
  }
};

module.exports = config;
```

## Backend-Anforderungen für `server.js`

- Lade `.env` mit `dotenv`
- Lade `config.js`
- Starte einen Express-Server
- Stelle die statischen Dateien bereit: `index.html`, `style.css`, `app.js`
- Erstelle einen POST-Endpunkt `/api/chat`
- Der Endpunkt erwartet JSON:

```json
{
  "message": "Text des Nutzers"
}
```

- Prüfe, ob `message` vorhanden ist
- Lies den API-Key aus:
  - zuerst `process.env.DEEP_INFRA_API_KEY`
  - alternativ `process.env.DEEPINFRA_API_KEY`
- Wenn kein API-Key gesetzt ist, gib eine verständliche Fehlermeldung zurück
- Sende eine Anfrage an DeepInfra mit folgendem Format:

```js
{
  model: config.deepinfra.model,
  messages: [
    {
      role: 'system',
      content: 'Du bist ein hilfreicher deutschsprachiger Assistent. Antworte klar, praktisch und direkt.'
    },
    {
      role: 'user',
      content: message
    }
  ],
  temperature: config.deepinfra.temperature,
  max_tokens: config.deepinfra.maxTokens
}
```

- Verwende den Header:

```http
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

- Gib an das Frontend nur die Antwort der KI zurück:

```json
{
  "reply": "Antwort der KI"
}
```

- Behandle Fehler sauber und gib verständliche Fehlermeldungen zurück

## Frontend-Anforderungen

### `index.html`

- Moderne einfache Oberfläche
- Titel: `DeepInfra Chat`
- Chat-Ausgabebereich
- Texteingabefeld
- Button `Senden`
- Ladezustand anzeigen, während die Anfrage läuft
- `style.css` und `app.js` einbinden

### `style.css`

- Zentriertes Layout
- Gut lesbare Typografie
- Chat-Bubbles für Nutzer und KI
- Responsive Darstellung für Mobilgeräte
- Button mit Hover-Effekt
- Fehler optisch erkennbar darstellen

### `app.js`

- Eingabe auslesen
- Bei Klick auf `Senden` oder Enter-Taste Anfrage an `/api/chat` senden
- Nutzer-Nachricht sofort im Chat anzeigen
- Antwort der KI im Chat anzeigen
- Fehler im Chat anzeigen
- Während der Anfrage Button deaktivieren und Ladehinweis anzeigen
- Nach Antwort Eingabefeld leeren und wieder fokussieren

## `package.json`

Erstelle ein vollständiges `package.json` mit:

```json
{
  "scripts": {
    "start": "node server.js",
    "dev": "node server.js"
  },
  "dependencies": {
    "dotenv": "latest",
    "express": "latest"
  }
}
```

Falls `fetch` in der verwendeten Node-Version nicht verfügbar sein könnte, nutze Node.js 18+ oder füge eine passende Lösung hinzu. Dokumentiere die Node-Version in der README.

## README.md

Erstelle eine kurze Anleitung auf Deutsch:

1. Projektordner öffnen
2. Abhängigkeiten installieren:

```bash
npm install
```

3. `.env.example` zu `.env` kopieren
4. API-Key eintragen:

```env
DEEP_INFRA_API_KEY=dein_key
```

5. Server starten:

```bash
npm start
```

6. Browser öffnen:

```text
http://localhost:3000
```

Erkläre außerdem kurz, warum die `.env` nicht direkt aus der `index.html` gelesen werden soll: Der API-Key würde sonst im Browser sichtbar werden.

## Qualitätsanforderungen

- Schreibe vollständigen, direkt ausführbaren Code
- Keine Platzhalter außer dem API-Key in `.env.example`
- Saubere Fehlerbehandlung
- Keine Frameworks im Frontend
- Keine Build-Tools
- Keine unnötige Komplexität
- Alle Dateien vollständig ausgeben

## Ausgabeformat

Gib jede Datei einzeln mit Dateiname und vollständigem Inhalt aus. Verwende Markdown-Codeblöcke, zum Beispiel:

```text
// Datei: index.html
```

Danach folgt der vollständige Code der Datei.
