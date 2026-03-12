# filename: second_brain_builder/run.sh
# purpose: One-click runner - sortable table now filters instantly when clicking any category card

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
echo "=== SORTABLE CATEGORY TABLE READY ==="
echo "Click any category card above the table to filter instantly"
echo "Click table headers to sort by Filename/Category/Date"
echo "All fixed - no more NameError"
"$VENV_DIR/bin/python" main.py "$@"
