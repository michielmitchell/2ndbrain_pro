# filename: second_brain_builder/run.sh
# purpose: One-click runner — AI Review now robustly renames files + LIVE table/stats update after every thought

#!/bin/bash
set -e
cd "$(dirname "$0")"
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
export PYTHONPATH=.
echo "Installing/updating dependencies..."
pip install -r requirements.txt --quiet
echo "🚀 Launching Second Brain Builder"
echo "=== AI REVIEW NOW UPDATES BRAIN MEMORY LIVE ==="
echo "• Robust rename for legacy files"
echo "• Table + stats refresh after EVERY thought"
echo "• Category and confidence now correct instantly"
"$VENV_DIR/bin/python" main.py "$@"
