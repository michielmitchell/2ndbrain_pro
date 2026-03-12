# filename: second_brain_builder/run.sh
# purpose: One-click runner - Delete Note button added in modal

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
echo "=== DELETE NOTE BUTTON ADDED ==="
echo "In the modal viewer (click any .md):"
echo "• Red 🗑️ Delete Note button (with confirmation)"
echo "• Instantly refreshes stats + list after delete"
"$VENV_DIR/bin/python" main.py "$@"
