d #!/bin/bash

# Prüfe ob mindestens eine Textdatei als Argument übergeben wurde
if [ $# -lt 1 ]; then
    echo "Verwendung: $0 <textdatei> [Optionen]"
    echo ""
    echo "Optionen:"
    echo "  --language, -l     Sprache (de/en, Standard: de)"
    echo "  --model, -m       Ollama Modell (Standard: abhängig von Sprache)"
    echo "  --temperature, -t  Kreativität (0.0-1.0, Standard: 0.7)"
    echo "  --top-p, -p       Nucleus Sampling (0.0-1.0, Standard: 0.9)"
    echo "  --top-k, -k       Token-Kandidaten (1-100, Standard: 40)"
    echo ""
    echo "Beispiele:"
    echo "  $0 text.txt                              # Deutsche Korrektur"
    echo "  $0 text.txt --language en               # Englische Korrektur"
    echo "  $0 text.txt -l en -m llama2:70b        # Anderes Modell"
    echo "  $0 text.txt -t 0.5 -p 0.9 -k 40        # Parameter anpassen"
    exit 1
fi

# Prüfe ob die Datei existiert (erstes Argument)
if [ ! -f "$1" ]; then
    echo "Fehler: Datei '$1' existiert nicht."
    exit 1
fi

# Prüfe ob pipx installiert ist
if ! command -v pipx &> /dev/null; then
    echo "Fehler: pipx ist nicht installiert."
    echo "Bitte installieren Sie pipx mit: brew install pipx"
    exit 1
fi

# Erstelle virtuelles Environment wenn es nicht existiert
if [ ! -d "venv" ]; then
    echo "Erstelle virtuelles Environment..."
    python3 -m venv venv
fi

# Aktiviere virtuelles Environment
source venv/bin/activate

# Installiere Abhängigkeiten
echo "Installiere Abhängigkeiten..."
pip install -r requirements.txt

# Führe das Python-Skript aus
echo "Starte Textkorrektur..."
# Leite alle Argumente an das Python-Skript weiter
python text_corrector.py "$@"

# Deaktiviere virtuelles Environment
deactivate
