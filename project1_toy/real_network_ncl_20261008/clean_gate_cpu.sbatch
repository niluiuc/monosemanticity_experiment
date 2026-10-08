#!/bin/bash
#SBATCH --job-name=ncl-clean-gate-cpu
#SBATCH --partition=physics
#SBATCH --account=adshead
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=01:30:00
#SBATCH --no-requeue
#SBATCH --output=/scratch/idas3/ncl_native_20261008_v1/logs/clean-%j.out
set -euo pipefail
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8
TASK_ROOT=/scratch/idas3/ncl_native_20261008_v1
cd "$TASK_ROOT"
"$TASK_ROOT/runtime/bin/python" -u run_clean_gate.py --root "$TASK_ROOT"
