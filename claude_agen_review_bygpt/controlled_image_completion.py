"""Complete the existing predeclared controlled-image fixture; no retraining.

Prediction stage reads train/calibration only. Evaluation stage requires a
frozen prediction tied to checkpoint hash and the archived source.
Uses established finite bias-profile and calibration-gap infrastructure.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util, json, time, hashlib, argparse
import numpy as np
from scipy.optimize import minimize_scalar

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent/'controlled_image_completion_v1'
TRAINED=ROOT/'project1_toy/controlled_image_phase_20261007/learning_run_v1'
STATES=np.array([[0,0],[0,1],[1,0],[1,1]],float)
spec=importlib.util.spec_from_file_location('profile_library',ROOT/'project1_toy/joint_phase_theory_2026-10-06/vision_transfer.py')
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):Path(p).write_text(json.dumps(V.plain(d),indent=2,allow_nan=False))

def profile(scores,labels,w):
    h=scores@w
    ps=[V.clean_profile(w[i]*h,labels[:,i]) for i in range(2)]
    return {'loss':sum(p['loss'] for p in ps),'biases':[p['beta'] for p in ps]}

def risks(scores,labels,w,b,sigma):
    h=scores@w
    return sum(V.moments(w[i]*h+b[i],abs(w[i])*sigma)[1]-2*labels[:,i]*V.moments(w[i]*h+b[i],abs(w[i])*sigma)[0]+labels[:,i]**2 for i in range(2))

def interval(rs,rm,delta):
    return [max(0,np.sqrt(rs)-delta)**2-(np.sqrt(rm)+delta)**2,
            (np.sqrt(rs)+delta)**2-max(0,np.sqrt(rm)-delta)**2]

def predict():
    OUT.mkdir(exist_ok=False)
    gate=json.loads((TRAINED/'recovery_gate.json').read_text());assert gate['passed']
    tr=np.load(TRAINED/'train_scores.npz'); ca=np.load(TRAINED/'calibration_scores.npz')
    scores=tr['scores'][:256];labels=tr['labels'][:256]
    assert np.array_equal(labels,np.tile(STATES,(64,1)))
    fits=[]
    for n in [256,512]:
        angles=np.arange(n)*np.pi/n
        vals=np.array([profile(scores,labels,np.array([np.cos(t),np.sin(t)]))['loss'] for t in angles])
        t0=angles[vals.argmin()]
        rr=minimize_scalar(lambda t:profile(scores,labels,np.array([np.cos(t),np.sin(t)]))['loss'],bounds=(t0-np.pi/(2*n),t0+np.pi/(2*n)),method='bounded',options={'xatol':1e-10,'maxiter':100})
        w=np.array([np.cos(rr.x),np.sin(rr.x)])
        fits.append({'resolution':n,'success':bool(rr.success),'theta':float(rr.x),'weights':w,'profile':profile(scores,labels,w)})
    ws=np.asarray(fits[-1]['weights'])
    monos=[profile(scores,labels,w) for w in np.eye(2)]
    r=int(np.argmin([m['loss'] for m in monos]));wm=np.eye(2)[r]
    delta_tr=float(np.sqrt(np.mean(np.sum((scores-labels)**2,axis=1))))
    ideal_best=.25-(3-2*np.sqrt(2))/48
    excess=float(fits[-1]['profile']['loss']-max(0,np.sqrt(ideal_best)-delta_tr)**2)
    rows=[];deadline=time.monotonic()+200
    for sigma in [0.,.3]:
        fitted={};ref={};ledger={}
        for name,w in [('share',ws),('mono',wm)]:
            h=ca['scores']@w
            ps=[V.calibrate(w[i]*h,ca['labels'][:,i],abs(w[i])*sigma,V.clean_profile(w[i]*h,ca['labels'][:,i])['beta'],1e-7,deadline) for i in range(2)]
            b=np.array([p['beta'] for p in ps]);ledger[name]=ps
            fitted[name]={'weights':w,'biases':b}
            ref[name]=float(risks(STATES,STATES,w,b,sigma).mean())
        bounds=interval(ref['share'],ref['mono'],.0005)
        rows.append({'sigma':sigma,'models':fitted,'reference_risks':ref,'reference_difference':ref['share']-ref['mono'],'predicted_interval':bounds,'calibration_resolved':all(p['resolved'] for ps in ledger.values() for p in ps),'calibration_ledgers':ledger})
    approved=all(f['success'] for f in fits) and abs(fits[0]['profile']['loss']-fits[1]['profile']['loss'])<1e-8 and 0<=excess<=.0015 and all(row['calibration_resolved'] for row in rows) and rows[0]['predicted_interval'][1]<0 and rows[1]['predicted_interval'][0]>0
    result={'approved_for_heldout':bool(approved),'model_sha256':sha(TRAINED/'model.pt'),'script_sha256':sha(__file__),'extractor_sha256':sha(TRAINED/'source_snapshot.py'),'fits':fits,'mono_retained':r,'mono_train_profiles':monos,'train_subset_recovery':delta_tr,'optimization_excess_upper_bound':excess,'prediction_recovery_allowance':.0005,'rows':rows,'scope':'Predetermined controlled visual factors, learned continuous scores, code noise; not native-network transfer.'}
    write(OUT/'prediction.json',result)
    print(json.dumps({k:V.plain(result[k]) for k in ['approved_for_heldout','train_subset_recovery','optimization_excess_upper_bound','mono_retained']}))
    print('predictions',[(row['sigma'],row['reference_difference'],row['predicted_interval'],row['calibration_resolved']) for row in rows])

def evaluate():
    pred=json.loads((OUT/'prediction.json').read_text());assert pred['approved_for_heldout']
    assert pred['model_sha256']==sha(TRAINED/'model.pt') and pred['script_sha256']==sha(__file__)
    test=np.load(OUT/'test_inference/test_scores.npz'); X=test['labels'];scores=test['scores']
    delta=float(np.sqrt(np.mean(np.sum((scores-X)**2,axis=1))))
    rows=[]; saved={}
    for row in pred['rows']:
        losses={name:risks(scores,X,np.array(m['weights']),np.array(m['biases']),row['sigma']) for name,m in row['models'].items()}
        diff=losses['share']-losses['mono'];mean=float(diff.mean())
        bounds=interval(row['reference_risks']['share'],row['reference_risks']['mono'],delta)
        rows.append({'sigma':row['sigma'],'observed_risks':{k:float(v.mean()) for k,v in losses.items()},'observed_difference':mean,'predicted_interval':row['predicted_interval'],'actual_recovery_interval':bounds,'prediction_contains_observation':bool(row['predicted_interval'][0]<=mean<=row['predicted_interval'][1]),'actual_bound_contains_observation':bool(bounds[0]<=mean<=bounds[1])})
        saved[str(row['sigma'])]=diff
    np.savez_compressed(OUT/'per_image_risk_differences.npz',background_ids=test['background_ids'],**saved)
    result={'test_recovery_rms':delta,'recovery_passes':bool(delta<=.0005),'rows':rows,'passed':bool(delta<=.0005 and rows[0]['observed_difference']<0 and rows[1]['observed_difference']>0 and all(r['prediction_contains_observation'] and r['actual_bound_contains_observation'] for r in rows))}
    write(OUT/'evaluation.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['predict','evaluate']);args=parser.parse_args()
    predict() if args.stage=='predict' else evaluate()
