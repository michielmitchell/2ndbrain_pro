# filename: second_brain_builder/run.sh
# purpose: One-click runner — Confidence Threshold ONLY for AI Review decision (injected into prompt)

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
echo "=== CONFIDENCE THRESHOLD ONLY FOR AI ==="
echo "• Injected into Categorization Prompt"
echo "• AI decides Review bucket"
echo "• Removed from all defaults/fallbacks"
"$VENV_DIR/bin/python" main.py "$@"
