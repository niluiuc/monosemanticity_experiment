"""Bounded Project 1 coefficient check. No final-evaluation rows or new pairs.

Independent implementation; reads Claude records, never imports/writes Claude code.
Run from repository root using NumPy, SciPy, Matplotlib. Results are descriptive
development-data calculations, not new independent confirmation or novelty evidence.
"""
import json
from pathlib import Path
import numpy as np
from scipy.special import ndtr
from scipy.optimize import minimize_scalar, brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
SRC = ROOT / 'claude_agent/repair_v3/results'
RAW = ROOT / 'project1_toy/head_transfer_20261007/extraction_run_v1/raw_logits.npy'

def phi(z):
    return np.exp(-np.asarray(z)**2 / 2) / np.sqrt(2*np.pi)

def H(z):
    return (1+z*z)*ndtr(z)+z*phi(z)

def moment_loss(mu, s, t):
    if s == 0:
        return (np.maximum(mu,0)-t)**2
    z=mu/s
    return (mu*mu+s*s)*ndtr(z)+mu*s*phi(z)-2*t*(mu*ndtr(z)+s*phi(z))+t*t

def fit(o, t, s, b0):
    # Independent fine search around the archived clean optimum and all noisy
    # local minima on a fixed global grid. Report numerical, not certified.
    grid=np.unique(np.r_[np.linspace(-3,3,601), b0+s*np.linspace(-8,8,161), b0])
    vals=np.array([moment_loss(o+b,s,t).mean() for b in grid])
    ids=[j for j in range(len(grid)) if (j==0 or vals[j]<=vals[j-1]) and (j==len(grid)-1 or vals[j]<=vals[j+1])]
    best=(vals.min(),float(grid[vals.argmin()]))
    for j in ids:
        if 0<j<len(grid)-1:
            rr=minimize_scalar(lambda b:moment_loss(o+b,s,t).mean(),bounds=(grid[j-1],grid[j+1]),method='bounded',options={'xatol':1e-13})
            if rr.fun<best[0]: best=(float(rr.fun),float(rr.x))
    # Risk values can be flat to floating-point precision while held-out bias
    # sensitivity is nonzero. Refine stationarity, not just risk minimisation.
    def grad(b):
        mu=o+b; z=mu/s
        return 2*np.mean(mu*ndtr(z)+s*phi(z)-t*ndtr(z))
    rad=max(8*s,.01)
    if grad(b0-rad)<0 and grad(b0+rad)>0:
        root=brentq(grad,b0-rad,b0+rad,xtol=1e-15)
        mu=o+root; z=mu/s
        curvature=2*np.mean(ndtr(z)-t*phi(z)/s)
        if curvature>0 and moment_loss(mu,s,t).mean()<=best[0]+1e-13:
            return float(root)
    return best[1]

def run():
    data=np.load(RAW,mmap_mode='r')
    perm=np.random.default_rng(20261008).permutation(np.arange(1024,4608))
    pred=perm[896:1792]
    # Explicit access whitelist: only calibration and prediction, never E.
    allowed=np.r_[np.arange(256,512),pred]
    assert len(np.unique(allowed))==1152
    selection=json.loads((SRC/'selection.json').read_text())
    eta=np.asarray(selection['eta'])
    sigmas=np.array([.00001,.00003,.0001,.0003,.001,.003,.01,.03,.1])
    pairs=selection['selected_crossing']+selection['selected_control']
    records=[]
    fig,axs=plt.subplots(1,len(pairs),figsize=(13,4),sharex=True)
    for pair,ax in zip(pairs,np.atleast_1d(axs)):
        info=next(c for c in selection['candidates'] if c['pair']==pair)
        rms=np.asarray(info['train_rms'])
        C=np.maximum(np.asarray(data[np.arange(256,512)][:,pair]),0)/rms
        P=np.maximum(np.asarray(data[pred][:,pair]),0)/rms
        models=json.loads((SRC/f'calib_{pair[0]}_{pair[1]}.json').read_text())['models']
        ws=np.asarray(models['share']['w']); bs=np.asarray(models['share']['biases'][0])
        wm=np.asarray(models['mono']['w']); bm=np.asarray(models['mono']['biases'][0])
        r=int(np.argmax(wm))
        oc=np.outer(C@ws,ws); op=np.outer(P@ws,ws)
        pc=float(np.mean(C[:,r]>0)); pp=float(np.mean(P[:,r]>0))
        zc=minimize_scalar(lambda z:pc*(1+z*z)+(1-pc)*H(z),bounds=(-8,0),method='bounded',options={'xatol':1e-13}).x
        zp=minimize_scalar(lambda z:pp*(1+z*z)+(1-pp)*H(z),bounds=(-8,0),method='bounded',options={'xatol':1e-13}).x
        openp=(op+bs>0).mean(axis=0)
        sharingB=float(np.sum(eta*ws**2*openp))
        mono_cal=pp*(1+zc*zc)+(1-pp)*H(zc)
        mono_self=pp*(1+zp*zp)+(1-pp)*H(zp)
        B_correct=sharingB-eta[r]*mono_cal
        B_old=sharingB-eta[r]*mono_self
        clean_s=sum(eta[i]*moment_loss(op[:,i]+bs[i],0,P[:,i]).mean() for i in range(2))
        clean_m=sum(eta[i]*moment_loss(np.outer(P@wm,wm)[:,i]+bm[i],0,P[:,i]).mean() for i in range(2))
        delta0=float(clean_s-clean_m)
        exact_kinks_C=np.sum(np.abs(oc+bs)<1e-12,axis=0).tolist()
        exact_kinks_P=np.sum(np.abs(op+bs)<1e-12,axis=0).tolist()
        rows=[]
        for sigma in sigmas:
            sb=np.array([fit(oc[:,i],C[:,i],abs(ws[i])*sigma,bs[i]) for i in range(2)])
            mb=np.array([fit(np.outer(C@wm,wm)[:,i],C[:,i],abs(wm[i])*sigma,bm[i]) if wm[i]!=0 else bm[i] for i in range(2)])
            rs=sum(eta[i]*moment_loss(op[:,i]+sb[i],abs(ws[i])*sigma,P[:,i]).mean() for i in range(2))
            rm=sum(eta[i]*moment_loss(np.outer(P@wm,wm)[:,i]+mb[i],abs(wm[i])*sigma,P[:,i]).mean() for i in range(2))
            d=float(rs-rm)
            rows.append({'sigma':float(sigma),'delta':d,'observed_coefficient':float((d-delta0)/sigma**2),'bias_share':sb.tolist(),'bias_mono':mb.tolist()})
        rec={'pair':pair,'delta0':delta0,'p_cal':pc,'p_pred':pp,'z_cal':float(zc),'B_original':float(B_old),'B_calibration_corrected':float(B_correct),'exact_sharing_kinks_cal':exact_kinks_C,'exact_sharing_kinks_pred':exact_kinks_P,'min_sharing_gate_distance_cal':np.min(np.abs(oc+bs),axis=0).tolist(),'min_sharing_gate_distance_pred':np.min(np.abs(op+bs),axis=0).tolist(),'checks':rows}
        records.append(rec)
        ax.semilogx(sigmas,[v['observed_coefficient'] for v in rows],'o-',label='Exact-risk increment / noise²')
        ax.axhline(B_correct,color='black',ls='--',label='Calibration-aware coefficient')
        ax.axhline(B_old,color='tab:orange',ls=':',label='Original coefficient')
        ax.set_title(str(tuple(pair))); ax.set_xlabel('Code-noise standard deviation σ'); ax.grid(alpha=.2)
        print(json.dumps({k:rec[k] for k in ['pair','B_original','B_calibration_corrected','exact_sharing_kinks_cal','exact_sharing_kinks_pred']}))
        print('observed coefficients:',[(v['sigma'],round(v['observed_coefficient'],8)) for v in rows])
    axs[0].set_ylabel('[Δ(σ) − Δ(0)] / σ²'); axs[0].legend(fontsize=7)
    fig.suptitle('Existing real-feature pairs: calibration-aware small-noise prediction (development only)')
    fig.tight_layout();fig.savefig(OUT/'calibration_boundary_check.png',dpi=180)
    result={'question':'Does the small-noise coefficient apply to CAL-fitted/P-evaluated compressors?','scope':'Three existing pairs; no E rows, no new selection, no significance or novelty claim.','sigma_grid':sigmas.tolist(),'pairs':records}
    (OUT/'calibration_boundary_results.json').write_text(json.dumps(result,indent=2))

if __name__=='__main__':run()
