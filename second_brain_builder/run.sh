# filename: second_brain_builder/run.sh
# purpose: One-click runner — 'ollama' package now installed on fresh git pull (fixes vector_store init)

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
echo "=== OLLAMA PYTHON PACKAGE ADDED ==="
echo "• Fixed missing 'ollama' package on fresh git clones"
echo "• Vector store now initializes correctly"
"$VENV_DIR/bin/python" main.py "$@"
