"""Validation-only native-classifier prediction, conditional on frozen clean gates."""
import argparse, datetime, json
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torchvision.datasets import CIFAR100
from torchvision.transforms import ToTensor
from run_clean_gate import SEED, MEAN, STD, NAMES, make_backbone, digest, save

GRID=np.array([0,.01,.02,.04,.08,.12,.20,.30])

class Classifier(nn.Module):
    def __init__(self, root, method, device):
        super().__init__()
        self.backbone=make_backbone(root/'checkpoints'/NAMES[method],device)
        probe=torch.load(root/'clean_run_v1'/method/'probe.pt',map_location='cpu',weights_only=True)
        self.head=nn.Linear(512,100); self.head.load_state_dict(probe['state_dict'])
        self.register_buffer('feature_mean',probe['mean'])
        self.register_buffer('feature_std',probe['std'])
        self.register_buffer('pixel_mean',torch.tensor(MEAN).view(1,3,1,1))
        self.register_buffer('pixel_std',torch.tensor(STD).view(1,3,1,1))
        self.to(device).eval()
        for p in self.parameters(): p.requires_grad_(False)
    def forward(self,x):
        f=self.backbone((x-self.pixel_mean)/self.pixel_std)
        return self.head((f-self.feature_mean)/self.feature_std)

def crossing(curve):
    for i in range(1,len(GRID)):
        if curve[i-1]>0 and curve[i]<=0:
            return float(GRID[i-1]+(GRID[i]-GRID[i-1])*curve[i-1]/(curve[i-1]-curve[i])),i
    return None,None

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--root',type=Path,required=True)
    root=parser.parse_args().root
    clean=json.loads((root/'clean_run_v1/results.json').read_text())
    if not clean['clean_gates_passed']: raise RuntimeError('Clean prerequisites failed; prediction forbidden.')
    out=root/'prediction_run_v1'; out.mkdir(exist_ok=False)
    device='cuda' if torch.cuda.is_available() else 'cpu'
    torch.set_num_threads(8); torch.backends.cuda.matmul.allow_tf32=False; torch.backends.cudnn.allow_tf32=False
    split=np.load(root/'clean_run_v1/split_indices.npz')
    ids=split['validation'].reshape(100,50)[:,:5].reshape(-1)
    ds=CIFAR100(str(root/'data'),train=True,download=False,transform=ToTensor())
    labels=np.array(ds.targets)[ids]
    save(out/'provenance.json',dict(start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        script_sha256=digest(__file__),protocol_sha256=digest(root/'PROTOCOL.md'),
        clean_results_sha256=digest(root/'clean_run_v1/results.json'),test_images_evaluated=0,
        directions_per_image=32,seed=SEED+2,relative_residual_definition='RMS centered logit residual / RMS centered true logit increment, aggregated over images, directions and classes; no division per image.'))
    methods={}; predicted=[]; gates=[]
    for method in NAMES:
        model=Classifier(root,method,device)
        generator=torch.Generator(device=device).manual_seed(SEED+2)
        affine=[]; clean_err=[]; actual={.01:[],.04:[]}; residual_sum=0.; increment_sum=0.
        for start in range(0,len(ids),8):
            batch=ids[start:start+8]
            x=torch.stack([ds[int(i)][0] for i in batch]).to(device)
            y=torch.tensor(labels[start:start+len(batch)],device=device)
            expanded=x[:,None].expand(-1,32,-1,-1,-1).reshape(-1,3,32,32)
            z=torch.randn(expanded.shape,generator=generator,device=device)
            with torch.no_grad():
                logits,tangent=torch.func.jvp(model,(expanded,),(z,))
                base=(logits.argmax(1)!=y.repeat_interleave(32)).view(len(batch),32)
                errs=torch.stack([(logits+float(s)*tangent).argmax(1)!=y.repeat_interleave(32) for s in GRID],dim=-1)
                affine.append(errs.view(len(batch),32,len(GRID)).cpu().numpy()); clean_err.append(base[:,0].cpu().numpy())
                for sigma in actual:
                    value=model(expanded+sigma*z)
                    actual[sigma].append((value.argmax(1)!=y.repeat_interleave(32)).view(len(batch),32).cpu().numpy())
                    if sigma==.04:
                        residual=value-logits-sigma*tangent; increment=value-logits
                        residual-=residual.mean(1,keepdim=True); increment-=increment.mean(1,keepdim=True)
                        residual_sum+=float(residual.square().sum()); increment_sum+=float(increment.square().sum())
            if start%80==0: print(method,'validation directions',start,len(ids),flush=True)
        affine=np.concatenate(affine); ce=np.concatenate(clean_err); actual={str(s):np.concatenate(v) for s,v in actual.items()}
        discrepancies={s:float(abs(v.mean()-affine[:,:,np.flatnonzero(GRID==float(s))[0]].mean())) for s,v in actual.items()}
        relative=float(np.sqrt(residual_sum/max(increment_sum,1e-30)))
        gate=all(v<=.02 for v in discrepancies.values()) and relative<=.25
        methods[method]=dict(affine_error_curve=affine.mean((0,1)).tolist(),actual_validation_errors={s:float(v.mean()) for s,v in actual.items()},
            mean_error_discrepancies=discrepancies,relative_rms_logit_residual=relative,linearization_gate_passed=gate)
        np.savez(out/(method+'_validation.npz'),image_indices=ids,labels=labels,affine_errors=affine,clean_errors=ce,**{'actual_'+s:v for s,v in actual.items()})
        predicted.append(affine.mean(1)-ce[:,None]); gates.append(gate)
        del model; torch.cuda.empty_cache() if device=='cuda' else None
    increments=predicted[1]-predicted[0]
    curve=clean['delta_error']+increments.mean(0)
    point,bracket=crossing(curve)
    # Pair subset and full validation baseline in the same within-class bootstrap.
    cl=np.load(root/'clean_run_v1/CL/validation_predictions.npz')['errors']
    ncl=np.load(root/'clean_run_v1/NCL/validation_predictions.npz')['errors']
    full_delta=(ncl.astype(float)-cl.astype(float)).reshape(100,50)
    rng=np.random.default_rng(SEED+3); draws=[]; roots=[]
    for b in range(2000):
        counts=np.stack([rng.multinomial(50,np.full(50,.02)) for _ in range(100)])
        baseline=(counts*full_delta).sum()/5000
        # The predetermined first-five subset retains counts from the full paired bootstrap.
        weights=counts[:,:5].reshape(-1); inc=(weights[:,None]*increments).sum(0)/max(weights.sum(),1)
        draw=baseline+inc; draws.append(draw); roots.append(crossing(draw)[0])
    valid=np.array([v for v in roots if v is not None]); ci=np.quantile(valid,[.025,.975]).tolist() if len(valid)==2000 else None
    precise=point is not None and ci is not None and (ci[1]-ci[0])/2<=.20*point
    passed=all(gates) and precise
    result=dict(methods=methods,sigma_grid=GRID.tolist(),delta_error_prediction=curve.tolist(),predicted_crossing=point,
        crossing_grid_index=bracket,crossing_ci95=ci,bootstrap_crossings_found=len(valid),prediction_precision_passed=precise,
        all_linearization_gates_passed=all(gates),prediction_gates_passed=passed,
        decision='Predictive claim eligible; proceed to frozen TEST evaluation' if passed else 'Predictive claim rejected; native phenomenon test remains eligible under pre-outcome amendment',test_images_evaluated=0,
        limitations='One fixed checkpoint pair. Linearization is an approximation; bootstrap uncertainty is conditional on fitted models. No test data used.')
    np.savez(out/'bootstrap_curves.npz',curves=np.array(draws)); save(out/'prediction.json',result)
    save(out/'frozen_prediction_hash.json',dict(sha256=digest(out/'prediction.json'),frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__': main()
