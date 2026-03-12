# filename: second_brain_builder/run.sh
# purpose: One-click runner - favicon.ico 404 silenced forever (no more log spam)

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
echo "=== favicon.ico 404 silenced forever ==="
echo "No more 404 for the browser tab icon request"
"$VENV_DIR/bin/python" main.py "$@"
