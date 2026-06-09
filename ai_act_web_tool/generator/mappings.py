from __future__ import annotations

DOCUMENT_CONFIG: dict[str, dict] = {
    "01_Management-Summary.docx": {
        "title": "Management Summary",
        "purpose": "Managementübersicht zur AI-Act-Dokumentation und zum Umsetzungsstand.",
        "sections": ["company", "ai_system_profile", "role_assessment", "risk_classification", "documentation_governance"],
    },
    "02_AI-System-Steckbrief.docx": {
        "title": "AI-System-Steckbrief",
        "purpose": "Zentrale Beschreibung des KI-Systems, seines Zwecks und seiner Einordnung.",
        "sections": ["ai_system_profile", "technical_architecture"],
    },
    "03_Rollenklärung-nach-AI-Act.docx": {
        "title": "Rollenklärung nach AI-Act",
        "purpose": "Einordnung der Organisation und des KI-Systems in die AI-Act-Rollen.",
        "sections": ["role_assessment", "deployer_obligations"],
    },
    "04_Risikoklassifizierung.docx": {
        "title": "Risikoklassifizierung",
        "purpose": "Vorläufige Risikoeinordnung des KI-Systems nach AI-Act.",
        "sections": ["risk_classification"],
    },
    "05_Pflichtenmatrix.docx": {
        "title": "Pflichtenmatrix",
        "purpose": "Zuordnung relevanter AI-Act-Pflichten zu Rollen und Verantwortlichkeiten.",
        "sections": ["role_assessment", "deployer_obligations", "risk_classification"],
    },
    "06_Risikomanagement.docx": {
        "title": "Risikomanagement",
        "purpose": "Dokumentation des Risikomanagement-Ansatzes für das KI-System.",
        "sections": ["risk_management"],
    },
    "07_Daten-Governance.docx": {
        "title": "Daten-Governance",
        "purpose": "Beschreibung der Datenverarbeitung, Datenqualität und Governance-Maßnahmen.",
        "sections": ["data_governance"],
    },
    "08_Human-Oversight-Konzept.docx": {
        "title": "Human-Oversight-Konzept",
        "purpose": "Konzept zur menschlichen Aufsicht und Kontrolle der KI-Ergebnisse.",
        "sections": ["human_oversight"],
    },
    "09_Transparenz-und-Nutzerinformation.docx": {
        "title": "Transparenz und Nutzerinformation",
        "purpose": "Information der Nutzer und Betroffenen über den KI-Einsatz.",
        "sections": ["transparency_information"],
    },
    "10_Logging-und-Monitoring.docx": {
        "title": "Logging und Monitoring",
        "purpose": "Protokollierung, Überwachung und Nachvollziehbarkeit des KI-Systems.",
        "sections": ["logging_monitoring"],
    },
    "11_Genauigkeit-Robustheit-Cybersicherheit.docx": {
        "title": "Genauigkeit, Robustheit und Cybersicherheit",
        "purpose": "Technische Anforderungen an Zuverlässigkeit, Robustheit und Sicherheit.",
        "sections": ["accuracy_robustness_cybersecurity", "technical_architecture"],
    },
    "12_Test-und-Validierungsbericht.docx": {
        "title": "Test- und Validierungsbericht",
        "purpose": "Dokumentation von Tests, Validierung und Qualitätssicherung.",
        "sections": ["testing_validation"],
    },
    "13_Technische-Dokumentation-Annex-IV.docx": {
        "title": "Technische Dokumentation (Annex IV)",
        "purpose": "Technische Dokumentation gemäß Annex IV des AI Act.",
        "sections": ["annex_iv_technical_documentation", "technical_architecture", "ai_system_profile"],
    },
    "14_Konformitätsbewertung.docx": {
        "title": "Konformitätsbewertung",
        "purpose": "Vorläufige Dokumentation der Konformitätsbewertung.",
        "sections": ["conformity_assessment"],
    },
    "15_EU-Konformitätserklärung.docx": {
        "title": "EU-Konformitätserklärung",
        "purpose": "Entwurf bzw. Vorbereitung der EU-Konformitätserklärung.",
        "sections": ["eu_declaration", "conformity_assessment"],
    },
    "16_Post-Market-Monitoring-Plan.docx": {
        "title": "Post-Market-Monitoring-Plan",
        "purpose": "Plan zur Überwachung des KI-Systems nach dem Einsatz.",
        "sections": ["post_market_monitoring"],
    },
    "17_Incident-Reporting-Prozess.docx": {
        "title": "Incident-Reporting-Prozess",
        "purpose": "Prozess zur Meldung schwerwiegender Vorfälle und Vorfälle.",
        "sections": ["incident_reporting"],
    },
    "18_FRIA-Vorprüfung.docx": {
        "title": "FRIA-Vorprüfung",
        "purpose": "Vorprüfung, ob eine Fundamental Rights Impact Assessment erforderlich ist.",
        "sections": ["fria_fundamental_rights"],
    },
    "19_Grundrechte-Folgenabschätzung.docx": {
        "title": "Grundrechte-Folgenabschätzung",
        "purpose": "Grundrechtebezogene Folgenabschätzung des KI-Systems.",
        "sections": ["fria_fundamental_rights"],
    },
    "20_DSGVO-Schnittstellenprüfung.docx": {
        "title": "DSGVO-Schnittstellenprüfung",
        "purpose": "Prüfung der Schnittstellen zwischen AI Act und DSGVO.",
        "sections": ["gdpr_dpia", "data_governance"],
    },
    "21_DSFA-Vorprüfung.docx": {
        "title": "DSFA-Vorprüfung",
        "purpose": "Vorprüfung, ob eine Datenschutz-Folgenabschätzung erforderlich ist.",
        "sections": ["gdpr_dpia", "data_governance"],
    },
    "22_Nutzungsrichtlinie-Mitarbeitende.docx": {
        "title": "Nutzungsrichtlinie für Mitarbeitende",
        "purpose": "Regeln für den sicheren und complianten Einsatz des KI-Systems.",
        "sections": ["employee_policy_training"],
    },
    "23_Schulungs-und-Kompetenznachweis.docx": {
        "title": "Schulungs- und Kompetenznachweis",
        "purpose": "Dokumentation von Schulungen und Kompetenzanforderungen.",
        "sections": ["employee_policy_training"],
    },
    "24_Anbieter-und-Lieferantenbewertung.docx": {
        "title": "Anbieter- und Lieferantenbewertung",
        "purpose": "Bewertung externer KI-Anbieter und relevanter Lieferanten.",
        "sections": ["supplier_assessment", "role_assessment"],
    },
    "25_Dokumentations-und-Freigabevermerk.docx": {
        "title": "Dokumentations- und Freigabevermerk",
        "purpose": "Freigabe, Versionierung und Governance der Dokumentation.",
        "sections": ["documentation_governance"],
    },
}
