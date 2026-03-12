# filename: second_brain_builder/run.sh
# purpose: One-click runner - Thoughts list now shows real note names (fixed {n.name} placeholders)

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
echo "=== Thoughts list FIXED ==="
echo "Bottom grid now shows real thought file names (no more {n.name} placeholders)"
echo "Search also works"
"$VENV_DIR/bin/python" main.py "$@"
