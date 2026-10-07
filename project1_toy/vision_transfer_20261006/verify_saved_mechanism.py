"""Independent arithmetic verification of an existing mechanism partition only."""
from pathlib import Path
import argparse, json, shutil
import numpy as np
from scipy.special import ndtr
from audit_vision_outputs import digest, manifest_check


def output_risk(x,w,b,sigma):
    code=x@w;columns=[]
    for i,importance in enumerate([1.,2./3.]):
        mu=w[i]*code+b[i];sd=sigma*abs(w[i])
        if sd==0:value=(np.maximum(mu,0)-x[:,i])**2
        else:
            z=mu/sd;Phi=ndtr(z);phi=np.exp(-z*z/2)/np.sqrt(2*np.pi)
            first=np.maximum(mu*Phi+sd*phi,0)
            second=np.maximum((mu*mu+sd*sd)*Phi+mu*sd*phi,0)
            value=second-2*x[:,i]*first+x[:,i]**2
        columns.append(importance*value)
    return np.asarray(columns).T


def check_group(values,mask,record):
    assert record['count']==int(mask.sum())
    assert record['fraction']==float(mask.mean())
    assert abs(record['mean']-values[mask].mean())<1e-12
    assert abs(record['weighted_contribution']-values[mask].sum()/len(values))<1e-12


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',type=Path,required=True)
    parser.add_argument('--mechanism',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    shutil.copy2(Path(__file__),args.output/Path(__file__).name)
    count=manifest_check(args.mechanism,'sha256_manifest.json')
    inputs=json.loads((args.mechanism/'input_hashes.json').read_text())
    for name,hashed in inputs.items():assert digest(args.run/name)==hashed
    x=np.load(args.run/'normalized_targets.npz')['test']
    saved=np.load(args.run/'per_image_losses.npz')
    raw=np.load(args.mechanism/'raw_arrays.npz')
    assert np.array_equal(x,raw['targets'])
    records=json.loads((args.mechanism/'results.json').read_text())
    rows=json.loads((args.run/'results.json').read_text())['cases']
    clean=json.loads((args.run/'clean_selection.json').read_text())
    masks={'target0_zero':x[:,0]==0,'target0_positive':x[:,0]>0}
    assert sum(mask.sum() for mask in masks.values())==512
    for name in ['sharing','mono']:
        w=np.asarray(clean[name]['weights']);b=np.asarray(rows[0]['profiles'][name]['frozen_bias'])
        mu=(x@w)[:,None]*w[None,:]+b
        assert np.array_equal(mu,raw[name+'_clean_mu'])
        for group,mask in masks.items():
            for i in range(2):
                for field,values in [('signed_mean',mu[mask,i]),('absolute_gate_distance',abs(mu[mask,i]))]:
                    rec=records['gates'][name][group][f'output_{i}'][field]
                    assert rec['count']==len(values)
                    assert abs(rec['mean']-values.mean())<1e-12
                    assert rec['minimum']==values.min() and rec['maximum']==values.max()
                    assert np.allclose(rec['quantiles'],np.quantile(values,[.25,.5,.75]),atol=1e-14,rtol=0)
                    assert rec['exactly_zero_fraction']==float(np.mean(values==0))
                    assert rec['positive_fraction']==float(np.mean(values>0))
    max_error=0.
    for j,row in enumerate(rows):
        rec=records['cases'][j];improvements={};outputs={}
        assert rec['sigma']==row['sigma'] and rec['multiplier']==row['multiplier']
        for name in ['sharing','mono']:
            w=np.asarray(clean[name]['weights']);p=row['profiles'][name]
            fr=output_risk(x,w,np.asarray(p['frozen_bias']),row['sigma'])
            cal=output_risk(x,w,np.asarray(p['calibrated_bias']),row['sigma'])
            outputs[name]=fr-cal;improvements[name]=(fr-cal).sum(1)
            error=float(np.max(abs(outputs[name]-raw[f'noise_{j}_{name}_output_improvements'])))
            max_error=max(max_error,error);assert error<1e-12
            for policy,per in [('frozen',fr),('calibrated',cal)]:
                assert np.max(abs(per.sum(1)-saved[f'noise_{j}_{name}_{policy}']))<1e-12
            assert abs(improvements[name].mean()-rec['global_improvements'][name])<1e-12
        contrast=improvements['mono']-improvements['sharing']
        assert np.max(abs(contrast-raw[f'noise_{j}_policy_contrast']))<1e-12
        assert abs(contrast.mean()-rec['global_contrast'])<1e-12
        for group,mask in masks.items():
            for name,v in {**improvements,'contrast':contrast}.items():
                check_group(v,mask,rec['primary_groups'][group][name])
        assert abs(sum(rec['primary_groups'][group]['contrast']['weighted_contribution']
                       for group in masks)-contrast.mean())<1e-12
        for i in range(2):
            for group,mask in [('own_target_zero',x[:,i]==0),('own_target_positive',x[:,i]>0)]:
                for name,v in outputs.items():
                    check_group(v[:,i],mask,rec['per_output_own_target_groups'][f'output_{i}'][group][name])
    last=records['cases'][-1]
    result={'passed':True,'scope':'Independent saved-input/formula/count/decomposition audit; no new fit/noise/bootstrap.',
        'manifest_files_checked':count,'cases_checked':len(rows),'max_output_improvement_discrepancy':max_error,
        'zero_target_count':int(masks['target0_zero'].sum()),'positive_target_count':int(masks['target0_positive'].sum()),
        'largest_noise_primary_groups':last['primary_groups'],
        'limit':'Observational partition; no causal intervention or resolved risk-ordering reversal.'}
    (args.output/'results.json').write_text(json.dumps(result,indent=2))
    (args.output/'sha256.json').write_text(json.dumps({p.name:digest(p) for p in args.output.iterdir()
                            if p.is_file() and p.name!='sha256.json'},indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
