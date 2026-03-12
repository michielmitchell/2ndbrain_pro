# filename: second_brain_builder/run.sh
# purpose: One-click runner - checkboxes kept, bulk bar removed, SyntaxWarning fixed

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
echo "=== CHECKBOXES KEPT — NO BULK BAR — WARNINGS FIXED ==="
echo "• Left column checkboxes + Select All header"
echo "• No pop-up bar = zero screen jump"
echo "• All regex escapes corrected"
"$VENV_DIR/bin/python" main.py "$@"
