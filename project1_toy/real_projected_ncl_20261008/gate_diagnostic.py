"""Post-outcome VALIDATION diagnostic, not a revised prospective prediction."""
import argparse, datetime, json
from pathlib import Path
import numpy as np
import torch
from torchvision.datasets import CIFAR100
from torchvision.transforms import ToTensor
from run_prediction import Classifier
from run_clean_gate import SEED, NAMES, digest, save

def main():
    p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,required=True)
    root=p.parse_args().root; out=root/'gate_diagnostic_v1'; out.mkdir(exist_ok=False)
    torch.set_num_threads(8); device='cpu'; sigma=.04
    split=np.load(root/'clean_run_v1/split_indices.npz')
    ids=split['validation'].reshape(100,50)[:,:5].reshape(-1)
    ds=CIFAR100(str(root/'data'),train=True,download=False,transform=ToTensor())
    labels=np.asarray(ds.targets)[ids]
    save(out/'provenance.json',dict(start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        script_sha256=digest(__file__),protocol_sha256=digest(root/'GATE_DIAGNOSTIC_PROTOCOL.md'),
        test_images_evaluated=0,post_outcome_diagnostic=True,sigma=sigma,directions=32,seed=SEED+2))
    results={}
    for method in NAMES:
        model=Classifier(root,method,device)
        def backbone(x): return model.backbone[0]((x-model.pixel_mean)/model.pixel_std)
        def readout(f): return model.head((model.backbone[1](f)-model.feature_mean)/model.feature_std)
        arrays={k:[] for k in ('clean_logits','actual_logits','full_affine_logits','backbone_affine_logits')}
        gen=torch.Generator().manual_seed(SEED+2)
        for start in range(0,len(ids),8):
            batch=ids[start:start+8]; x=torch.stack([ds[int(i)][0] for i in batch])
            expanded=x[:,None].expand(-1,32,-1,-1,-1).reshape(-1,3,32,32)
            z=torch.randn(expanded.shape,generator=gen)
            with torch.no_grad():
                f,df=torch.func.jvp(backbone,(expanded,),(z,))
                logits,dl=torch.func.jvp(readout,(f,),(df,))
                values=dict(clean_logits=logits,actual_logits=model(expanded+sigma*z),
                    full_affine_logits=logits+sigma*dl,backbone_affine_logits=readout(f+sigma*df))
                for key,value in values.items(): arrays[key].append(value.reshape(len(batch),32,100).numpy())
            if start%80==0: print(method,start,len(ids),flush=True)
        arrays={k:np.concatenate(v) for k,v in arrays.items()}
        np.savez_compressed(out/(method+'_logits.npz'),image_indices=ids,labels=labels,**arrays)
        actual=arrays['actual_logits']; clean=arrays['clean_logits']
        inc=actual-clean; inc-=inc.mean(-1,keepdims=True)
        actual_error=float((actual.argmax(-1)!=labels[:,None]).mean()); comparisons={}
        for key in ('full_affine_logits','backbone_affine_logits'):
            v=arrays[key]; residual=actual-v; residual-=residual.mean(-1,keepdims=True)
            error=float((v.argmax(-1)!=labels[:,None]).mean())
            relative=float(np.sqrt(np.mean(residual.astype(float)**2)/np.mean(inc.astype(float)**2)))
            discrepancy=abs(error-actual_error)
            comparisons[key]=dict(error=error,error_discrepancy=discrepancy,relative_rms=relative,
                gate_passed=discrepancy<=.02 and relative<=.25)
        results[method]=dict(actual_error=actual_error,comparisons=comparisons)
    passed=all(v['comparisons']['backbone_affine_logits']['gate_passed'] for v in results.values())
    save(out/'results.json',dict(methods=results,projection_gate_correction_sufficient=passed,
        decision='Projection-gate correction warrants further prospective testing' if passed else
        'Stop projection-only repair: upstream CNN nonlinearity remains necessary',
        limitations='Post-outcome validation diagnostic. No new crossing prediction, causal conclusion, or TEST evidence.'))
    print(json.dumps(results,indent=2),flush=True)
if __name__=='__main__': main()
