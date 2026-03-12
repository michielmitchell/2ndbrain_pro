# filename: second_brain_builder/run.sh
# purpose: One-click runner — Prompts Config flash fixed (tab3 now starts hidden)

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
echo "=== PROMPTS CONFIG FLASH FIXED ==="
echo "• #tab3 now starts with hidden class"
echo "• No more prompts section appearing at bottom of Dashboard on fresh load"
"$VENV_DIR/bin/python" main.py "$@"
