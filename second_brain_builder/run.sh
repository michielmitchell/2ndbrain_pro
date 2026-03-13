# filename: second_brain_builder/run.sh
# purpose: One-click runner — averages in category cards now correct + full modular structure

#!/bin/bash
set -e
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
echo "=== CATEGORY CARD AVERAGES NOW CORRECT ==="
echo "• Projects/Ideas/Admin/etc. now show real avg confidence"
echo "• Full modular structure (helpers + routes + frontend + app)"
"$VENV_DIR/bin/python" main.py "$@"
