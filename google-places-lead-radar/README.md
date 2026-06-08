# Google Places Lead-Radar

Dieses Projekt erstellt aus Suchbegriffen eine einfache Lead-Liste für regionale B2B-Recherche.

Das Skript liest Suchbegriffe aus einer Textdatei ein, fragt die offizielle Google Places API ab und speichert die gefundenen Unternehmen oder Orte in einer formatierten Excel-Datei.

Beispiel:

```text
Hausverwaltung Bayreuth
Bauträger Bayreuth
Projektentwickler Bayreuth
Architekt Bayreuth
```

Daraus wird eine Excel-Liste mit Informationen wie:

- Firmenname
- Adresse
- Telefonnummer
- Website
- Google-Maps-Link
- Bewertung
- Anzahl Bewertungen
- Kategorie
- Geschäftsstatus

---

## Wichtig

Dieses Projekt ist kein Google-Maps-Scraper.

Es wird nicht Google Maps automatisiert ausgelesen. Stattdessen wird die offizielle Google Places API verwendet.

Das ist technisch sauberer, stabiler und besser für einen professionellen Workshop geeignet.

---

## Projektstruktur

```text
google-places-lead-radar/
├── main.py
├── create_test_api_key.py
├── requirements.txt
├── .env.example
├── .env
├── input.txt
├── README.md
└── output/
```

| Datei | Bedeutung |
|---|---|
| `main.py` | Hauptskript: fragt Google Places ab und erstellt die Excel-Datei |
| `create_test_api_key.py` | Optionales Hilfsskript: erzeugt testweise einen API-Key über die Google Cloud API Keys API |
| `requirements.txt` | Liste der benötigten Python-Pakete |
| `.env.example` | Vorlage für die API-Key-Datei |
| `.env` | Ihre persönliche API-Key-Datei |
| `input.txt` | Suchbegriffe für die Google Places API |
| `output/` | Hier wird die Excel-Datei gespeichert |

---

# 1. Voraussetzungen

Sie benötigen:

- einen Computer mit Windows, macOS oder Linux
- Internetzugang
- Python
- ein Google-Konto
- ein Google-Cloud-Projekt
- einen Google-Cloud-API-Key für die Google Places API

Für die optionale automatische Test-Key-Erzeugung benötigen Sie zusätzlich:

- Google Cloud CLI (`gcloud`)
- Anmeldung per Application Default Credentials
- Berechtigung zum Erstellen von API-Keys im Google-Cloud-Projekt
- aktivierte API Keys API

Für Einsteiger ist der manuelle Weg über die Google Cloud Console einfacher.

---

# 2. Python installieren

## Windows

1. Öffnen Sie:

```text
https://www.python.org/downloads/
```

2. Laden Sie die aktuelle Python-Version herunter.
3. Starten Sie die Installation.
4. Wichtig: Setzen Sie den Haken bei:

```text
Add Python to PATH
```

5. Klicken Sie auf „Install Now“.

## macOS

Öffnen Sie das Terminal und prüfen Sie zuerst, ob Python bereits installiert ist:

```bash
python3 --version
```

Falls Python nicht installiert ist, laden Sie Python hier herunter:

```text
https://www.python.org/downloads/
```

## Prüfung der Installation

Windows:

```bash
python --version
```

macOS oder Linux:

```bash
python3 --version
```

Wenn eine Versionsnummer erscheint, ist Python installiert.

---

# 3. Google Cloud einrichten

Damit das Skript funktioniert, benötigen Sie einen API-Key für die Google Places API.

## Schritt 1: Google Cloud Console öffnen

Öffnen Sie:

```text
https://console.cloud.google.com/
```

Melden Sie sich mit Ihrem Google-Konto an.

## Schritt 2: Neues Projekt erstellen

1. Klicken Sie oben auf die Projektauswahl.
2. Klicken Sie auf „Neues Projekt“.
3. Geben Sie einen Namen ein, zum Beispiel:

```text
places-lead-radar
```

4. Klicken Sie auf „Erstellen“.

## Schritt 3: Abrechnung aktivieren

Für die Google Maps Platform muss in der Regel ein Abrechnungskonto hinterlegt werden.

Wichtig: Die Nutzung der Google Places API kann Kosten verursachen. Prüfen Sie vor der Nutzung die aktuellen Preise und setzen Sie gegebenenfalls Budgets oder Limits in der Google Cloud Console.

## Schritt 4: Places API aktivieren

1. Öffnen Sie in der Google Cloud Console den Bereich „APIs & Dienste“.
2. Klicken Sie auf „Bibliothek“.
3. Suchen Sie nach:

```text
Places API
```

4. Aktivieren Sie die **Places API**.

## Schritt 5: API-Key manuell erstellen

1. Öffnen Sie „APIs & Dienste“.
2. Klicken Sie auf „Anmeldedaten“.
3. Klicken Sie auf „Anmeldedaten erstellen“.
4. Wählen Sie „API-Schlüssel“.
5. Kopieren Sie den erzeugten API-Key.

## Schritt 6: API-Key absichern

Der API-Key sollte nicht offen und ungeschützt bleiben.

Empfehlung:

- Beschränken Sie den Key auf die Google Places API.
- Nutzen Sie nach Möglichkeit IP-Beschränkungen.
- Verwenden Sie den Key nicht öffentlich auf Webseiten.
- Teilen Sie den Key nicht in Präsentationen, Screenshots oder GitHub-Repositories.

---

# 4. Optional: API-Key testweise per Python erzeugen

Neben dem manuellen Weg gibt es im Projekt ein optionales Hilfsskript:

```text
create_test_api_key.py
```

Dieses Skript kann testweise einen API-Key über die Google Cloud API Keys Python Client Library erzeugen.

Wichtig:

- Dieser Weg ist eher für technischere Teilnehmende geeignet.
- Er ersetzt nicht die Prüfung der Google-Cloud-Einstellungen.
- Das Skript erzeugt einen Key, schränkt ihn aber nicht vollständig produktionssicher ein.
- Der erzeugte Key sollte anschließend in der Google Cloud Console auf die Places API eingeschränkt werden.
- Verwenden Sie diesen Weg nur in Test-/Workshop-Umgebungen.

## Voraussetzungen für diese Variante

Sie benötigen zusätzlich:

1. Google Cloud CLI
2. aktivierte API Keys API
3. passende Berechtigungen im Google-Cloud-Projekt
4. gesetzte Projekt-ID
5. Anmeldung per Application Default Credentials

## Google Cloud CLI installieren

Installationsseite:

```text
https://cloud.google.com/sdk/docs/install
```

## Bei Google anmelden

```bash
gcloud auth login
```

Danach Application Default Credentials setzen:

```bash
gcloud auth application-default login
```

## Projekt-ID setzen

Windows PowerShell:

```powershell
$env:GOOGLE_CLOUD_PROJECT="ihre-projekt-id"
```

macOS / Linux:

```bash
export GOOGLE_CLOUD_PROJECT="ihre-projekt-id"
```

Beispiel:

```bash
export GOOGLE_CLOUD_PROJECT="places-lead-radar-123456"
```

## API Keys API aktivieren

In der Google Cloud Console suchen Sie nach:

```text
API Keys API
```

Aktivieren Sie diese API.

Alternativ per Google Cloud CLI:

```bash
gcloud services enable apikeys.googleapis.com
```

## Test-Key erzeugen

Windows:

```bash
python create_test_api_key.py
```

macOS / Linux:

```bash
python3 create_test_api_key.py
```

Wenn alles funktioniert, schreibt das Skript automatisch eine Datei `.env` mit folgendem Inhalt:

```env
API_KEY_GOOGLE_PLACES=...
```

Danach können Sie das Hauptskript starten.

---

# 5. Projekt vorbereiten

## Schritt 1: Projektordner erstellen

Erstellen Sie einen Ordner, zum Beispiel:

```text
google-places-lead-radar
```

Legen Sie darin die Projektdateien ab.

## Schritt 2: Terminal im Projektordner öffnen

### Windows

Öffnen Sie den Ordner im Explorer.

Klicken Sie oben in die Adresszeile, geben Sie ein:

```text
cmd
```

und drücken Sie Enter.

### macOS

Öffnen Sie das Terminal und wechseln Sie in den Projektordner.

Beispiel:

```bash
cd ~/Desktop/google-places-lead-radar
```

---

# 6. Virtuelle Umgebung erstellen

Eine virtuelle Umgebung sorgt dafür, dass die benötigten Python-Pakete sauber getrennt installiert werden.

## Windows

```bash
python -m venv venv
```

Danach aktivieren:

```bash
venv\Scripts\activate
```

## macOS / Linux

```bash
python3 -m venv venv
```

Danach aktivieren:

```bash
source venv/bin/activate
```

Wenn die Aktivierung funktioniert hat, sehen Sie meist vorne in der Zeile:

```text
(venv)
```

---

# 7. Benötigte Pakete installieren

Führen Sie im Projektordner aus:

## Windows

```bash
pip install -r requirements.txt
```

## macOS / Linux

```bash
pip3 install -r requirements.txt
```

Dadurch werden diese Pakete installiert:

- `requests`
- `python-dotenv`
- `pandas`
- `openpyxl`
- `google-cloud-api-keys`

---

# 8. .env-Datei erstellen

Wenn Sie den API-Key manuell erstellt haben, legen Sie die `.env`-Datei selbst an.

Im Projekt gibt es eine Datei:

```text
.env.example
```

Diese Datei ist nur eine Vorlage.

Erstellen Sie eine Kopie dieser Datei und nennen Sie die Kopie:

```text
.env
```

Der Inhalt soll so aussehen:

```env
API_KEY_GOOGLE_PLACES=hier_api_key_eintragen
```

Ersetzen Sie `hier_api_key_eintragen` durch Ihren echten Google API-Key.

Beispiel:

```env
API_KEY_GOOGLE_PLACES=AIzaSyA1234567890BeispielKey
```

Wichtig: Die Datei `.env` enthält einen geheimen Schlüssel. Diese Datei sollte nicht öffentlich geteilt werden.

---

# 9. Suchbegriffe eintragen

Öffnen Sie die Datei:

```text
input.txt
```

Jede Zeile ist eine eigene Suchanfrage.

Beispiel:

```text
Hausverwaltung Bayreuth
Bauträger Bayreuth
Projektentwickler Bayreuth
Architekt Bayreuth
Gewerbepark Bayreuth
Pflegeheim Betreiber Bayreuth
Hotel Betreiber Bayreuth
Gewerbeflächen Bayreuth
```

Zeilen mit `#` am Anfang werden ignoriert.

Beispiel:

```text
# Diese Zeile wird ignoriert
Hausverwaltung Bayreuth
```

Leere Zeilen werden ebenfalls ignoriert.

---

# 10. Skript starten

Windows:

```bash
python main.py
```

macOS / Linux:

```bash
python3 main.py
```

Das Skript liest dann:

1. den API-Key aus `.env`
2. die Suchbegriffe aus `input.txt`
3. die Ergebnisse aus der Google Places API

Danach erstellt es eine Excel-Datei.

---

# 11. Ergebnis finden

Die Excel-Datei wird im Ordner `output/` gespeichert.

Der Dateiname enthält Datum und Uhrzeit.

Beispiel:

```text
output/google_places_leads_2026-06-08_1430.xlsx
```

Die Excel-Datei enthält folgende Komfortfunktionen:

- fixierte erste Zeile
- Filter-Dropdowns in der Kopfzeile
- formatierte Excel-Tabelle
- hervorgehobene Kopfzeile
- sinnvolle Spaltenbreiten
- klickbare Links für Website und Google Maps
- Zahlenformat für Bewertungen und Bewertungsanzahl

Die Datei enthält zum Beispiel folgende Spalten:

| Spalte | Bedeutung |
|---|---|
| Suchbegriff | Der Suchbegriff aus `input.txt` |
| Name | Name des Unternehmens oder Ortes |
| Kategorie | Kategorie laut Google Places |
| Adresse | Adresse |
| Telefonnummer | Telefonnummer, falls vorhanden |
| Website | Website, falls vorhanden |
| Google Maps Link | Link zum Google-Maps-Eintrag |
| Bewertung | Durchschnittsbewertung |
| Anzahl Bewertungen | Anzahl der Google-Bewertungen |
| Geschäftsstatus | Zum Beispiel geöffnet oder geschlossen |
| Place ID | Eindeutige Google-Places-ID |
| Gefunden am | Zeitpunkt der Abfrage |

---

# 12. Typische Fehlermeldungen

## Fehler: `.env` wurde nicht gefunden

Mögliche Ursache:

Die Datei `.env` fehlt.

Lösung:

Kopieren Sie `.env.example` und nennen Sie die Kopie `.env`.

## Fehler: `API_KEY_GOOGLE_PLACES` fehlt

Mögliche Ursache:

In der `.env`-Datei wurde kein API-Key eingetragen.

Lösung:

Öffnen Sie `.env` und tragen Sie den API-Key ein:

```env
API_KEY_GOOGLE_PLACES=Ihr_API_Key
```

## Fehler: `input.txt` wurde nicht gefunden

Mögliche Ursache:

Die Datei `input.txt` liegt nicht im Projektordner.

Lösung:

Legen Sie eine Datei `input.txt` an und tragen Sie Suchbegriffe ein.

## Fehler: API wurde nicht aktiviert

Mögliche Ursache:

Die Places API wurde in Google Cloud nicht aktiviert.

Lösung:

Aktivieren Sie die Places API in der Google Cloud Console.

## Fehler: Abrechnung nicht aktiviert

Mögliche Ursache:

Für das Google-Cloud-Projekt wurde keine Abrechnung eingerichtet.

Lösung:

Aktivieren Sie die Abrechnung in Google Cloud.

## Fehler: API-Key ungültig

Mögliche Ursache:

Der API-Key wurde falsch kopiert oder eingeschränkt.

Lösung:

Prüfen Sie den API-Key und die API-Beschränkungen.

## Fehler beim Erzeugen des Test-API-Keys

Mögliche Ursachen:

- `GOOGLE_CLOUD_PROJECT` ist nicht gesetzt.
- Sie sind nicht per `gcloud auth application-default login` angemeldet.
- Die API Keys API ist nicht aktiviert.
- Ihnen fehlen Berechtigungen im Google-Cloud-Projekt.

Lösung:

Prüfen Sie die Schritte im Abschnitt „Optional: API-Key testweise per Python erzeugen“.

---

# 13. Hinweise zu Kosten

Die Google Places API kann kostenpflichtig sein.

Vor produktiver Nutzung sollten Sie:

- die aktuellen Preise prüfen
- ein Budget in Google Cloud setzen
- Warnungen für Kosten aktivieren
- nur die Felder abfragen, die wirklich benötigt werden
- keine unnötig großen Suchläufe durchführen

Für Workshops empfiehlt sich eine kleine Testliste mit wenigen Suchbegriffen.

---

# 14. Datenschutz und Compliance

Dieses Projekt ist für saubere B2B-Recherche gedacht.

Bitte beachten Sie:

- Sammeln Sie keine privaten personenbezogenen Daten.
- Verwenden Sie die Daten nicht ungeprüft für Massenwerbung.
- Prüfen Sie die Ergebnisse manuell.
- Nutzen Sie bevorzugt allgemeine Unternehmensdaten.
- Speichern Sie nur Daten, die Sie wirklich benötigen.
- Beachten Sie die Datenschutzvorgaben.
- Beachten Sie die Nutzungsbedingungen von Google.
- Dokumentieren Sie den Zweck der Recherche.
- Löschen Sie nicht benötigte Daten regelmäßig.

Dieses Projekt ist ein technisches Workshop-Beispiel und keine Rechtsberatung.

---

# 15. Gute Suchbegriffe für Makler

Beispiele:

```text
Hausverwaltung Bayreuth
Bauträger Bayreuth
Projektentwickler Bayreuth
Architekt Bayreuth
Gewerbepark Bayreuth
Pflegeheim Betreiber Bayreuth
Hotel Betreiber Bayreuth
Gewerbeflächen Bayreuth
Wohnungsbaugesellschaft Bayreuth
Immobilienverwaltung Bayreuth
```

Weitere mögliche Suchmuster:

```text
Hausverwaltung Bamberg
Bauträger Nürnberg
Projektentwickler München
Gewerbeflächen Regensburg
Architekturbüro Würzburg
```

---

# 16. Empfohlener Workshop-Ablauf

1. `input.txt` gemeinsam mit Suchbegriffen füllen.
2. API-Key in `.env` eintragen oder optional testweise erzeugen.
3. Skript starten.
4. Excel-Datei öffnen.
5. Filter ausprobieren.
6. Ergebnisse prüfen.
7. Interessante Unternehmen markieren.
8. Optional: Websites der Unternehmen separat analysieren.
9. Datenschutz-Ampel ergänzen:
   - Grün: allgemeiner B2B-Kontakt
   - Gelb: manuell prüfen
   - Rot: nicht verwenden

---

# 17. Wichtiger Hinweis zur Nutzung

Dieses Skript soll nicht dazu dienen, wahllos Kontaktdaten zu sammeln.

Der sinnvolle Einsatz ist:

```text
Regionale Unternehmensrecherche → manuelle Prüfung → qualifizierte B2B-Ansprache
```

Nicht sinnvoll ist:

```text
Massenhaft Daten sammeln → automatisch Werbemails versenden
```

Für Ihren Workshop passt daher die Formulierung:

```text
Regionaler Lead-Radar mit Google Places API und KI-Bewertung
```

statt:

```text
Google Maps Scraper
```

---

# 18. Beispiel `requirements.txt`

```text
requests
python-dotenv
pandas
openpyxl
google-cloud-api-keys
```

---

# 19. Beispiel `.env.example`

```env
API_KEY_GOOGLE_PLACES=hier_api_key_eintragen
```

---

# 20. Erwartetes Ergebnis

Nach dem Start des Skripts sollte eine Excel-Datei entstehen, zum Beispiel:

```text
output/google_places_leads_2026-06-08_1430.xlsx
```

Diese Datei können Sie mit Microsoft Excel, LibreOffice Calc oder Google Tabellen öffnen.

---

# 21. Aus main.py ein ausführbares Programm erstellen

Zusätzlich zum normalen Start über Python kann aus `main.py` eine ausführbare Datei erstellt werden.

Dafür ist die Datei vorhanden:

```text
build_exe.py
```

Das Build-Skript verwendet **PyInstaller**.

## Wichtig vorab

Die ausführbare Datei wird immer für das Betriebssystem erstellt, auf dem das Build-Skript läuft.

Das bedeutet:

| Sie führen `build_exe.py` aus auf | Ergebnis |
|---|---|
| Windows | `.exe` für Windows |
| macOS | ausführbares Programm für macOS |
| Linux | ausführbares Programm für Linux |

Eine Windows-EXE sollte daher auf einem Windows-Rechner erstellt werden.

## Schritt 1: Abhängigkeiten installieren

Aktivieren Sie zuerst die virtuelle Umgebung.

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

Installieren Sie danach die Pakete:

```bash
pip install -r requirements.txt
```

In `requirements.txt` ist auch `pyinstaller` enthalten.

## Schritt 2: Build-Skript starten

Windows:

```bash
python build_exe.py
```

macOS / Linux:

```bash
python3 build_exe.py
```

## Schritt 3: Ergebnis finden

Nach erfolgreichem Build gibt es einen Ordner:

```text
release/GooglePlacesLeadRadar/
```

Darin liegen unter anderem:

```text
GooglePlacesLeadRadar.exe     Windows
GooglePlacesLeadRadar         macOS/Linux
input.txt
.env.example
README.md
START_HIER.txt
output/
```

Zusätzlich wird eine ZIP-Datei erstellt:

```text
release/GooglePlacesLeadRadar.zip
```

Diese ZIP-Datei können Sie an Workshop-Teilnehmende weitergeben.

## Schritt 4: Programm verwenden

Im Release-Ordner:

1. Kopieren Sie `.env.example`.
2. Benennen Sie die Kopie in `.env` um.
3. Tragen Sie den API-Key ein:

```env
API_KEY_GOOGLE_PLACES=Ihr_API_Key
```

4. Bearbeiten Sie `input.txt` mit den gewünschten Suchbegriffen.
5. Starten Sie die ausführbare Datei.
6. Die Excel-Datei wird im Ordner `output/` erstellt.

## Hinweis zur .env-Datei bei der ausführbaren Version

Bei der ausführbaren Version müssen diese Dateien im gleichen Ordner liegen wie die `.exe` bzw. das ausführbare Programm:

```text
.env
input.txt
```

Der Ordner `output/` wird automatisch verwendet bzw. erstellt.

## Typische Probleme beim Build

### Fehler: PyInstaller ist nicht installiert

Lösung:

```bash
pip install -r requirements.txt
```

### Antivirenprogramm meldet die EXE

Bei selbst erstellten PyInstaller-EXE-Dateien kann es gelegentlich zu Warnungen kommen, weil die Datei unbekannt ist.

Für Workshops empfiehlt sich:

- EXE nur aus vertrauenswürdigem Quellcode erstellen
- keine fremden API-Keys einbauen
- `.env` immer separat halten
- EXE vorab auf dem Zielsystem testen

### Die EXE findet input.txt nicht

Lösung:

Legen Sie `input.txt` in denselben Ordner wie die EXE.

### Die EXE findet .env nicht

Lösung:

Legen Sie `.env` in denselben Ordner wie die EXE.

Die Datei muss enthalten:

```env
API_KEY_GOOGLE_PLACES=Ihr_API_Key
```
