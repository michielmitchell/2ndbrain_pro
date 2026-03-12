# filename: second_brain_builder/run.sh
# purpose: One-click runner — all table columns now fully sortable with ↑↓ arrows

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
echo "=== ALL TABLE COLUMNS NOW FULLY SORTABLE ==="
echo "• Click any header (Thought, Category, Confidence, Date & Time)"
echo "• Numeric sort on Confidence, arrow indicators updated"
"$VENV_DIR/bin/python" main.py "$@"
