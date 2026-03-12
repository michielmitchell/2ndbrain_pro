# filename: second_brain_builder/run.sh
# purpose: One-click runner with automatic venv + PYTHONPATH fix for import issues

#!/bin/bash
set -e

cd "$(dirname "$0")"

VENV_DIR=".venv"

# Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment with python3..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Set Python path so src. imports work
export PYTHONPATH=.

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Run main
echo "Launching Second Brain Builder..."
"$VENV_DIR/bin/python" main.py "$@"

echo "Done."
echo "Next run will be fast (venv already exists)."
echo "To serve on custom port: ./run.sh --serve --port 8084"
