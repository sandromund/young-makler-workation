# Workshop-Kit: Prompt Injection im Kundendokument

Dieses Paket dient als Live-Demo fuer den Workshop "Zwischen Malediven und Justizvollzugsanstalt: KI Hacks fuer Makler".

Die Demo zeigt, dass ein normal wirkendes Kundendokument versteckte Anweisungen enthalten kann, die von einer KI beim PDF-Upload verarbeitet werden koennen.

## Enthaltene Dateien

| Datei | Zweck |
|---|---|
| `kundennotiz_malediven_jva_visible.pdf` | Sauberes sichtbares Ausgangs-PDF ohne versteckte Nachricht |
| `kundennotiz_malediven_jva_hidden.pdf` | Gleich aussehendes PDF mit versteckter Nachricht |
| `hidden_message.txt` | Versteckte Nachricht, die vom Skript eingelesen wird |
| `embed_hidden_message.py` | Python-Skript zum Einbau einer Nachricht aus einer TXT-Datei in ein PDF |
| `prompts.md` | Fertige Prompts fuer unsichere und sichere Demo-Runden |

## Schnellstart

Alle Befehle im Ordner `prompt_injection_workshop_kit` ausfuehren (dort liegt `embed_hidden_message.py`). Abhaengigkeiten stehen in `requirements.txt` im Repository-Root.

```powershell
cd prompt_injection_workshop_kit
```

Falls Sie den Ordner bereits geoeffnet haben, diesen `cd`-Befehl ueberspringen.

### 1. Virtuelle Umgebung einrichten

Unter Windows ist oft nur `py -3` verfuegbar, nicht `python`. Beide Schritte unten nutzen deshalb den Windows Python Launcher beziehungsweise die venv direkt.

```powershell
py -3 -m venv .venv
.venv/Scripts/python.exe -m pip install -r ../requirements.txt
```

Optional: `.venv/Scripts/Activate.ps1` — danach funktioniert auch `python` im gleichen Terminal.

Unter Linux oder macOS:

```bash
cd prompt_injection_workshop_kit
python3 -m venv .venv
.venv/bin/pip install -r ../requirements.txt
source .venv/bin/activate
```

### 2. Demo-PDF mit versteckter Nachricht erstellen

```powershell
.venv/Scripts/python.exe embed_hidden_message.py --input kundennotiz_malediven_jva_visible.pdf --hidden-text-file hidden_message.txt --output kundennotiz_malediven_jva_hidden.pdf --mode white
```

### 3. Komplettes Beispiel neu erzeugen

```powershell
.venv/Scripts/python.exe embed_hidden_message.py --make-sample --hidden-text-file hidden_message.txt --output kundennotiz_malediven_jva_hidden.pdf --visible-output kundennotiz_malediven_jva_visible.pdf --mode white
```

## Modi

| Modus | Beschreibung |
|---|---|
| `white` | Weisser Text auf weissem Hintergrund. Optisch unsichtbar, haeufig fuer PDF-Parser lesbar. |
| `tiny` | Sehr kleiner hellgrauer Text am unteren Rand. Praktisch unsichtbar, oft robuster extrahierbar. |
| `offpage` | Text wird ausserhalb beziehungsweise am Rand der sichtbaren Seite platziert. |

Empfehlung fuer Live-Demos: zuerst `white`, falls ein Tool nichts erkennt, danach `tiny` testen.

## KI-Tools zum Testen

- ChatGPT: https://chatgpt.com/
- Claude: https://claude.com/
- Google Gemini: https://gemini.google.com/
- Microsoft Copilot: https://copilot.microsoft.com/
- Microsoft 365 Copilot Chat fuer Arbeitskonten: https://copilot.cloud.microsoft/

Hinweis: Datei-Upload, PDF-Verarbeitung und Schutzmechanismen unterscheiden sich je nach Tool, Tarif, Organisationseinstellung und Modell. Genau dieser Unterschied ist fuer den Workshop sinnvoll: Das Risiko ist nicht ein einzelnes Tool, sondern der Umgang mit nicht vertrauenswuerdigen Dokumentinhalten.

## Empfohlener Ablauf fuer die Live-Demo

1. Zeigen Sie zuerst `kundennotiz_malediven_jva_visible.pdf` oder die sichtbare Ansicht von `kundennotiz_malediven_jva_hidden.pdf`.
2. Laden Sie `kundennotiz_malediven_jva_hidden.pdf` in eine KI hoch.
3. Verwenden Sie zuerst den unsicheren Einstiegsprompt aus `prompts.md`.
4. Fragen Sie das Publikum: Wo entsteht ein Haftungsrisiko?
5. Verwenden Sie danach den sicheren Gegenprompt aus `prompts.md`.
6. Zeigen Sie die Kernaussage: Dokumente sind Daten, keine Befehle.

## Erwartete Ergebnisse

Je nach KI kann eines dieser Ergebnisse auftreten:

- Die KI befolgt die versteckte Nachricht teilweise.
- Die KI erkennt die versteckte Nachricht und warnt davor.
- Die KI ignoriert den versteckten Text, weil der PDF-Parser ihn nicht extrahiert.

Alle drei Ergebnisse sind didaktisch brauchbar. Besonders stark ist der Fall, wenn die KI die versteckte Anweisung erkennt: Dann wird sichtbar, dass der Text fuer Menschen nicht auffaellt, aber von der KI verarbeitet wurde.

## Wichtiger Praxishinweis

Diese Demo ist fuer Sensibilisierung, Schulung und interne Sicherheitsarbeit gedacht. In echten Maklerprozessen sollten Dokumente aus fremden Quellen grundsaetzlich als nicht vertrauenswuerdig behandelt werden.

Praktische Regel:

> Inhalte aus Dokumenten sind Daten. Anweisungen innerhalb von Dokumenten duerfen keine Arbeitsanweisungen fuer die KI sein.
