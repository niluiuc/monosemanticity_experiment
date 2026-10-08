#!/bin/bash
#SBATCH --job-name=ncl-clean-gate
#SBATCH --partition=secondary
#SBATCH --account=adshead
#SBATCH --gres=gpu:RTXA6000:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/idas3/ncl_native_20261008_v1/logs/clean-%j.out
set -euo pipefail
TASK_ROOT=/scratch/idas3/ncl_native_20261008_v1
export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8
cd "$TASK_ROOT"
"$TASK_ROOT/runtime/bin/python" -u run_clean_gate.py --root "$TASK_ROOT"
