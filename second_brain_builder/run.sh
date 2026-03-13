# filename: second_brain_builder/run.sh
# purpose: One-click runner — creates ALL missing runtime folders (logs/, vault/, vector_index/) BEFORE any Python import happens (fixes fresh clone crash forever)

#!/bin/bash
set -e

# Create required runtime directories FIRST (these are intentionally never in git)
mkdir -p logs
mkdir -p vault/notes/thoughts
mkdir -p vault/vector_index

cd "$(dirname "$0")"
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
export PYTHONPATH=.

echo "Installing/updating dependencies..."
pip install -r requirements.txt --quiet
echo "🚀 Launching Second Brain Builder"
echo "=== ALL RUNTIME FOLDERS CREATED ON FRESH CLONE ==="
echo "• logs/ vault/ vector_index/ now exist"
"$VENV_DIR/bin/python" main.py "$@"
