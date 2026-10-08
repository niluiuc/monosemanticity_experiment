"""Independent saved-result check; imports no compressor/experiment functions."""
from pathlib import Path
import json, hashlib
import numpy as np
from scipy.special import ndtr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
OUT=HERE/'controlled_image_completion_v1'

def risk(scores,target,w,b,s):
    mu=np.outer(scores@w,w)+b
    sd=np.abs(w)*s
    if s==0:
        return np.sum((np.maximum(mu,0)-target)**2,axis=1)
    m1=np.maximum(mu,0);m2=m1*m1
    active=sd>0
    z=mu[:,active]/sd[active]
    dens=np.exp(-z*z/2)/np.sqrt(2*np.pi)
    m1[:,active]=mu[:,active]*ndtr(z)+sd[active]*dens
    m2[:,active]=(mu[:,active]**2+sd[active]**2)*ndtr(z)+mu[:,active]*sd[active]*dens
    return np.sum(m2-2*target*m1+target*target,axis=1)

def run():
    pred=json.loads((OUT/'prediction.json').read_text());ev=json.loads((OUT/'evaluation.json').read_text())
    test=np.load(OUT/'test_inference/test_scores.npz');r=test['scores'];X=test['labels']
    assert r.shape==X.shape==(1024,2)
    assert np.array_equal(X,np.tile([[0,0],[0,1],[1,0],[1,1]],(256,1)))
    group=test['background_ids'];assert len(np.unique(group))==256
    trained=HERE.parent/'project1_toy/controlled_image_phase_20261007/learning_run_v1'
    ids=np.load(trained/'split_background_ids.npz')
    assert len(set(ids['test'])&set(ids['train']))==0 and len(set(ids['test'])&set(ids['calibration']))==0
    delta=float(np.sqrt(np.mean(np.sum((r-X)**2,axis=1))))
    assert abs(delta-ev['test_recovery_rms'])<1e-14
    values=[];errors=[]
    for p,e in zip(pred['rows'],ev['rows']):
        ls={k:risk(r,X,np.asarray(v['weights']),np.asarray(v['biases']),p['sigma']) for k,v in p['models'].items()}
        diff=float(np.mean(ls['share']-ls['mono'])); errors.append(abs(diff-e['observed_difference']))
        assert errors[-1]<1e-12
        values.append(diff)
    assert not ev['passed'] and not ev['recovery_passes']
    result={'verified':True,'max_risk_difference_error':max(errors),'test_recovery_rms':delta,'protocol_passed':False,'test_backgrounds_disjoint':True,'actual_signs_match_predictions':True,'qualification':'Recovery gate failed. Neither this verification nor actual-error bounds changes that verdict.'}
    (OUT/'independent_verification.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
    fig,ax=plt.subplots(figsize=(7,4))
    x=np.arange(2);limits=np.array([p['predicted_interval'] for p in pred['rows']])
    refs=np.array([p['reference_difference'] for p in pred['rows']])
    ax.errorbar(x,refs,yerr=np.vstack([refs-limits[:,0],limits[:,1]-refs]),fmt='s',capsize=6,label='Pre-recorded prediction + allowed recovery bound')
    ax.scatter(x,values,c='black',zorder=5,label='Held-out observed risk difference')
    ax.axhline(0,color='grey',lw=1)
    ax.set_xticks(x,['Clean: σ = 0','Code noise: σ = 0.30'])
    ax.set_ylabel('Sharing risk − mono risk');ax.set_title('Controlled learned vision: ordering reverses\nRecovery gate FAILED: 0.001204 > 0.0005')
    ax.legend(fontsize=8);fig.tight_layout();fig.savefig(OUT/'ordering_comparison.png',dpi=180)
    # Examples are controlled images, not native CIFAR classifications.
    im=np.load(OUT/'test_inference/test_images.npz')['images'][:4]
    fig,axs=plt.subplots(1,4,figsize=(8,2.5))
    for i,a in enumerate(axs):
        a.imshow(im[i].transpose(1,2,0));a.set_title(f'Factors {X[i].astype(int).tolist()}');a.axis('off')
    fig.suptitle('Same held-out background, four planted factor states')
    fig.tight_layout();fig.savefig(OUT/'heldout_examples.png',dpi=160)

if __name__=='__main__':run()
