#!/bin/bash
set -euo pipefail
TASK_ROOT=/scratch/idas3/ncl_native_20261008_v1
mkdir -p "$TASK_ROOT/logs"
exec 9>"$TASK_ROOT/runtime_setup.lock"
flock 9
if [ -f "$TASK_ROOT/runtime_ready.txt" ]; then exit 0; fi
if [ ! -e "$TASK_ROOT/runtime/pyvenv.cfg" ]; then
  /sw/apps/anaconda3/2024.10/bin/python -m venv "$TASK_ROOT/runtime"
fi
"$TASK_ROOT/runtime/bin/python" -m pip install --quiet numpy==2.1.3
"$TASK_ROOT/runtime/bin/python" -m pip install --quiet torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124
"$TASK_ROOT/runtime/bin/python" -c 'import torch,torchvision; print(torch.__version__,torchvision.__version__)'
date -u > "$TASK_ROOT/runtime_ready.txt"
