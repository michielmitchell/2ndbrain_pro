# filename: second_brain_builder/run.sh
# purpose: One-click runner - re import fixed, category totals now correct

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
echo "=== RE IMPORT FIXED + TOTALS CORRECT ==="
echo "• All category cards now show real live counts"
echo "• Avg Confidence updates instantly"
echo "• NameError resolved"
"$VENV_DIR/bin/python" main.py "$@"
