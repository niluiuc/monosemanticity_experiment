"""Create a separate source-justified projected-representation experiment; retain v1."""
from pathlib import Path
old=Path(__file__).parent; new=old.parent/'real_projected_ncl_20261008'; new.mkdir(exist_ok=False)
text=(old/'run_clean_gate.py').read_text()
text=text.replace('def make_backbone(path,device):','def make_image_backbone(path,device):')
needle='    return model.eval().to(device)\n'
extra='''
PRIOR_ROOT=Path('/scratch/idas3/ncl_native_20261008_v1')
def make_projector(path,device):
    ck=torch.load(path,map_location='cpu',weights_only=True)
    state={k.removeprefix('projector.'):v for k,v in ck['state_dict'].items() if k.startswith('projector.')}
    assert state['0.weight'].shape==(2048,512) and state['2.weight'].shape==(256,2048)
    projector=nn.Sequential(nn.Linear(512,2048),nn.ReLU(),nn.Linear(2048,256))
    projector.load_state_dict(state,strict=True)
    final=nn.ReLU() if path.name==NAMES['NCL'] else nn.Identity()
    model=nn.Sequential(projector,final).eval().to(device)
    for p in model.parameters(): p.requires_grad_(False)
    return model

def make_backbone(path,device):
    return nn.Sequential(make_image_backbone(path,device),make_projector(path,device)).eval()
'''
assert text.count(needle)==1; text=text.replace(needle,needle+extra)
text=text.replace('head=nn.Linear(512,100)','head=nn.Linear(features.shape[1],100)')
text=text.replace('counts=torch.zeros(100,512,device=f.device)','counts=torch.zeros(100,features.shape[1],device=f.device)')
text=text.replace("train=True,download=True", "train=True,download=False")
text=text.replace("model=make_backbone(root/'checkpoints'/name,device)","model=make_projector(root/'checkpoints'/name,device)")
needle="        f,y=extract(model,ds,device); np.savez(sub/'clean_train_features.npz',features=f.numpy(),labels=y.numpy())"
replacement="""        cached=np.load(PRIOR_ROOT/'clean_run_v1'/method/'clean_train_features.npz')
        raw=cached['features']; y=torch.tensor(cached['labels'])
        assert np.array_equal(y.numpy(),targets)
        with torch.inference_mode():
            f=torch.cat([model(torch.tensor(batch,device=device)).cpu() for batch in np.array_split(raw,100)])
        np.savez(sub/'clean_train_features.npz',features=f.numpy(),labels=y.numpy())
        del raw,cached
"""
assert needle in text; text=text.replace(needle,replacement)
text=text.replace("images_evaluated='TRAIN only; no TEST'", "images_evaluated='TRAIN only; no TEST',representation='Frozen native projector; CL signed output; NCL ReLU output',parent_clean_result_sha256=digest(PRIOR_ROOT/'clean_run_v1/results.json'),anchor_source_commit='d8519e994d8e0ccc98ad6d55978c58d70c72421e'")
(new/'run_clean_gate.py').write_text(text)
prediction=(old/'run_prediction.py').read_text().replace('self.head=nn.Linear(512,100)','self.head=nn.Linear(256,100)')
(new/'run_prediction.py').write_text(prediction)
for name in ('run_test.py','verify_saved_outputs.py','plot_saved_outputs.py','audit_consistency.py'):
    (new/name).write_bytes((old/name).read_bytes())
conditional=(old/'run_conditional.py').read_text().replace('/scratch/idas3/ncl_native_20261008_v1','/scratch/idas3/ncl_projected_20261008_v1')
(new/'run_conditional.py').write_text(conditional)
sbatch=(old/'clean_gate_cpu.sbatch').read_text().replace('ncl_native_20261008_v1','ncl_projected_20261008_v1').replace('ncl-clean-gate-cpu','ncl-projected-clean')
(new/'clean.sbatch').write_text(sbatch)
conditional_batch=sbatch.replace('ncl-projected-clean','ncl-projected-test').replace('run_clean_gate.py --root "$TASK_ROOT"','run_conditional.py').replace('--time=01:30:00','--time=02:00:00').replace('/logs/clean-%j.out','/logs/conditional-%j.out')
(new/'conditional.sbatch').write_text(conditional_batch)
protocol=(old/'PROTOCOL.md').read_text()
protocol=protocol.replace('# Native CIFAR-100 phase-boundary test — v1','# Native projected-representation test — separate follow-up')
protocol=protocol.replace('512-dimensional pooled features','the actual trained 2048-hidden/256-output projector; CL uses its signed output and NCL uses ReLU of its output')
protocol=protocol.replace('Projection-head semantic consistency is not substituted for backbone consistency.', 'The classifier and consistency calculation both use this same 256-dimensional representation. This is a separate experiment motivated by the anchor code, not a successful continuation of the failed backbone test.')
protocol=protocol.replace('512-dimensional backbone features','256-dimensional projected features').replace('Backbone parameters stay frozen.','Backbone and projector parameters stay frozen.')
protocol=protocol.replace('No representation substitution after failure.','No further representation substitution after failure of this source-specified follow-up.')
protocol=protocol.replace('No backbone training, width sweep','No backbone or projector training, width sweep')
protocol=protocol.replace("Prefer the user's existing GPU runtime and secondary Slurm partition.","Use the existing isolated runtime and Physics CPU allocation, whose availability was verified. Record device and timing.")
protocol+='''

## Specific justification, interpretation and final stopping decision

The prior backbone-only experiment failed both clean prerequisites and remains recorded in real_network_ncl_20261008. Inspection of the anchor repository at commit d8519e994d8e0ccc98ad6d55978c58d70c72421e establishes that solo/methods/linear.py forward applies backbone, then projector, then ReLU when non_neg is set. Its CIFAR configs enable non_neg for NCL and leave CL signed. The predecessor main_eval.py likewise scores model output z and applies ReLU for the NCL checkpoint. Therefore the smallest necessary correction is one separate experiment on that explicitly defined native representation, not a search among arbitrary heads.

Use the actual released checkpoint projector shapes (hidden 2048, output 256), not the larger projector in the anchor's unreleased runs. No exact numerical reproduction of the anchor is claimed. Reuse the hash-verified cached clean backbone features and identical FIT/VALIDATION indices; apply the strictly loaded native projector to them. For corrupted images, execute the complete backbone-plus-projector-plus-clean-probe network, with NCL ReLU. No toy compressor or synthetic feature replacement is introduced.

This layer decision is made after observing the backbone failure but before computing projected features. It is a source-justified follow-up, not a retrospectively preregistered choice for the original experiment. The official TEST images remain unscored. No further heads, checkpoints, thresholds, noise grids or probes will be tried after this follow-up fails. Any successful crossing is one native-network observation, not proof of a monosemanticity cause, the toy exponent, a general phase diagram, or ICML acceptance. A failed result is retained in full.
'''
(new/'PROTOCOL.md').write_text(protocol)
print(new)
