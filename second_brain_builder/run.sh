# filename: second_brain_builder/run.sh
# purpose: One-click runner with automatic venv (fixes Debian externally-managed-environment + python not found)

#!/bin/bash
set -e

cd "$(dirname "$0")"

VENV_DIR=".venv"

# Create venv if missing (uses system python3)
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment with python3..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install requirements (inside venv, no system conflict)
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Run main with venv python (handles --serve --port etc)
echo "Launching Second Brain Builder..."
"$VENV_DIR/bin/python" main.py "$@"

echo "Done. For web mode: ./run.sh --serve --port 8084"
echo "Next run will reuse venv (fast)."
