"""Specific saved-record prerequisite for a decoder-bias control."""
import json
from pathlib import Path
import numpy as np
base=Path(__file__).parent; out=base/'outputs/gate_diagnostic_v1'; rows=[]
for m in ('CL','NCL'):
    a=np.load(out/(m+'_logits.npz'))
    for kind in ('actual_increment','affine_residual'):
        reference=a['clean_logits'] if kind=='actual_increment' else a['full_affine_logits']
        r=a['actual_logits'].astype(float)-reference.astype(float); r-=r.mean(-1,keepdims=True)
        global_mean=r.mean((0,1)); total=float(np.mean(r*r)); common=float(np.mean(global_mean*global_mean))
        rows.append(dict(method=m,quantity=kind,total_energy=total,common_class_shift_energy=common,
            common_fraction=common/total))
eligible=any(r['quantity']=='affine_residual' and r['common_fraction']>=.25 for r in rows)
record=dict(rows=rows,threshold=.25,global_bias_control_warranted=eligible,
    status='Post-outcome descriptive prerequisite at sigma .04; no new forwards',
    limitations='A large common class shift warrants a control but does not prove bias calibration improves error or changes model ordering.')
(out/'common_drift_check.json').write_text(json.dumps(record,indent=2)); print(json.dumps(record,indent=2))
