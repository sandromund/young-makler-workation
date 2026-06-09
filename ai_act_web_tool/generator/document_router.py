from __future__ import annotations

HIGH_RISK_RESULTS = {
    "Hochrisiko-Indikation möglich",
    "Verbotene Praxis möglich",
    "Unklar / rechtliche Prüfung erforderlich",
}

PROVIDER_ROLES = {
    "Anbieter / Provider",
    "Mehrere Rollen möglich",
    "Produkthersteller",
}

DEPLOYER_ROLES = {
    "Betreiber / Deployer",
    "Mehrere Rollen möglich",
}

ALWAYS_DOCUMENTS = [
    "01_Management-Summary.docx",
    "02_AI-System-Steckbrief.docx",
    "03_Rollenklärung-nach-AI-Act.docx",
    "04_Risikoklassifizierung.docx",
    "05_Pflichtenmatrix.docx",
    "06_Risikomanagement.docx",
    "07_Daten-Governance.docx",
    "08_Human-Oversight-Konzept.docx",
    "09_Transparenz-und-Nutzerinformation.docx",
    "10_Logging-und-Monitoring.docx",
    "25_Dokumentations-und-Freigabevermerk.docx",
]


def select_documents(answers: dict[str, str]) -> list[str]:
    documents = set(ALWAYS_DOCUMENTS)

    if answers.get("data_governance.personal_data_processed") == "Ja":
        documents.update(
            [
                "20_DSGVO-Schnittstellenprüfung.docx",
                "21_DSFA-Vorprüfung.docx",
            ]
        )

    if answers.get("risk_classification.preliminary_risk_result") in HIGH_RISK_RESULTS:
        documents.update(
            [
                "11_Genauigkeit-Robustheit-Cybersicherheit.docx",
                "12_Test-und-Validierungsbericht.docx",
                "13_Technische-Dokumentation-Annex-IV.docx",
                "18_FRIA-Vorprüfung.docx",
                "19_Grundrechte-Folgenabschätzung.docx",
            ]
        )

    primary_role = answers.get("role_assessment.primary_role", "")
    if primary_role in PROVIDER_ROLES:
        documents.update(
            [
                "13_Technische-Dokumentation-Annex-IV.docx",
                "14_Konformitätsbewertung.docx",
                "15_EU-Konformitätserklärung.docx",
                "16_Post-Market-Monitoring-Plan.docx",
                "17_Incident-Reporting-Prozess.docx",
            ]
        )

    if primary_role in DEPLOYER_ROLES:
        documents.update(
            [
                "22_Nutzungsrichtlinie-Mitarbeitende.docx",
                "23_Schulungs-und-Kompetenznachweis.docx",
                "24_Anbieter-und-Lieferantenbewertung.docx",
            ]
        )

    if answers.get("role_assessment.external_ai_service") == "Ja":
        documents.add("24_Anbieter-und-Lieferantenbewertung.docx")

    return sorted(documents)
