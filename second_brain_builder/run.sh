# filename: second_brain_builder/run.sh
# purpose: One-click runner - sidebar now properly highlights the ACTIVE tab (Dashboard no longer permanently focused)

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
echo "=== Sidebar active tab FIXED ==="
echo "The currently selected tab now has proper focus highlight"
"$VENV_DIR/bin/python" main.py "$@"
