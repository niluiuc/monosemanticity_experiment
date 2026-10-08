#!/bin/bash
# queue runner: run_ww.sh <queue-id>
cd "$(dirname "$0")"
if [ "$1" = "A" ]; then L="0.001 0.003"; else L="0.01 0.03"; fi
for s in $L; do for c in 0 -0.002 0.002; do
  python3 well_width.py $s $c 21 > ../numerics_results/logs/ww_s${s}_c${c}.log 2>&1
done; done
