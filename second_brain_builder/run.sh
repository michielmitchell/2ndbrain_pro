# filename: second_brain_builder/run.sh
# purpose: One-click runner - Avg Confidence now displayed inside each category card exactly like screenshot

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
echo "=== AVG CONFIDENCE INSIDE CATEGORY CARDS ==="
echo "Each card now shows:"
echo "• Big count"
echo "• Small green Avg Confidence (exactly like screenshot)"
echo "All inside the dashboard tab block"
"$VENV_DIR/bin/python" main.py "$@"
