# Cursor Prompt – AI-Act Documentation Generator

## Ziel

Erstelle ein vollständiges lokales Projekt für einen **AI-Act Documentation Generator**.

Das Projekt soll aus zwei Teilen bestehen:

1. **Web-Tool**
   - liest eine `questions.json` ein
   - zeigt daraus einen dynamischen Fragebogen
   - speichert Antworten wieder in derselben JSON-Struktur
   - erlaubt Download der aktualisierten JSON-Datei

2. **Python-Dokumentengenerator**
   - liest die ausgefüllte `questions.json`
   - erzeugt daraus automatisch Word-Dokumente im `.docx`-Format
   - erstellt nur die Dokumente, die nach Rolle, Risiko und Antworten relevant sind
   - erstellt zusätzlich ein ZIP-Paket mit allen generierten Word-Dateien

Die vorhandene JSON-Datei heißt:

```text
questions_ai_act_v3_full_default.json
```

Sie enthält:

```text
Schema-Version: 3.0
Abschnitte: 23
Fragen: 216
Struktur: meta → sections → questions → answer
```

---

## Erwartete Projektstruktur

Bitte erstelle folgende Struktur:

```text
ai-act-documentation-generator/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── questions.json
│
├── web/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── generator/
│   ├── main.py
│   ├── config.py
│   ├── json_loader.py
│   ├── document_router.py
│   ├── docx_utils.py
│   ├── mappings.py
│   └── documents/
│       ├── management_summary.py
│       ├── ai_system_profile.py
│       ├── role_assessment.py
│       ├── risk_classification.py
│       ├── obligations_matrix.py
│       ├── risk_management.py
│       ├── data_governance.py
│       ├── human_oversight.py
│       ├── transparency_information.py
│       ├── logging_monitoring.py
│       ├── accuracy_robustness_cybersecurity.py
│       ├── testing_validation.py
│       ├── annex_iv_technical_documentation.py
│       ├── conformity_assessment.py
│       ├── eu_declaration.py
│       ├── post_market_monitoring.py
│       ├── incident_reporting.py
│       ├── fria_precheck.py
│       ├── fundamental_rights_assessment.py
│       ├── gdpr_screening.py
│       ├── dpia_precheck.py
│       ├── employee_policy.py
│       ├── training_evidence.py
│       ├── supplier_assessment.py
│       └── documentation_governance.py
│
├── output/
│   ├── documents/
│   └── ai_act_documentation_package.zip
│
└── templates/
    └── optional_docx_templates/
```

---

## Technische Anforderungen

### Python

Verwende:

```text
python-docx
```

Optional:

```text
docxtpl
jinja2
```

Für den ersten Schritt reicht `python-docx`.

Die Datei `requirements.txt` soll enthalten:

```text
python-docx>=1.1.2
```

---

## JSON-Struktur

Die JSON-Datei hat diese Grundstruktur:

```json
{
  "meta": {
    "project_name": "AI-Act Dokumentationspaket",
    "schema_version": "3.0",
    "document_outputs": []
  },
  "sections": [
    {
      "id": "company",
      "title": "Unternehmen",
      "description": "...",
      "questions": [
        {
          "id": "company_name",
          "label": "Name des Unternehmens",
          "type": "text",
          "required": true,
          "answer": "Muster GmbH"
        }
      ]
    }
  ]
}
```

Die Python-Logik soll einen einfachen Zugriff ermöglichen:

```python
answers.get("company.company_name")
answers.get("ai_system_profile.ai_system_name")
answers.get("risk_classification.preliminary_risk_result")
```

Dafür soll `json_loader.py` diese Funktionen bereitstellen:

```python
def load_answers(json_path: str) -> dict:
    # Gibt ein flaches Dictionary zurück:
    # {
    #     "company.company_name": "Muster GmbH",
    #     "ai_system_profile.ai_system_name": "AI Compliance Assistant"
    # }
    pass


def load_raw_json(json_path: str) -> dict:
    # Lädt die vollständige JSON-Struktur unverändert.
    pass
```

---

## Web-Tool Anforderungen

Das Web-Tool soll lokal im Browser funktionieren.

### Funktionen

1. JSON-Datei laden
2. Abschnitte anzeigen
3. Fragen nach Typ rendern
4. Antworten bearbeiten
5. Fortschritt anzeigen
6. JSON herunterladen
7. Geänderte Antworten im jeweiligen `answer`-Feld speichern

### Unterstützte Fragetypen

```text
text
textarea
select
radio
checkbox
date
number
```

### Wichtig

Das Web-Tool muss die vorhandene JSON-Struktur nicht verändern. Es darf nur die Werte in `answer` aktualisieren.

---

## Python-Dokumentengenerator

Der Einstiegspunkt soll sein:

```bash
python generator/main.py --input data/questions.json --output output/documents
```

Optional zusätzlich:

```bash
python generator/main.py --input data/questions.json --output output/documents --zip
```

---

## Dokumente, die erzeugt werden sollen

Das System soll diese Dokumente erzeugen können:

```text
01_Management-Summary.docx
02_AI-System-Steckbrief.docx
03_Rollenklärung-nach-AI-Act.docx
04_Risikoklassifizierung.docx
05_Pflichtenmatrix.docx
06_Risikomanagement.docx
07_Daten-Governance.docx
08_Human-Oversight-Konzept.docx
09_Transparenz-und-Nutzerinformation.docx
10_Logging-und-Monitoring.docx
11_Genauigkeit-Robustheit-Cybersicherheit.docx
12_Test-und-Validierungsbericht.docx
13_Technische-Dokumentation-Annex-IV.docx
14_Konformitätsbewertung.docx
15_EU-Konformitätserklärung.docx
16_Post-Market-Monitoring-Plan.docx
17_Incident-Reporting-Prozess.docx
18_FRIA-Vorprüfung.docx
19_Grundrechte-Folgenabschätzung.docx
20_DSGVO-Schnittstellenprüfung.docx
21_DSFA-Vorprüfung.docx
22_Nutzungsrichtlinie-Mitarbeitende.docx
23_Schulungs-und-Kompetenznachweis.docx
24_Anbieter-und-Lieferantenbewertung.docx
25_Dokumentations-und-Freigabevermerk.docx
```

---

## Dynamische Dokumentenlogik

Erzeuge nicht immer alle Dokumente. Nutze eine Router-Funktion in `document_router.py`.

### Immer erzeugen

```text
01_Management-Summary.docx
02_AI-System-Steckbrief.docx
03_Rollenklärung-nach-AI-Act.docx
04_Risikoklassifizierung.docx
05_Pflichtenmatrix.docx
06_Risikomanagement.docx
07_Daten-Governance.docx
08_Human-Oversight-Konzept.docx
09_Transparenz-und-Nutzerinformation.docx
10_Logging-und-Monitoring.docx
25_Dokumentations-und-Freigabevermerk.docx
```

### Wenn personenbezogene Daten verarbeitet werden

Bedingung:

```python
answers.get("data_governance.personal_data_processed") == "Ja"
```

Dann zusätzlich erzeugen:

```text
20_DSGVO-Schnittstellenprüfung.docx
21_DSFA-Vorprüfung.docx
```

### Wenn Hochrisiko-Indikation möglich ist

Bedingung:

```python
answers.get("risk_classification.preliminary_risk_result") in [
    "Hochrisiko-Indikation möglich",
    "Verbotene Praxis möglich",
    "Unklar / rechtliche Prüfung erforderlich"
]
```

Dann zusätzlich erzeugen:

```text
11_Genauigkeit-Robustheit-Cybersicherheit.docx
12_Test-und-Validierungsbericht.docx
13_Technische-Dokumentation-Annex-IV.docx
18_FRIA-Vorprüfung.docx
19_Grundrechte-Folgenabschätzung.docx
```

### Wenn Anbieter / Provider betroffen ist

Bedingung:

```python
answers.get("role_assessment.primary_role") in [
    "Anbieter / Provider",
    "Mehrere Rollen möglich",
    "Produkthersteller"
]
```

Dann zusätzlich erzeugen:

```text
13_Technische-Dokumentation-Annex-IV.docx
14_Konformitätsbewertung.docx
15_EU-Konformitätserklärung.docx
16_Post-Market-Monitoring-Plan.docx
17_Incident-Reporting-Prozess.docx
```

### Wenn Betreiber / Deployer betroffen ist

Bedingung:

```python
answers.get("role_assessment.primary_role") in [
    "Betreiber / Deployer",
    "Mehrere Rollen möglich"
]
```

Dann zusätzlich erzeugen:

```text
22_Nutzungsrichtlinie-Mitarbeitende.docx
23_Schulungs-und-Kompetenznachweis.docx
24_Anbieter-und-Lieferantenbewertung.docx
```

### Wenn externer Anbieter genutzt wird

Bedingung:

```python
answers.get("role_assessment.external_ai_service") == "Ja"
```

Dann zusätzlich erzeugen:

```text
24_Anbieter-und-Lieferantenbewertung.docx
```

---

## Inhaltliche Anforderungen an Word-Dokumente

Jedes Dokument soll einheitlich aufgebaut sein:

```text
Titel
Dokumentstatus
Zweck des Dokuments
Zusammenfassung
Relevante Angaben aus dem Fragebogen
Bewertung / Einordnung
Offene Punkte
Empfohlene nächste Maßnahmen
Disclaimer
```

Jedes Dokument soll diese Metadaten enthalten:

```text
Projektname
Unternehmen
KI-System
Version
Erstellungsdatum
Dokumentationsversion
Freigabestatus
Verantwortliche Person
```

---

## Word-Formatierung

Bitte erstelle in `docx_utils.py` Hilfsfunktionen:

```python
from docx import Document

def create_document(title: str) -> Document:
    pass

def add_metadata_table(doc: Document, answers: dict) -> None:
    pass

def add_section(doc: Document, title: str, body: str) -> None:
    pass

def add_key_value_table(doc: Document, rows: list[tuple[str, str]]) -> None:
    pass

def add_bullet_list(doc: Document, items: list[str]) -> None:
    pass

def add_disclaimer(doc: Document) -> None:
    pass

def save_document(doc: Document, output_path: str) -> None:
    pass
```

Die Dokumente sollen sauber lesbar sein:

- Überschrift 1 für Titel
- Überschrift 2 für Kapitel
- Tabellen für Stammdaten
- Bullet Points für Maßnahmen
- Seitenränder Standard
- keine komplizierten Styles nötig

---

## Beispiel: Dokument `02_AI-System-Steckbrief.docx`

Dieses Dokument soll mindestens enthalten:

```text
1. Zweck des Dokuments
2. Stammdaten
3. Beschreibung des KI-Systems
4. Vorgesehene Nutzung
5. Ausgeschlossene Nutzung
6. Hauptfunktionen
7. Nutzergruppen
8. Betroffene Personen
9. Systemgrenzen
10. Offene Punkte
11. Nächste Maßnahmen
```

Zu verwendende Felder:

```text
company.company_name
company.industry
company.contact_person
ai_system_profile.ai_system_name
ai_system_profile.ai_system_version
ai_system_profile.deployment_status
ai_system_profile.system_purpose
ai_system_profile.intended_use
ai_system_profile.excluded_use
ai_system_profile.main_functions
ai_system_profile.users
ai_system_profile.affected_persons
ai_system_profile.system_boundaries
documentation_governance.open_points
```

---

## Beispiel: Dokument `04_Risikoklassifizierung.docx`

Dieses Dokument soll mindestens enthalten:

```text
1. Zweck des Dokuments
2. Beschreibung des Systems
3. Prüfung verbotener KI-Praktiken
4. Prüfung Hochrisiko-Bereiche
5. Prüfung Produkt-/Sicherheitskomponente
6. Prüfung Entscheidungswirkung
7. Prüfung Transparenzpflichten
8. Prüfung GPAI-Bezug
9. Vorläufiges Ergebnis
10. Begründung
11. Offene Punkte
12. Empfohlene nächste Maßnahmen
```

Zu verwendende Felder:

```text
risk_classification.prohibited_practices_checked
risk_classification.prohibited_practices_indicators
risk_classification.high_risk_area
risk_classification.product_safety_component
risk_classification.decision_impact
risk_classification.automated_decision
risk_classification.transparency_relevant
risk_classification.gpa_ai_relevance
risk_classification.preliminary_risk_result
risk_classification.risk_classification_reasoning
```

---

## Beispiel: Dokument `05_Pflichtenmatrix.docx`

Erzeuge eine Tabelle mit diesen Spalten:

```text
Prüfpunkt
Antwort / Ergebnis
Mögliche Pflicht
Status
Nächster Schritt
```

Beispielzeilen:

```text
Rolle
Betreiber / Deployer
Betreiberpflichten prüfen
Relevant
Nutzungsrichtlinie und Schulung dokumentieren

Personenbezogene Daten
Ja
DSGVO-Schnittstellenprüfung / DSFA-Vorprüfung
Relevant
Datenschutzprüfung abschließen

Transparenzpflicht
Ja
Nutzer über KI-Einsatz informieren
Relevant
Transparenzhinweis finalisieren

Hochrisiko-Indikation
Keine unmittelbare Hochrisiko-Indikation
High-Risk-Paket derzeit nicht zwingend
Vorläufig nicht relevant
Bei Zweckänderung neu prüfen
```

---

## Beispiel: Dokument `13_Technische-Dokumentation-Annex-IV.docx`

Dieses Dokument soll mindestens enthalten:

```text
1. Zweck des Dokuments
2. Allgemeine Systembeschreibung
3. Vorgesehene Nutzung
4. Technische Architektur
5. Systemkomponenten
6. Modellinformationen
7. Entwicklungsprozess
8. Designentscheidungen
9. Eingaben und Ausgaben
10. Daten-Governance
11. Mensch-Maschine-Schnittstelle
12. Leistungsmerkmale
13. Bekannte Einschränkungen
14. Vorhersehbare Fehlanwendungen
15. Tests und Validierung
16. Risikomanagement
17. Logging und Monitoring
18. Genauigkeit, Robustheit und Cybersicherheit
19. Versionshistorie
20. Wartung und Updates
21. Offene Punkte
```

---

## Beispiel: Dokument `20_DSGVO-Schnittstellenprüfung.docx`

Dieses Dokument soll mindestens enthalten:

```text
1. Zweck des Dokuments
2. Verarbeitung personenbezogener Daten
3. Zwecke der Verarbeitung
4. Rechtsgrundlage
5. Kategorien betroffener Personen
6. Datenkategorien
7. Empfänger
8. Drittlandtransfer
9. Auftragsverarbeitung
10. Betroffenenrechte
11. Technische und organisatorische Maßnahmen
12. Speicherdauer
13. Art. 22 DSGVO Vorprüfung
14. Ergebnis
15. Offene Punkte
```

---

## Textlogik für Bewertungen

Bitte keine endgültigen rechtlichen Aussagen formulieren wie:

```text
Das System ist AI-Act-konform.
```

Stattdessen verwenden:

```text
Auf Basis der eingegebenen Informationen ergibt sich eine vorläufige Einschätzung.
```

```text
Die Dokumentation dient der strukturierten Compliance-Vorbereitung und sollte fachlich, technisch, datenschutzrechtlich und rechtlich geprüft werden.
```

```text
Eine finale Konformitätsbewertung ist erst nach vollständiger Prüfung aller Anforderungen möglich.
```

---

## README.md

Erstelle eine verständliche README mit:

```text
Projektbeschreibung
Installation
Nutzung des Web-Tools
Nutzung des Python-Generators
JSON-Struktur
Dokumentenlogik
Hinweise zur rechtlichen Prüfung
Beispielbefehle
```

Beispielbefehle:

```bash
pip install -r requirements.txt
python generator/main.py --input data/questions.json --output output/documents --zip
```

---

## Qualitätsanforderungen

Bitte achte auf:

- klare Dateinamen
- gut lesbaren Code
- robuste Fehlerbehandlung
- keine fest verdrahteten absoluten Pfade
- UTF-8-Unterstützung
- deutsche Dokumenttitel
- sinnvolle Default-Texte
- keine unnötigen externen Abhängigkeiten
- keine Cloud-Pflicht
- lokale Ausführung möglich

---

## Erste Umsetzungsschritte

Bitte arbeite in dieser Reihenfolge:

1. Projektstruktur erstellen
2. `requirements.txt` und `README.md` erstellen
3. Web-Tool erstellen
4. JSON-Loader erstellen
5. DOCX-Hilfsfunktionen erstellen
6. Dokument-Router erstellen
7. Erste fünf Dokumentgeneratoren erstellen
8. Danach restliche Dokumentgeneratoren ergänzen
9. ZIP-Export ergänzen
10. Testlauf mit `data/questions.json`

---

## Akzeptanzkriterien

Das Projekt gilt als funktionsfähig, wenn:

```text
[ ] Das Web-Tool kann questions.json laden
[ ] Das Web-Tool zeigt alle Abschnitte und Fragen an
[ ] Antworten können geändert werden
[ ] Die aktualisierte JSON kann heruntergeladen werden
[ ] Python kann die JSON laden
[ ] Python erzeugt mindestens die Basisdokumente 01–10 und 25
[ ] Python erzeugt zusätzliche Dokumente nach Router-Logik
[ ] Alle Word-Dateien sind lesbar
[ ] ZIP-Export funktioniert
[ ] README erklärt die Nutzung
```

---

## Wichtiger Hinweis für die Umsetzung

Wenn die vollständige Umsetzung aller 25 Dokumente zu groß für einen Schritt ist, beginne mit diesen Dokumenten:

```text
01_Management-Summary.docx
02_AI-System-Steckbrief.docx
03_Rollenklärung-nach-AI-Act.docx
04_Risikoklassifizierung.docx
05_Pflichtenmatrix.docx
06_Risikomanagement.docx
07_Daten-Governance.docx
08_Human-Oversight-Konzept.docx
09_Transparenz-und-Nutzerinformation.docx
10_Logging-und-Monitoring.docx
25_Dokumentations-und-Freigabevermerk.docx
```

Danach ergänze die bedingten Dokumente.
