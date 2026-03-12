# filename: second_brain_builder/run.sh
# purpose: One-click runner with venv + reminder for Ollama (supports OLLAMA_HOST env for custom IP like screenshot)

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
echo "=== OLLAMA SETUP ==="
echo "Set custom Ollama: OLLAMA_HOST=http://192.168.3.237:11434 ./run.sh --serve"
echo "Make sure Ollama is running: ollama serve"
echo "Pull models: ollama pull llama3.2"
"$VENV_DIR/bin/python" main.py "$@"
