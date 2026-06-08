# PROMPT.md

Erstelle ein vollständiges Python-Projekt für einen Workshop.

## Ziel des Projekts

Das Python-Skript soll Suchbegriffe aus einer `.txt`-Datei einlesen, mit der Google Places API nach passenden Unternehmen/Orten suchen und die Ergebnisse in eine Excel-Datei exportieren.

Das Projekt soll möglichst einfach bedienbar sein, damit auch Personen ohne Programmierkenntnisse es nutzen können.

## Anforderungen

Erstelle folgende Dateien:

```text
google-places-lead-radar/
├── main.py
├── create_test_api_key.py
├── requirements.txt
├── .env.example
├── input.txt
├── README.md
└── output/
```

## Funktionen des Skripts

Das Skript `main.py` soll:

1. Eine `.env`-Datei einlesen.
2. Den API-Key aus folgender Umgebungsvariable verwenden:

```env
API_KEY_GOOGLE_PLACES=
```

3. Eine Datei `input.txt` einlesen.
4. Jede Zeile in `input.txt` als eigene Suchanfrage verwenden.
5. Leere Zeilen und Zeilen mit `#` am Anfang ignorieren.
6. Für jede Suchanfrage die Google Places API verwenden.
7. Die API-Endpunkt-Variante `Text Search (New)` verwenden:

```text
https://places.googleapis.com/v1/places:searchText
```

8. Pro Suchanfrage mehrere Ergebnisse sammeln.
9. Die Ergebnisse in einer Excel-Datei speichern.
10. Die Excel-Datei im Ordner `output/` speichern.
11. Der Dateiname soll automatisch mit Datum und Uhrzeit erzeugt werden, zum Beispiel:

```text
output/google_places_leads_2026-06-08_1430.xlsx
```

## Zu erfassende Datenfelder

Die Excel-Datei soll folgende Spalten enthalten:

- Suchbegriff
- Name
- Kategorie
- Adresse
- Telefonnummer
- Website
- Google Maps Link
- Bewertung
- Anzahl Bewertungen
- Geschäftsstatus
- Place ID
- Gefunden am

## Google Places API FieldMask

Verwende diese Felder:

```text
places.id,
places.displayName,
places.formattedAddress,
places.nationalPhoneNumber,
places.websiteUri,
places.primaryType,
places.rating,
places.userRatingCount,
places.googleMapsUri,
places.businessStatus
```


## Anforderungen an die Excel-Formatierung

Die erzeugte Excel-Datei soll optisch verbessert werden:

- Die erste Zeile soll fixiert werden, sodass die Kopfzeile beim Scrollen sichtbar bleibt.
- Die erste Zeile soll Filter-Dropdowns erhalten.
- Die Daten sollen als Excel-Tabelle formatiert werden.
- Die Kopfzeile soll hervorgehoben werden.
- Spaltenbreiten sollen sinnvoll gesetzt werden.
- Lange Texte sollen umbrochen werden.
- Website- und Google-Maps-Links sollen als klickbare Hyperlinks gesetzt werden.
- Bewertungen sollen als Zahl mit einer Nachkommastelle formatiert werden.
- Anzahl Bewertungen soll als Ganzzahl formatiert werden.

## Verhalten bei Fehlern

Das Skript soll robust sein:

- Wenn die `.env`-Datei fehlt, soll eine verständliche Fehlermeldung erscheinen.
- Wenn `API_KEY_GOOGLE_PLACES` fehlt oder leer ist, soll eine verständliche Fehlermeldung erscheinen.
- Wenn `input.txt` fehlt, soll eine verständliche Fehlermeldung erscheinen.
- Wenn die Google API einen Fehler zurückgibt, soll der Fehler verständlich ausgegeben werden.
- Das Skript soll nicht komplett abstürzen, wenn eine einzelne Suchanfrage fehlschlägt.
- Am Ende soll angezeigt werden, wie viele Ergebnisse gespeichert wurden.

## Technische Anforderungen

Verwende folgende Python-Bibliotheken:

- requests
- python-dotenv
- pandas
- openpyxl

## Anforderungen an requirements.txt

Die Datei `requirements.txt` soll enthalten:

```text
requests
python-dotenv
pandas
openpyxl
google-cloud-api-keys
```

## Anforderungen an .env.example

Die Datei `.env.example` soll enthalten:

```env
API_KEY_GOOGLE_PLACES=hier_api_key_eintragen
```

## Anforderungen an input.txt

Erstelle eine Beispiel-Datei `input.txt` mit diesen Suchbegriffen:

```text
# Jede Zeile ist eine eigene Suchanfrage.
# Zeilen mit # werden ignoriert.

Hausverwaltung Bayreuth
Bauträger Bayreuth
Projektentwickler Bayreuth
Architekt Bayreuth
Gewerbepark Bayreuth
Pflegeheim Betreiber Bayreuth
Hotel Betreiber Bayreuth
Gewerbeflächen Bayreuth
```


## Zusätzliche Anforderung: optionale Test-API-Key-Erzeugung

Erstelle zusätzlich eine Datei `create_test_api_key.py`.

Dieses Hilfsskript soll testweise einen Google API-Key über die Google Cloud API Keys Python Client Library erzeugen können. Es soll die Bibliothek `google-cloud-api-keys` verwenden.

Wichtig:

- Das Hilfsskript ist optional und nur für Test-/Workshop-Zwecke gedacht.
- Es soll nicht automatisch von `main.py` ausgeführt werden.
- Es benötigt Google Application Default Credentials.
- Es soll die Projekt-ID aus der Umgebungsvariable `GOOGLE_CLOUD_PROJECT` lesen.
- Es soll einen API-Key mit dem Anzeigenamen `workshop-google-places-test-key` erzeugen.
- Es soll den erzeugten API-Key in die lokale `.env`-Datei schreiben:

```env
API_KEY_GOOGLE_PLACES=...
```

- Es soll verständliche Fehlermeldungen ausgeben, wenn Anmeldung, Projekt-ID, Berechtigungen oder API-Aktivierung fehlen.
- In der README soll erklärt werden, dass dieser Weg fortgeschrittener ist und dass der Key anschließend in der Google Cloud Console auf die Places API eingeschränkt werden sollte.

## Anforderungen an README.md

Erstelle eine ausführliche README-Datei auf Deutsch.

Die README soll für Personen ohne Programmierkenntnisse verständlich sein.

Sie soll enthalten:

1. Kurze Erklärung, was das Projekt macht.
2. Voraussetzungen.
3. Anleitung zur Installation von Python.
4. Anleitung zum Anlegen eines Google-Cloud-Projekts.
5. Anleitung zum Aktivieren der Google Places API.
6. Anleitung zum Erstellen eines API-Keys.
7. Hinweis zur Absicherung des API-Keys.
8. Hinweis, dass Kosten entstehen können.
9. Anleitung zum Erstellen der `.env`-Datei aus `.env.example`.
10. Anleitung zum Bearbeiten der `input.txt`.
11. Anleitung zum Installieren der Abhängigkeiten.
12. Anleitung zum Starten des Skripts.
13. Erklärung, wo die Excel-Datei gespeichert wird.
14. Erklärung typischer Fehlermeldungen.
15. Datenschutz- und Compliance-Hinweise.
16. Hinweis, dass nicht Google Maps gescraped wird, sondern die offizielle Google Places API genutzt wird.

## Datenschutz- und Compliance-Hinweise in der README

Die README soll klar erklären:

- Das Skript soll nur für saubere B2B-Recherche verwendet werden.
- Es sollen keine privaten personenbezogenen Daten gesammelt werden.
- Die Ergebnisse sollen manuell geprüft werden.
- Die Daten dürfen nicht automatisch für Massenwerbung verwendet werden.
- Die Nutzungsbedingungen von Google und Datenschutzvorgaben sind einzuhalten.
- Das Skript ist ein Workshop-Beispiel und keine Rechtsberatung.

## Stil

Der Code soll sauber, kommentiert und verständlich sein.

Bitte schreibe den Code so, dass Anfänger ihn nachvollziehen können.

Nutze sprechende Variablennamen.

Baue keine unnötig komplexe Struktur ein.

Ein einziges Skript `main.py` reicht aus.

## Wichtig

Verwende keine Scraping-Methoden, kein Selenium, kein BeautifulSoup für Google Maps und keine Browser-Automatisierung. Nutze ausschließlich die offizielle Google Places API.

## Zusatzanforderung: ausführbares Programm erzeugen

Ergänze zusätzlich eine Datei:

```text
build_exe.py
```

Diese Datei soll mit PyInstaller aus `main.py` eine ausführbare Datei erstellen.

Anforderungen:

1. Nutze PyInstaller mit `--onefile`.
2. Der Name der App soll `GooglePlacesLeadRadar` sein.
3. Das Build-Skript soll alte Build-Ordner vorher löschen.
4. Das Ergebnis soll in einen Release-Ordner kopiert werden:

```text
release/GooglePlacesLeadRadar/
```

5. In den Release-Ordner sollen zusätzlich kopiert werden:

```text
input.txt
.env.example
README.md
```

6. Im Release-Ordner soll ein leerer Ordner `output/` erstellt werden.
7. Im Release-Ordner soll eine kurze Datei `START_HIER.txt` erstellt werden.
8. Zusätzlich soll eine ZIP-Datei erstellt werden:

```text
release/GooglePlacesLeadRadar.zip
```

9. `requirements.txt` soll zusätzlich enthalten:

```text
pyinstaller
```

10. `main.py` soll so angepasst werden, dass es sowohl als normales Python-Skript als auch als PyInstaller-Programm funktioniert.

Wichtig:

Wenn das Programm als `.exe` läuft, sollen `.env`, `input.txt` und `output/` im gleichen Ordner wie die `.exe` gesucht bzw. erstellt werden.

Dafür kann in `main.py` geprüft werden:

```python
getattr(sys, "frozen", False)
```

Wenn `sys.frozen` aktiv ist, soll der Ordner von `sys.executable` verwendet werden.
