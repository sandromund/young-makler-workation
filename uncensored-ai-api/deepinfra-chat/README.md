# DeepInfra Chat

Kleine lokale Webapp zum Chatten mit DeepInfra (Mistral Small 24B). Das Frontend ist reines HTML/CSS/JavaScript; ein Express-Server leitet Anfragen sicher an die DeepInfra-API weiter.

## Voraussetzungen

- **Node.js 18+** (für natives `fetch` im Backend)

## Einrichtung

1. In den Projektordner wechseln:

```bash
cd deepinfra-chat
```

2. Abhängigkeiten installieren:

```bash
npm install
```

3. `.env.example` nach `.env` kopieren:

```bash
copy .env.example .env
```

4. DeepInfra-API-Key in `.env` eintragen:

```env
DEEP_INFRA_API_KEY=dein_key
```

Alternativ funktioniert auch `DEEPINFRA_API_KEY` (ohne Unterstrich).

5. Server starten:

```bash
npm start
```

6. Im Browser öffnen:

```text
http://localhost:3000
```

## Warum kein API-Key im Frontend?

Eine reine `index.html` im Browser kann keine `.env`-Datei sicher einlesen. Würde der Key im JavaScript stehen, wäre er für jeden sichtbar, der die Seite oder den Quellcode aufruft. Der lokale Express-Server hält den Key auf dem Server und leitet nur die Chat-Anfragen weiter — das Frontend kennt keinen API-Key.

## Konfiguration

Modell, API-URL, Temperatur und maximale Tokens liegen in `config.js`. Port und API-Key in `.env`.
