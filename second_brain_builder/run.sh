# filename: second_brain_builder/run.sh
# purpose: One-click runner (chmod +x run.sh) - now supports --serve --port XXXX

#!/bin/bash
cd "$(dirname "$0")"
pip install -r requirements.txt --quiet
python main.py "$@"
echo "Done. For web mode: ./run.sh --serve --port 9000"
