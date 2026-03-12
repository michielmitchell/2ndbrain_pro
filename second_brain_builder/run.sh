# filename: second_brain_builder/run.sh
# purpose: One-click runner — "Filter thoughts..." live search box added above table

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
echo "=== FILTER THOUGHTS SEARCH BOX ADDED ==="
echo "• Live search input above the table"
echo "• Filters instantly on Thought column"
echo "• Works together with category cards"
"$VENV_DIR/bin/python" main.py "$@"
