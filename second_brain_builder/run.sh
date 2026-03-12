# filename: second_brain_builder/run.sh
# purpose: One-click runner - dashboard now shows the exact AI categories (People, Projects, Ideas, Admin, Review) with live counts

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
echo "=== AI CATEGORY DASHBOARD FIXED ==="
echo "Cards now show the exact categories the AI sorts thoughts into:"
echo "• Total Thoughts"
echo "• People"
echo "• Projects"
echo "• Ideas"
echo "• Admin"
echo "• Review"
echo "All counts update instantly after every save"
"$VENV_DIR/bin/python" main.py "$@"
