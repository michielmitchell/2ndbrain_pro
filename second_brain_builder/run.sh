# filename: second_brain_builder/run.sh
# purpose: One-click runner — now reminds that .gitignore is active and protects data

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
echo "=== .gitignore ACTIVE ==="
echo "• All notes, logs, .venv, and databases are now protected from git"
echo "• Only code + config is tracked"
"$VENV_DIR/bin/python" main.py "$@"
