# filename: second_brain_builder/run.sh
# purpose: One-click runner - guaranteed real model names now (qwen3.5:27b etc.)

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
echo "=== MODEL NAMES FIXED ==="
echo "Table will now show real names: qwen3.5:27b, deepseek-r1:8B etc."
echo "Refresh the Models Config tab if needed."
"$VENV_DIR/bin/python" main.py "$@"
