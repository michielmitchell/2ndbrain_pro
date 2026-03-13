# filename: second_brain_builder/run.sh
# purpose: One-click runner — AI Review Threshold slider now vertical + tall on left of Prompts Config tab

#!/bin/bash
set -e
cd "$(dirname "$0")"
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
export PYTHONPATH=.
echo "Installing/updating dependencies..."
pip install -r requirements.txt --quiet
echo "🚀 Launching Second Brain Builder"
echo "=== AI REVIEW THRESHOLD SLIDER NOW VERTICAL ==="
echo "• Tall vertical slider on left of Prompts Config tab"
echo "• All other tabs/UI/table/AI Chat unchanged"
"$VENV_DIR/bin/python" main.py "$@"
