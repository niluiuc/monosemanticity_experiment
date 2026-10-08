#!/bin/bash
#SBATCH --job-name=ncl-projected-test
#SBATCH --partition=physics
#SBATCH --account=adshead
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --no-requeue
#SBATCH --output=/scratch/idas3/ncl_projected_20261008_v1/logs/conditional-%j.out
set -euo pipefail
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8
TASK_ROOT=/scratch/idas3/ncl_projected_20261008_v1
cd "$TASK_ROOT"
"$TASK_ROOT/runtime/bin/python" -u run_conditional.py
