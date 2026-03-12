# filename: second_brain_builder/run.sh
# purpose: One-click runner - checkboxes toggle only, row click opens modal (checkbox click ignored)

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
echo "=== CHECKBOXES TOGGLE ONLY — MODAL ON ROW ELSEWHERE ==="
echo "• Click checkbox = toggle only"
echo "• Click anywhere else on row = open modal"
echo "• Select All header still works"
"$VENV_DIR/bin/python" main.py "$@"
