"""Descriptive decomposition of exactly the saved pilot, no new evaluation settings."""
from pathlib import Path
import argparse,hashlib,json,shutil,sys
import numpy as np
HOME=Path(__file__).resolve().parent
sys.path.insert(0,str(HOME.parent/'joint_phase_theory_2026-10-06'))
import vision_transfer as implementation

def summary(v):
    v=np.asarray(v,float)
    if len(v)==0:return dict(count=0)
    return dict(count=len(v),mean=float(np.mean(v)),minimum=float(np.min(v)),
                quantiles=np.quantile(v,[.25,.5,.75]),maximum=float(np.max(v)),
                exactly_zero_fraction=float(np.mean(v==0)),positive_fraction=float(np.mean(v>0)))

def contributions(v,mask):
    selected=np.asarray(v)[mask]
    return dict(count=int(np.sum(mask)),fraction=float(np.mean(mask)),
                mean=float(np.mean(selected)) if len(selected) else None,
                weighted_contribution=float(np.sum(selected)/len(v)))

def output_losses(x,w,b,sigma):
    h=x@w;loss=[]
    for i in range(2):
        m1,m2=implementation.moments(w[i]*h+b[i],sigma*abs(w[i]))
        loss.append(implementation.IMPORTANCE[i]*(m2-2*x[:,i]*m1+x[:,i]*x[:,i]))
    return np.asarray(loss).T

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=False);snap=out/'source_snapshot';snap.mkdir()
    for p in [Path(__file__),HOME/'mechanism_audit_protocol.md',Path(implementation.__file__)]:shutil.copy2(p,snap/p.name)
    input_paths=[args.run/name for name in ['normalized_targets.npz','per_image_losses.npz','clean_selection.json','results.json']]
    implementation.write(out/'input_hashes.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths})
    x=np.load(input_paths[0],allow_pickle=False)['test'];saved=np.load(input_paths[1],allow_pickle=False)
    clean=json.loads(input_paths[2].read_text());results=json.loads(input_paths[3].read_text())['cases']
    assert x.shape==(512,2) and len(results)==5
    masks=dict(target0_zero=x[:,0]==0,target0_positive=x[:,0]>0)
    arrays={};gates={}
    for name in ['sharing','mono']:
        w=np.asarray(clean[name]['weights']);b=np.asarray(results[0]['profiles'][name]['frozen_bias'])
        mu=(x@w)[:,None]*w[None,:]+b[None,:];arrays[name+'_clean_mu']=mu
        gates[name]={group:{f'output_{i}':dict(signed_mean=summary(mu[mask,i]),
                         absolute_gate_distance=summary(abs(mu[mask,i]))) for i in range(2)}
                     for group,mask in masks.items()}
    rows=[];max_error=0.
    for j,row in enumerate(results):
        improvements={};output_improvements={}
        for name in ['sharing','mono']:
            w=np.asarray(clean[name]['weights']);profile=row['profiles'][name]
            fr=output_losses(x,w,np.asarray(profile['frozen_bias']),row['sigma'])
            cal=output_losses(x,w,np.asarray(profile['calibrated_bias']),row['sigma'])
            for policy,computed in [('frozen',fr),('calibrated',cal)]:
                error=float(np.max(abs(np.sum(computed,axis=1)-saved[f'noise_{j}_{name}_{policy}'])))
                max_error=max(max_error,error);assert error<1e-12
            output_improvements[name]=fr-cal;improvements[name]=np.sum(fr-cal,axis=1)
            arrays[f'noise_{j}_{name}_output_improvements']=fr-cal
        contrast=improvements['mono']-improvements['sharing']
        assert np.max(abs(contrast-saved[f'noise_{j}_policy_contrast']))<1e-12
        arrays[f'noise_{j}_policy_contrast']=contrast
        primary={group:{name:contributions(v,mask) for name,v in {**improvements,'contrast':contrast}.items()}
                 for group,mask in masks.items()}
        diagnostics={}
        for i in range(2):
            diagnostics[f'output_{i}']={group:{name:contributions(v[:,i],mask) for name,v in output_improvements.items()}
                   for group,mask in [('own_target_zero',x[:,i]==0),('own_target_positive',x[:,i]>0)]}
        rows.append(dict(sigma=row['sigma'],multiplier=row['multiplier'],primary_groups=primary,
                         per_output_own_target_groups=diagnostics,
                         global_contrast=float(np.mean(contrast)),
                         global_improvements={name:float(np.mean(v)) for name,v in improvements.items()}))
    np.savez_compressed(out/'raw_arrays.npz',targets=x,**arrays)
    implementation.write(out/'results.json',dict(scope='Descriptive saved-record decomposition, no new training/noise/bootstrap',
        gates=gates,cases=rows,max_saved_loss_discrepancy=max_error,
        limit='Zero/positive groups are observational; this does not isolate causal gate effects or establish a heldout reversal.'))
    implementation.manifest(out)
    print(json.dumps(implementation.plain(dict(max_saved_loss_discrepancy=max_error,
             largest_noise_primary_groups=rows[-1]['primary_groups'],gates=gates)),indent=2))

if __name__=='__main__':main()
