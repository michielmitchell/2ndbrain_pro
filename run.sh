# filename: run.sh
# purpose: Top-level wrapper in ~/2ndbrain_pro so you can run ./run.sh directly (delegates to second_brain_builder/run.sh)

#!/bin/bash
set -e
cd second_brain_builder || { echo "Error: second_brain_builder folder not found"; exit 1; }
exec ./run.sh "$@"
