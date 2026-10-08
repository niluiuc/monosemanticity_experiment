import argparse,datetime,json
from pathlib import Path
import numpy as np
import torch
from run_clean_gate import save,digest

def purity(active,y):
    counts=np.stack([active[y==c].sum(0) for c in range(100)])
    denominator=counts.sum(0); keep=denominator>0
    return float(np.mean(counts[:,keep].max(0)/denominator[keep]))

def main():
    p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,required=True); root=p.parse_args().root
    out=root/'prevalence_check_v1'; out.mkdir(exist_ok=False)
    split=np.load(root/'clean_run_v1/split_indices.npz')['validation']; features={}; originals={}
    save(out/'provenance.json',dict(start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        script_sha256=digest(__file__),protocol_sha256=digest(root/'PREVALENCE_PROTOCOL.md'),test_images_evaluated=0,post_outcome=True))
    for m in ('CL','NCL'):
        a=np.load(root/'clean_run_v1'/m/'clean_train_features.npz'); y=a['labels'][split]
        f=torch.nn.functional.normalize(torch.tensor(a['features'][split]),dim=1).abs().numpy()
        original=f>1e-5; keep=original.any(0); features[m]=f[:,keep]; originals[m]=original[:,keep]
    prevalence=float(originals['NCL'].mean()); k=int(np.clip(round(prevalence*len(y)),1,len(y)))
    order=np.random.default_rng(20261022).permutation(len(y)); selected={}; records={}
    for m,f in features.items():
        ranks=np.argsort(f[order],axis=0,kind='stable')[-k:]
        mask=np.zeros(f.shape,dtype=bool); mask[order[ranks],np.arange(f.shape[1])[None,:]]=True
        cutoff=np.take_along_axis(f[order],ranks[:1],axis=0)[0]
        tied=(f==cutoff[None,:]).sum(0)
        selected[m]=mask
        records[m]=dict(original_purity=purity(originals[m],y),matched_purity=purity(mask,y),
            nondead_dimensions=f.shape[1],cutoff_tied_coordinates=int((tied>1).sum()),
            zero_cutoff_coordinates=int((cutoff==0).sum()))
        np.savez_compressed(out/(m+'_selection.npz'),active=mask,original_active=originals[m],labels=y,image_indices=split)
    delta=records['NCL']['matched_purity']-records['CL']['matched_purity']
    ids=np.stack([np.flatnonzero(y==c) for c in range(100)]); rng=np.random.default_rng(20261023); draws=[]
    for _ in range(200):
        selected_ids=ids[np.arange(100)[:,None],rng.integers(0,50,(100,50))].reshape(-1)
        draws.append(purity(selected['NCL'][selected_ids],y[selected_ids])-purity(selected['CL'][selected_ids],y[selected_ids]))
    interval=np.quantile(draws,[.025,.975]).tolist()
    result=dict(methods=records,NCL_original_prevalence=prevalence,k=k,matched_prevalence=k/len(y),
        matched_difference=delta,conditional_ci95=interval,contrast_survives_control=bool(interval[0]>0),
        limitations='Post-outcome descriptive proxy check. Bootstrap conditions on rank selections and k. This is not ground-truth monosemanticity, causal attribution, or a replacement of registered gates.')
    np.savez(out/'bootstrap.npz',draws=draws); save(out/'results.json',result); print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__': main()
