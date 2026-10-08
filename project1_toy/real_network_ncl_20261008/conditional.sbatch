#!/bin/bash
#SBATCH --job-name=ncl-conditional
#SBATCH --partition=secondary
#SBATCH --account=adshead
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/idas3/ncl_native_20261008_v1/logs/conditional-%j.out
set -euo pipefail
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8
TASK_ROOT=/scratch/idas3/ncl_native_20261008_v1
cd "$TASK_ROOT"
"$TASK_ROOT/runtime/bin/python" -u run_conditional.py
