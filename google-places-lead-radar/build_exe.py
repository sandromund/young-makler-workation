"""
Erstellt aus main.py ein ausführbares Programm.

Voraussetzung:
    pip install -r requirements.txt

Start:
    python build_exe.py

Ergebnis:
    release/GooglePlacesLeadRadar/GooglePlacesLeadRadar.exe   Windows
    release/GooglePlacesLeadRadar/GooglePlacesLeadRadar       macOS/Linux
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
APP_NAME = "GooglePlacesLeadRadar"
MAIN_FILE = PROJECT_DIR / "main.py"
DIST_DIR = PROJECT_DIR / "dist"
BUILD_DIR = PROJECT_DIR / "build"
RELEASE_ROOT = PROJECT_DIR / "release"
RELEASE_DIR = RELEASE_ROOT / APP_NAME
SPEC_FILE = PROJECT_DIR / f"{APP_NAME}.spec"

# Schutz gegen überfrachtete Shared-Venvs (z. B. torch, scipy aus data-science).
# main.py braucht nur requests, python-dotenv und openpyxl.
EXCLUDED_MODULES = [
    "torch",
    "torchvision",
    "tensorflow",
    "scipy",
    "matplotlib",
    "pandas",
    "numpy",
    "IPython",
    "jupyter",
    "notebook",
    "pyarrow",
    "numba",
    "llvmlite",
    "sqlalchemy",
    "botocore",
    "boto3",
    "sklearn",
    "skimage",
    "cv2",
    "PIL",
    "lxml",
    "zmq",
    "jedi",
    "parso",
    "rich",
    "fsspec",
    "cryptography",
    "google",
    "grpc",
]


def run_command(command: list[str]) -> None:
    """Führt einen Konsolenbefehl aus und bricht bei Fehlern verständlich ab."""
    print("Befehl:", " ".join(command))
    result = subprocess.run(command, cwd=PROJECT_DIR)
    if result.returncode != 0:
        raise RuntimeError(f"Der Befehl ist fehlgeschlagen: {' '.join(command)}")


def ensure_main_file_exists() -> None:
    if not MAIN_FILE.exists():
        raise FileNotFoundError("main.py wurde nicht gefunden. Bitte starten Sie build_exe.py im Projektordner.")


def ensure_pyinstaller_available() -> None:
    """Prüft, ob PyInstaller installiert ist."""
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--version"],
        cwd=PROJECT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "PyInstaller ist nicht installiert.\n\n"
            "Bitte führen Sie zuerst aus:\n"
            "    pip install -r requirements.txt\n\n"
            "Danach starten Sie erneut:\n"
            "    python build_exe.py"
        )


def clean_old_build_files() -> None:
    """Entfernt alte Build-Artefakte, damit das Ergebnis eindeutig ist."""
    for path in [DIST_DIR, BUILD_DIR, RELEASE_DIR, SPEC_FILE]:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def build_executable() -> Path:
    """Erstellt die ausführbare Datei mit PyInstaller."""
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--clean",
        "--noconfirm",
        "--log-level",
        "WARN",
        "--name",
        APP_NAME,
    ]

    for module_name in EXCLUDED_MODULES:
        command.extend(["--exclude-module", module_name])

    command.append(str(MAIN_FILE))

    run_command(command)

    executable_name = f"{APP_NAME}.exe" if sys.platform.startswith("win") else APP_NAME
    executable_path = DIST_DIR / executable_name

    if not executable_path.exists():
        raise FileNotFoundError(f"Die ausführbare Datei wurde nicht gefunden: {executable_path}")

    return executable_path


def create_release_folder(executable_path: Path) -> Path:
    """Kopiert die fertige Datei und benötigte Beispieldateien in einen Release-Ordner."""
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)

    target_executable = RELEASE_DIR / executable_path.name
    shutil.copy2(executable_path, target_executable)

    files_to_copy = [
        "input.txt",
        ".env.example",
        "README.md",
    ]

    for file_name in files_to_copy:
        source = PROJECT_DIR / file_name
        if source.exists():
            shutil.copy2(source, RELEASE_DIR / file_name)

    (RELEASE_DIR / "output").mkdir(exist_ok=True)

    info_file = RELEASE_DIR / "START_HIER.txt"
    info_file.write_text(
        "Google Places Lead-Radar\n"
        "========================\n\n"
        "1. Kopieren Sie .env.example und nennen Sie die Kopie .env\n"
        "2. Tragen Sie in .env Ihren Google Places API-Key ein\n"
        "3. Bearbeiten Sie input.txt mit Ihren Suchbegriffen\n"
        "4. Starten Sie die ausführbare Datei\n"
        "5. Die Excel-Datei wird im Ordner output gespeichert\n\n"
        "Wichtig: Die Datei .env darf nicht öffentlich geteilt werden.\n",
        encoding="utf-8",
    )

    return RELEASE_DIR


def create_release_zip(release_dir: Path) -> Path:
    """Erstellt zusätzlich eine ZIP-Datei aus dem Release-Ordner."""
    zip_base_name = RELEASE_ROOT / APP_NAME
    zip_path = shutil.make_archive(str(zip_base_name), "zip", root_dir=release_dir)
    return Path(zip_path)


def main() -> None:
    print("Build startet...")

    try:
        ensure_main_file_exists()
        ensure_pyinstaller_available()
        clean_old_build_files()
        executable_path = build_executable()
        release_dir = create_release_folder(executable_path)
        zip_path = create_release_zip(release_dir)
    except Exception as error:
        print("\nFehler beim Erstellen des Programms:")
        print(error)
        sys.exit(1)

    print("\nFertig.")
    print(f"Ausführbare Datei: {release_dir / executable_path.name}")
    print(f"Release-ZIP: {zip_path}")


if __name__ == "__main__":
    main()
