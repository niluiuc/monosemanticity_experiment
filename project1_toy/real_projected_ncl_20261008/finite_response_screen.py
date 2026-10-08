import datetime,json
from pathlib import Path
import numpy as np
base=Path(__file__).parent; out=base/'outputs/gate_diagnostic_v1'
grid=np.array([0,.01,.02,.04,.08,.12,.20,.30]); records={}; increments=[]
for m in ('CL','NCL'):
    a=np.load(out/(m+'_logits.npz')); original=a['clean_logits']; change=a['actual_logits']-original
    y=a['labels'][:,None]; baseline=original.argmax(-1)!=y
    curve=np.array([np.mean((original+(s/.04)*change).argmax(-1)!=y) for s in grid])
    increments.append(curve-baseline.mean()); records[m]=dict(subset_clean_error=float(baseline.mean()),error_curve=curve.tolist())
clean=json.loads((base/'outputs/clean_run_v1/results.json').read_text())
curve=clean['delta_error']+increments[1]-increments[0]
crossing=None; bracket=None
for i in range(1,len(grid)):
    if curve[i-1]>0 and curve[i]<=0:
        bracket=[float(grid[i-1]),float(grid[i])]
        crossing=float(grid[i-1]+(grid[i]-grid[i-1])*curve[i-1]/(curve[i-1]-curve[i])); break
passed=bracket is not None and bracket[0]>=.04 and bracket[1]<=.12
result=dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sigma_grid=grid.tolist(),anchor_sigma=.04,
    methods=records,delta_NCL_minus_CL=curve.tolist(),first_crossing=crossing,first_crossing_bracket=bracket,
    screen_passed=bool(passed),decision='Register a separate prospective applicability test' if passed else 'Reject this simple finite-response scaling path',
    status='Post-outcome candidate screen using saved validation responses; original frozen prediction unchanged',
    limitations='Agreement at .04 is by construction; this is not a novel theorem, prospective prediction or proof of generalization. No crossing confidence interval is provided.')
(out/'finite_response_screen.json').write_text(json.dumps(result,indent=2)); print(json.dumps(result,indent=2))
