# filename: second_brain_builder/run.sh
# purpose: One-click runner — Drop a new thought now ultra-tight (exact latest screenshot)

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
echo "=== DROP NEW THOUGHT NOW ULTRA-TIGHT (exact latest screenshot) ==="
echo "• Title + Save button on same top row"
echo "• Textarea directly below (much shorter)"
echo "• Reply box right"
echo "• Table now shows many more rows"
"$VENV_DIR/bin/python" main.py "$@"
