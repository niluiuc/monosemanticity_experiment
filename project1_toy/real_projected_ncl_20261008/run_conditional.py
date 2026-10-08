"""Run only scientifically permitted stages after the clean job completes."""
import json
from pathlib import Path
import subprocess
import sys

root=Path('/scratch/idas3/ncl_projected_20261008_v1')
clean=json.loads((root/'clean_run_v1/results.json').read_text())
if not clean['clean_gates_passed']:
    print('STOP: clean prerequisites failed. Prediction and TEST were not run.',flush=True)
    raise SystemExit(0)
subprocess.run([sys.executable,str(root/'run_prediction.py'),'--root',str(root)],check=True)
prediction=json.loads((root/'prediction_run_v1/prediction.json').read_text())
if not prediction['prediction_gates_passed']:
    print('Prediction claim STOPPED: prerequisites failed. Run only the predeclared native phenomenon test.',flush=True)
subprocess.run([sys.executable,str(root/'run_test.py'),'--root',str(root)],check=True)
