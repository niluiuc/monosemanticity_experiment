"""One frozen native-network corruption test; requires prediction gates to pass."""
import argparse, datetime, json
from pathlib import Path
import numpy as np
import torch
from torchvision.datasets import CIFAR100
from torchvision.transforms import ToTensor
from run_clean_gate import SEED, NAMES, digest, save
from run_prediction import Classifier, GRID, crossing

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--root',type=Path,required=True)
    root=parser.parse_args().root
    predpath=root/'prediction_run_v1/prediction.json'
    prediction=json.loads(predpath.read_text())
    frozen=json.loads((predpath.parent/'frozen_prediction_hash.json').read_text())
    if digest(predpath)!=frozen['sha256']: raise RuntimeError('Frozen prediction hash mismatch.')
    if not prediction['prediction_gates_passed']: raise RuntimeError('Prediction prerequisites failed; TEST forbidden.')
    out=root/'test_run_v1'; out.mkdir(exist_ok=False)
    save(out/'provenance.json',dict(start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        script_sha256=digest(__file__),protocol_sha256=digest(root/'PROTOCOL.md'),prediction_sha256=frozen['sha256'],
        prediction_frozen_utc=frozen['frozen_utc'],seed=SEED+4,directions_per_image=3))
    ds=CIFAR100(str(root/'data'),train=False,download=False,transform=ToTensor())
    labels=np.array(ds.targets); device='cuda' if torch.cuda.is_available() else 'cpu'
    torch.set_num_threads(8); torch.backends.cuda.matmul.allow_tf32=False; torch.backends.cudnn.allow_tf32=False
    scores=[]
    for method in NAMES:
        model=Classifier(root,method,device); generator=torch.Generator(device=device).manual_seed(SEED+4)
        errors=np.empty((len(ds),3,len(GRID)),dtype=bool); losses=np.empty(errors.shape,dtype=np.float32)
        with torch.inference_mode():
            for start in range(0,len(ds),64):
                end=min(start+64,len(ds)); x=torch.stack([ds[i][0] for i in range(start,end)]).to(device)
                y=torch.tensor(labels[start:end],device=device).repeat_interleave(3)
                x=x[:,None].expand(-1,3,-1,-1,-1).reshape(-1,3,32,32)
                z=torch.randn(x.shape,generator=generator,device=device)
                for k,sigma in enumerate(GRID):
                    logits=model(x+float(sigma)*z)
                    errors[start:end,:,k]=(logits.argmax(1)!=y).view(end-start,3).cpu().numpy()
                    losses[start:end,:,k]=torch.nn.functional.cross_entropy(logits,y,reduction='none').view(end-start,3).cpu().numpy()
                if start%640==0: print(method,'TEST',start,len(ds),flush=True)
        np.savez_compressed(out/(method+'_test_scores.npz'),errors=errors,losses=losses,labels=labels)
        scores.append(errors.mean(1)); del model
        torch.cuda.empty_cache() if device=='cuda' else None
    delta=scores[1]-scores[0]; curve=delta.mean(0)
    rng=np.random.default_rng(SEED+5); ids=np.stack([np.flatnonzero(labels==c) for c in range(100)])
    draws=[]
    for b in range(2000):
        chosen=ids[np.arange(100)[:,None],rng.integers(0,100,(100,100))].reshape(-1)
        draws.append(delta[chosen].mean(0))
    draws=np.array(draws); bands=np.quantile(draws,[.025/len(GRID),1-.025/len(GRID)],axis=0)
    point,bracket=crossing(curve)
    resolved=bool(bands[0,0]>0 and np.any(bands[1,1:]<0))
    ci=prediction['crossing_ci95']; compatible=False
    if bracket is not None:
        compatible=bool(GRID[bracket-1]<=ci[1] and GRID[bracket]>=ci[0])
    relative_ok=point is not None and 1/1.5<=point/prediction['predicted_crossing']<=1.5
    success=resolved and compatible and relative_ok
    result=dict(sigma_grid=GRID.tolist(),CL_error=scores[0].mean(0).tolist(),NCL_error=scores[1].mean(0).tolist(),
        delta_NCL_minus_CL=curve.tolist(),simultaneous_lower=bands[0].tolist(),simultaneous_upper=bands[1].tolist(),
        observed_crossing=point,observed_crossing_grid_index=bracket,resolved_reversal=resolved,
        crossing_bracket_compatible_with_prediction=compatible,crossing_factor_tolerance_passed=relative_ok,
        predictive_success=bool(success),test_images_evaluated=len(ds),
        limitations='Single checkpoint/probe pair; conditional image bootstrap. Gaussian unclipped input noise only. This does not isolate monosemanticity causally or validate a universal phase diagram.')
    np.savez_compressed(out/'bootstrap_curves.npz',curves=draws); save(out/'results.json',result)
    save(out/'completed.json',dict(end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),success=True))
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__': main()
