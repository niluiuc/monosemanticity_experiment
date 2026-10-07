"""Fixed-ID adapter using the existing reviewed continuous risk routines."""
from pathlib import Path
import importlib.util, json, shutil, time
import numpy as np
from scipy.stats import rankdata

HERE=Path(__file__).resolve().parent
ASSEMBLY=HERE.parent/'paper_assembly_20261006'
SOURCE=HERE.parent/'joint_phase_theory_2026-10-06/vision_transfer.py'
spec=importlib.util.spec_from_file_location('existing_vision_math',SOURCE)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def auc(y,s):
    y=np.asarray(y,bool);n=int(y.sum());m=len(y)-n
    if n==0 or m==0:return None
    return float((rankdata(s,method='average')[y].sum()-n*(n+1)/2)/(n*m))

def main():
    extraction=HERE/'extraction_run_v1';features=extraction/'targets.npz'
    review=ASSEMBLY/'head_adapter_review.md'
    assert review.is_file() and features.is_file()
    provenance=json.loads((extraction/'provenance.json').read_text())
    assert provenance['status']=='complete' and provenance['ids']==[281,207]
    out=HERE/'evaluation_run_v1';out.mkdir(exist_ok=False)
    snap=out/'source_snapshot';snap.mkdir()
    for source in [Path(__file__),SOURCE,review,ASSEMBLY/'head_transfer_protocol.md',ASSEMBLY/'head_transfer_design_review.md']:
        shutil.copy2(source,snap/source.name)
    v.write(out/'input_hashes.json',{str(p):v.hashlib.sha256(p.read_bytes()).hexdigest() for p in [features,extraction/'provenance.json']})
    raw=np.load(features,allow_pickle=False)
    arrays={k:np.asarray(raw[k],float) for k in ['train','calibration','test']}
    for k,n in [('train',256),('calibration',256),('test',4096)]:
        assert arrays[k].shape==(n,2) and np.isfinite(arrays[k]).all() and (arrays[k]>=0).all()
    associations=[auc(raw['train_labels']==c,arrays['train'][:,i]) for i,c in enumerate([3,5])]
    v.write(out/'association_gate.json',dict(train_auc=associations,threshold=.65,
        target_names=provenance['names'],cifar_associations=['cat','dog'],
        passed=all(a is not None and a>.65 for a in associations)))
    if not all(a is not None and a>.65 for a in associations):
        v.write(out/'stopping_decision.json',dict(stop='class_association_gate_failed'));v.manifest(out);return
    train=arrays['train'];rms=np.sqrt(np.mean(train*train,axis=0))
    if not np.all((rms>0)&(np.var(train,axis=0)>0)):
        v.write(out/'stopping_decision.json',dict(stop='nonconstant_target_gate_failed'));v.manifest(out);return
    x={k:a/rms for k,a in arrays.items()};zero=np.mean(x['train']==0,axis=0)
    ref=float(np.sqrt(np.var(x['train'],axis=0).mean()))
    settings=dict(ids=[281,207],names=provenance['names'],rms=rms,zero_fractions=zero,
        coactivation=float(np.mean(np.all(x['train']>0,axis=1))),sigma_reference=ref,
        importance=v.IMPORTANCE,multipliers=[0,.05,.1,.2,.4],seed=20261007,test_images=4096,
        primary='delta_calibrated_at_multiplier_.4',bootstrap_replicates=2000,
        calibration_gap=v.GAP,slack=v.SLACK,expansions=v.EXPANSIONS,seconds=v.TOTAL_SECONDS)
    v.write(out/'settings.json',settings);np.savez_compressed(out/'normalized_targets.npz',**x)
    clean=v.clean_selection(x['train']);v.write(out/'clean_selection.json',clean)
    if not np.any(zero>0) or not clean['eligible']:
        v.write(out/'stopping_decision.json',dict(stop='clean_mechanism_gate_failed',zero_support=bool(np.any(zero>0)),clean_gates=clean['gates']));v.manifest(out);return
    v.write(out/'association_test_descriptive.json',dict(auc=[auc(raw['test_labels']==c,arrays['test'][:,i]) for i,c in enumerate([3,5])],used_to_fit_or_select=False))
    models={name:clean[name] for name in ['sharing','mono']}
    for name,item in models.items():
        h=x['calibration']@item['weights']
        base=[v.clean_profile(item['weights'][i]*h,x['calibration'][:,i],True) for i in range(2)]
        item['zero_calibration_biases']=np.array([z['beta'] for z in base]);v.write(out/f'{name}_zero_calibration.json',base)
    indices=np.random.default_rng(20261007).integers(0,4096,size=(2000,4096)).astype(np.uint16)
    np.save(out/'bootstrap_indices.npy',indices)
    deadline=time.monotonic()+v.TOTAL_SECONDS;rows=[];all_losses={};all_boots={}
    for j,mult in enumerate(settings['multipliers']):
        sigma=mult*ref;losses={};profiles={};folder=out/f'noise_{j}';folder.mkdir()
        for name,item in models.items():
            w=item['weights'];b0=item['zero_calibration_biases'];h=x['calibration']@w
            ledgers=[v.calibrate(w[i]*h,x['calibration'][:,i],sigma*abs(w[i]),b0[i],v.GAP/float(v.IMPORTANCE.sum()),deadline) for i in range(2)]
            for i,ledger in enumerate(ledgers):v.write(folder/f'{name}_feature_{i}.json',ledger)
            b=np.array([z['beta'] for z in ledgers]);profiles[name]=dict(calibrated_bias=b,frozen_bias=b0,
                resolved=all(z['resolved'] for z in ledgers),total_gap=float(sum(v.IMPORTANCE[i]*ledgers[i]['gap'] for i in range(2))))
            losses[name+'_frozen']=v.per_image_loss(x['test'],w,b0,sigma)
            losses[name+'_calibrated']=v.per_image_loss(x['test'],w,b,sigma)
        comparisons=dict(delta_frozen=losses['sharing_frozen']-losses['mono_frozen'],delta_calibrated=losses['sharing_calibrated']-losses['mono_calibrated'])
        comparisons['policy_contrast']=comparisons['delta_calibrated']-comparisons['delta_frozen']
        for name in models:comparisons[name+'_calibration_improvement']=losses[name+'_frozen']-losses[name+'_calibrated']
        summary={}
        for name,values in comparisons.items():
            boots=values[indices].mean(axis=1);all_boots[f'noise_{j}_{name}']=boots
            summary[name]=dict(mean=float(values.mean()),interval95=np.quantile(boots,[.025,.975]))
        all_losses.update({f'noise_{j}_{name}':a for name,a in {**losses,**comparisons}.items()})
        rows.append(dict(multiplier=mult,sigma=sigma,profiles=profiles,risks={name:float(a.mean()) for name,a in losses.items()},comparisons=summary))
        v.write(out/'results.json',dict(cases=rows))
        print('Noise',mult,'frozen',summary['delta_frozen'],'calibrated',summary['delta_calibrated'],flush=True)
    np.savez_compressed(out/'per_image_losses.npz',**all_losses);np.savez_compressed(out/'bootstrap_statistics.npz',**all_boots)
    v.write(out/'stopping_decision.json',dict(stop='five_fixed_levels_completed',all_calibration_resolved=all(p['resolved'] for row in rows for p in row['profiles'].values())))
    v.manifest(out)

if __name__=='__main__':main()
