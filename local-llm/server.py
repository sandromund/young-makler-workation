from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("Demo Tools")


@mcp.tool()
def addiere(a: int, b: int) -> int:
    """Addiert zwei Zahlen."""
    return a + b


@mcp.tool()
def erstelle_demo_text(thema: str, zielgruppe: str = "Versicherungsmakler") -> str:
    """Erstellt einen kurzen Demo-Text zu einem Thema für eine Zielgruppe."""
    return (
        f"Demo-Text zum Thema '{thema}' für {zielgruppe}:\n\n"
        f"In dieser Demo zeigen wir, wie ein lokales Sprachmodell über MCP "
        f"gezielt externe Python-Funktionen aufrufen kann. Das ermöglicht "
        f"strukturierte Workflows, Berechnungen und Integrationen direkt aus der Chat-Oberfläche."
    )


@mcp.tool()
def aktueller_zeitstempel() -> str:
    """Gibt den aktuellen lokalen Zeitstempel zurück."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@mcp.tool()
def lead_score(firmenname: str, mitarbeiter: int, interesse: str) -> dict:
    """Berechnet einen einfachen Demo-Lead-Score."""
    score = 0

    if mitarbeiter >= 100:
        score += 40
    elif mitarbeiter >= 25:
        score += 25
    else:
        score += 10

    if interesse.lower() in ["hoch", "sehr hoch"]:
        score += 40
    elif interesse.lower() == "mittel":
        score += 25
    else:
        score += 10

    if "versicherung" in firmenname.lower() or "makler" in firmenname.lower():
        score += 20

    return {
        "firmenname": firmenname,
        "score": min(score, 100),
        "einschaetzung": "heißer Lead" if score >= 75 else "prüfen" if score >= 45 else "niedrige Priorität",
    }


if __name__ == "__main__":
    mcp.run()