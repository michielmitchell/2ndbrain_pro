# filename: second_brain_builder/run.sh
# purpose: One-click runner — ensures logs/ directory exists for CLI

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
echo "=== CLI TOOL 2b+ READY ==="
echo "• Usage: 2b+ \"your thought text here\""
echo "• Example: 2b+ \"this is to show how a CLI command would look for getting a thought into the brain\""
mkdir -p logs
chmod +x 2b+
ln -sf "$(pwd)/2b+" ../2b+ 2>/dev/null || true
"$VENV_DIR/bin/python" main.py "$@"
