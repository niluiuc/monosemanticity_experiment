import argparse, datetime, json
from pathlib import Path
import numpy as np
import torch
from torchvision.datasets import CIFAR100
from torchvision.transforms import ToTensor
import run_clean_gate as clean

SEEDS=(20261018,20261019); GRID=(0.,.12); NOISE_SEED=20261020

def main():
    p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,required=True)
    root=p.parse_args().root; out=root/'probe_replication_v1'; out.mkdir(exist_ok=False)
    torch.set_num_threads(8); device='cpu'; split=np.load(root/'clean_run_v1/split_indices.npz')
    clean.save(out/'provenance.json',dict(start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        post_outcome_followup=True,script_sha256=clean.digest(__file__),protocol_sha256=clean.digest(root/'PROBE_REPLICATION_PROTOCOL.md'),
        seeds=SEEDS,noise_seed=NOISE_SEED,sigma_grid=GRID,test_images_previously_seen=True))
    ds=CIFAR100(str(root/'data'),train=False,download=False,transform=ToTensor())
    labels=np.array(ds.targets); method_errors={}; validation={}
    for method,name in clean.NAMES.items():
        cache=np.load(root/'clean_run_v1'/method/'clean_train_features.npz')
        f=torch.tensor(cache['features']); y=torch.tensor(cache['labels']); heads=[]
        for seed in SEEDS:
            sub=out/str(seed)/method; sub.mkdir(parents=True)
            clean.SEED=seed
            head,mean,std=clean.fit_probe(f[split['fit']],y[split['fit']],device,sub)
            with torch.no_grad():
                logits=head((f[split['validation']]-mean)/std)
            err=logits.argmax(1)!=y[split['validation']]
            np.savez(sub/'validation.npz',image_indices=split['validation'],logits=logits.numpy(),errors=err.numpy(),labels=y[split['validation']].numpy())
            validation[f'{seed}_{method}']=float(err.float().mean()); heads.append((head,mean,std))
        del f,cache
        model=clean.make_backbone(root/'checkpoints'/name,device)
        pm=torch.tensor(clean.MEAN).view(1,3,1,1); ps=torch.tensor(clean.STD).view(1,3,1,1)
        gen=torch.Generator().manual_seed(NOISE_SEED)
        errors=np.empty((2,len(ds),3,2),dtype=bool); losses=np.empty(errors.shape,dtype=np.float32)
        with torch.inference_mode():
            for start in range(0,len(ds),64):
                end=min(start+64,len(ds)); x=torch.stack([ds[i][0] for i in range(start,end)])
                x=x[:,None].expand(-1,3,-1,-1,-1).reshape(-1,3,32,32)
                z=torch.randn(x.shape,generator=gen); target=torch.tensor(labels[start:end]).repeat_interleave(3)
                for k,sigma in enumerate(GRID):
                    features=model((x+sigma*z-pm)/ps)
                    for j,(head,mean,std) in enumerate(heads):
                        logits=head((features-mean)/std)
                        errors[j,start:end,:,k]=(logits.argmax(1)!=target).reshape(end-start,3).numpy()
                        losses[j,start:end,:,k]=torch.nn.functional.cross_entropy(logits,target,reduction='none').reshape(end-start,3).numpy()
                if start%640==0: print(method,'replication TEST',start,len(ds),flush=True)
        for j,seed in enumerate(SEEDS):
            np.savez_compressed(out/str(seed)/method/'test_scores.npz',errors=errors[j],losses=losses[j],labels=labels)
        method_errors[method]=errors.mean(2); del model,heads
    delta=method_errors['NCL']-method_errors['CL']; points=delta.mean(1)
    ids=np.stack([np.flatnonzero(labels==c) for c in range(100)])
    rng=np.random.default_rng(20261021); draws=[]
    for _ in range(2000):
        selected=ids[np.arange(100)[:,None],rng.integers(0,100,(100,100))].reshape(-1)
        draws.append(delta[:,selected,:].mean(1))
    draws=np.array(draws); bands=np.quantile(draws,[.025/4,1-.025/4],axis=0)
    passed=bool(np.all(bands[0,:,0]>0) and np.all(bands[1,:,1]<0))
    np.savez_compressed(out/'bootstrap.npz',draws=draws)
    result=dict(seeds=SEEDS,sigma_grid=GRID,validation_errors=validation,
        CL_errors=method_errors['CL'].mean(1).tolist(),NCL_errors=method_errors['NCL'].mean(1).tolist(),
        delta_NCL_minus_CL=points.tolist(),simultaneous_lower=bands[0].tolist(),simultaneous_upper=bands[1].tolist(),
        probe_stability_gate_passed=passed,
        limitations='Post-outcome reliability check on reused TEST images and the same backbone checkpoints. Conditional image uncertainty only. No prospective boundary prediction or causal isolation.')
    clean.save(out/'results.json',result); print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__': main()
