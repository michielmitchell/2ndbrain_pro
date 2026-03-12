# filename: second_brain_builder/run.sh
# purpose: One-click runner (chmod +x run.sh)

#!/bin/bash
cd "$(dirname "$0")"
pip install -r requirements.txt --quiet
python -m src.utils.folder_setup
python main.py
echo "Done - vault created."
