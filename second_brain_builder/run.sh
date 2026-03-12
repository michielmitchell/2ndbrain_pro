# filename: second_brain_builder/run.sh
# purpose: One-click runner - Prompts Config now has silent saves (no popups) and confirm() only for destructive Reset actions

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
echo "=== Prompts Config updated ==="
echo "• Save actions are now silent (no alerts)"
echo "• Only destructive Reset actions show confirm()"
"$VENV_DIR/bin/python" main.py "$@"
