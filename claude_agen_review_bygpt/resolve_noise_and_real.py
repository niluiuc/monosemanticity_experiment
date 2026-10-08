"""Focused follow-up for the ONE noise-bracket contradiction and real-loss spotchecks.
Original data/results unchanged. Imports only the independent audit and side-effect-free fra2.
"""
import sys
from pathlib import Path
import json
import numpy as np
import mpmath as mp
from scipy.optimize import brentq,minimize_scalar
from scipy.special import ndtr
import verify as V

sys.path.insert(0,str(V.BASE))
import fra2
OUT={}

def mp_loss(theta,p,b,sigma):
    t=mp.mpf(str(theta)); pp=mp.mpf(str(p)); s=mp.mpf(str(sigma))
    w=[mp.cos(t),mp.sin(t)]; total=mp.mpf(0)
    probs=[(1-pp)**2,pp*(1-pp),pp*(1-pp),pp**2]
    for i,eta in [(0,1),(1,mp.mpf('.5'))]:
        v=0
        for x,prob in zip([(0,0),(1,0),(0,1),(1,1)],probs):
            mu=w[i]*(w[0]*x[0]+w[1]*x[1])+mp.mpf(str(b[i])); sd=abs(w[i])*s
            if sd==0: m1=max(0,mu);m2=m1*m1
            else:
                z=mu/sd;Phi=(1+mp.erf(z/mp.sqrt(2)))/2;phi=mp.exp(-z*z/2)/mp.sqrt(2*mp.pi)
                m1=mu*Phi+sd*phi;m2=(mu*mu+sd*sd)*Phi+mu*sd*phi
            v+=prob*(m2-2*x[i]*m1+x[i]**2)
        total+=eta*v
    return total

pc=(3-np.sqrt(5))/2; rows=[]
for sigma in [.001,.003]:
    def sharing(eps):
        p=pc-eps
        r=minimize_scalar(lambda t:V.profile(t,p,sigma=sigma)[0],bounds=(-2.3*eps,-.7*eps),method='bounded',options={'xatol':1e-12})
        return r.x,V.profile(0,p,sigma=sigma)[0]-r.fun
    root=brentq(lambda eps:sharing(eps)[1],.7*.8315564147061506*sigma**(2/3),1.3*.8315564147061506*sigma**(2/3),xtol=5e-10)
    for eps in [root,root-.0001,root+.0001]:
        p=pc-eps;t,gain=sharing(eps)
        ours,bs=V.profile(t,p,sigma=sigma); mono,bm=V.profile(0,p,sigma=sigma)
        orig,b1,b2=fra2.F(t,p,0,sigma,.5); origm,mb1,mb2=fra2.F(0,p,0,sigma,.5)
        rows.append({'sigma':sigma,'independent_eps_root':root,'eps':eps,'theta':t,'gain_independent':gain,
          'gain_55digit':str(mp_loss(0,p,bm,sigma)-mp_loss(t,p,bs,sigma)),
          'original_loss_minus_independent':orig-ours,'original_mono_minus_independent':origm-mono,
          'original_biases':[b1,b2],'independent_biases':bs,
          'original_gain_at_same_theta':origm-orig})
OUT['noise_resolution']=rows
print('noise roots',[(r['sigma'],r['independent_eps_root']) for r in rows[::3]],flush=True)
(V.HERE/'followup_results.json').write_text(json.dumps(OUT,indent=2),encoding='utf-8')

def empirical_bias(offset,x,s):
    if s<1e-14: return V.clean_bias(offset,x,np.ones(len(x))/len(x))
    def fun(b):
        mu=offset+b;z=mu/s;Phi=ndtr(z);phi=np.exp(-z*z/2)/np.sqrt(2*np.pi)
        return np.mean((mu*mu+s*s)*Phi+mu*s*phi-2*x*(mu*Phi+s*phi)+x*x)
    # Multiple candidate minima on an expanded range; enough to audit the saved answer,
    # not claimed a formal proof of empirical globality.
    grid=np.linspace(-4,4,321);vals=np.array([fun(b) for b in grid]);cands=[(vals.min(),grid[np.argmin(vals)])]
    for j in range(1,len(grid)-1):
        if vals[j]<=vals[j-1] and vals[j]<=vals[j+1]:
            r=minimize_scalar(fun,bounds=(grid[j-1],grid[j+1]),method='bounded',options={'xatol':1e-12})
            cands.append((r.fun,r.x))
    return min(cands)

def empirical_loss(X,w,sigma,etas):
    h=X@w
    return sum(e*empirical_bias(w[i]*h,X[:,i],abs(w[i])*sigma)[0] for i,e in enumerate(etas))

checks=[]
for name in ['real','real_logits']:
    if name=='real':
        z=np.load(V.ROOT/'project1_toy/vision_transfer_20261006/extraction_run_v1/vision_activations.npz')
        X=np.concatenate([z['train'],z['calibration'],z['test']],0).astype(float)
    else:X=np.maximum(np.load(V.ROOT/'project1_toy/head_transfer_20261007/extraction_run_v1/raw_logits.npy',mmap_mode='r')[:1024].astype(float),0)
    X=X/np.sqrt((X*X).mean(0,keepdims=True)+1e-30)
    P={(p['i'],p['j']):p for p in V.load(f'results/{name}/pairs.json')['pairs']}
    L=V.load(f'results/{name}/landscapes.json')
    ordered=sorted(L,key=lambda r:P[(r['i'],r['j'])]['corr'])
    chosen=[ordered[0],min(L,key=lambda r:abs(P[(r['i'],r['j'])]['corr'])),ordered[-1]]
    for r in chosen:
        pair=X[:,[r['i'],r['j']]]
        for sig in [.005,.4]:
            saved=next(s for s in r['rows'] if s['sigma']==sig); t=saved['theta_star'];w=np.array([np.cos(t),np.sin(t)])
            loss=empirical_loss(pair,w,sig,[1,.5])
            nearby=[empirical_loss(pair,np.array([np.cos(t+d),np.sin(t+d)]),sig,[1,.5]) for d in [-.001,.001]]
            checks.append({'dataset':name,'channels':[r['i'],r['j']],'sigma':sig,'theta':t,
              'saved_loss':saved['F_star'],'independent_loss':loss,'difference':loss-saved['F_star'],
              'nearby_min_minus_selected':min(nearby)-loss})
    tripdir='real_triples' if name=='real' else 'real_triples_logits'
    S=V.load(f'results/{tripdir}/solutions.json'); triples=sorted(S,key=lambda r:r['c13'])
    for r in [triples[0],triples[-1]]:
        Xs=X[:,[r['i'],r['j'],r['k']]];loss=empirical_loss(Xs,np.array(r['w']),.005,[1,.5,.45])
        checks.append({'dataset':tripdir,'channels':[r['i'],r['j'],r['k']],'saved_loss':r['F'],'independent_loss':loss,'difference':loss-r['F']})
OUT['real_loss_spotchecks']=checks
OUT['scope']='Refitted biases at saved encoder directions plus two neighboring directions for six pairs. No full encoder retraining or native network intervention.'
(V.HERE/'followup_results.json').write_text(json.dumps(OUT,indent=2),encoding='utf-8')
print('real loss checks',len(checks),'max absolute difference',max(abs(r['difference']) for r in checks),flush=True)
