# filename: second_brain_builder/run.sh
# purpose: One-click runner — AI Review JSON extraction now robust (ignores extra explanation text)

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
echo "=== AI REVIEW JSON EXTRACTION FIXED ==="
echo "• Now extracts clean JSON even when Ollama adds explanation text"
echo "• Category + Confidence update instantly after every review"
"$VENV_DIR/bin/python" main.py "$@"
