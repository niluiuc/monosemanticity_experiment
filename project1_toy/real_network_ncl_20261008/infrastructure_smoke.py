"""Dummy-input software check; no research images or risk measurements."""
import json
from pathlib import Path
import torch
from run_clean_gate import make_backbone,NAMES

torch.set_num_threads(2)
torch.manual_seed(1)
model=make_backbone(Path('C:/Users/indra/.cache/monosemanticity_ncl_20261008/checkpoints')/NAMES['CL'],'cpu')
x=torch.rand(2,3,32,32); z=torch.randn_like(x)
with torch.no_grad():
    value,direction=torch.func.jvp(model,(x,),(z,))
assert value.shape==direction.shape==(2,512)
assert torch.isfinite(value).all() and torch.isfinite(direction).all()
record=dict(check='Dummy inputs only: torchvision checkpoint loading and torch.func.jvp compatibility',
            torch=torch.__version__,shape=list(value.shape),finite=True,scientific_images_scored=0,
            limitation='Local CPU smoke check, not an equivalence check against the cluster GPU runtime or evidence about robustness.')
Path(__file__).with_name('infrastructure_smoke.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record,indent=2))
