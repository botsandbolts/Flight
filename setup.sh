#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python -m pip install -r requirements.txt
if [[ "${1:-full}" != "--base" ]]; then
  python -m pip install 'torch>=2.4,<3' --index-url https://download.pytorch.org/whl/cpu
  python -m pip install -r requirements-ml.txt
fi
