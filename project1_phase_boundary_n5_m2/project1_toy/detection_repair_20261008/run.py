import json,shutil,itertools
from pathlib import Path
import numpy as np
from scipy.special import ndtr,softmax
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(__file__).parent; O=H/'run_v1';O.mkdir(exist_ok=False)
shutil.copyfile(__file__,O/'run_snapshot.py');shutil.copyfile(H/'PROTOCOL.md',O/'PROTOCOL.md')
P=np.arange(1,41)*.02; S=np.arange(1,61)*.025; N=20000
B=np.array(list(itertools.product([0.,1.],repeat=5))); bits=B.sum(1)
def decode(x):
 a=x[:5];r=np.sqrt(2*softmax(x[5:10]));V=np.array([np.cos(a),np.sin(a)]);return V*r,V,x[10:]
def perrisk(W,V,t,p,s):
 prob=p**bits*(1-p)**(5-bits);means=B@W.T@V
 if s==0:err=(means>t)!=B
 else:err=ndtr(-(2*B-1)*(means-t)/s)
 return prob@err
def exact(W,V,t,modes,p,s):
 rr=perrisk(W,V,t,p,s);return float(np.where(modes==0,p,np.where(modes==1,1-p,rr)).sum())
def choose(W,V,t):
 rr=perrisk(W,V,t,.2,.02);return np.where(rr<=.2,2,0) # presence has risk .8, so never wins here
mono=np.zeros((2,5));mono[0,0]=mono[1,1]=1
mv=np.zeros((2,5));mv[0,0]=mv[1,1]=1; mt=np.array([.5,.5,0,0,0]);mm=np.array([2,2,0,0,0])
records=[];models=[]
for seed in [0,1,2]:
 old=np.load(H.parent/f'learned_five_concepts_20261008/run_v1/p0.20_seed{seed}/training.npz');W0=old['W'];r=np.linalg.norm(W0,axis=0)
 x=np.r_[np.arctan2(W0[1],W0[0]),np.log(r*r+1e-30)-np.log(r*r+1e-30).mean(),r/2]
 x[5:10]=np.clip(x[5:10],-12,12)
 bounds=[(None,None)]*5+[(-12,12)]*5+[(-4,4)]*5;trace=[]
 fun=lambda x:float(perrisk(*decode(x),.2,.02).sum())
 def callback(x):trace.append(np.r_[fun(x),x].copy())
 result=minimize(fun,x,method='L-BFGS-B',bounds=bounds,callback=callback,options=dict(maxiter=2000,maxls=50,ftol=1e-12,gtol=1e-7))
 W,V,t=decode(result.x);modes=choose(W,V,t);g=result.jac.copy()
 for i,(lo,hi) in enumerate(bounds):
  if lo is not None and result.x[i]<=lo+1e-8 and g[i]>0:g[i]=0
  if hi is not None and result.x[i]>=hi-1e-8 and g[i]<0:g[i]=0
 rec=dict(seed=seed,success=bool(result.success),message=str(result.message),iterations=int(result.nit),training_risk=float(result.fun),projected_gradient_max=float(abs(g).max()),settled=bool(result.success and abs(g).max()<=1e-5),modes=modes.tolist(),column_norms=np.linalg.norm(W,axis=0).tolist(),clean_risk=exact(W,V,t,modes,.2,0),mono_clean_risk=.6)
 np.savez_compressed(O/f'model_seed{seed}.npz',W=W,V=V,thresholds=t,modes=modes,parameters=result.x,gradient=result.jac,trace=np.array(trace))
 models.append((W,V,t,modes));records.append(rec);print(rec,flush=True)

# Fixed mathematical grids and genuinely simulated colour grids.
rng=np.random.default_rng(20261028)
theory=np.zeros((5,len(S),len(P)));mc=theory.copy();se=theory.copy()
for j,p in enumerate(P):
 b=(rng.random((N,5))<p).astype(float);noise=rng.normal(size=(N,2))
 np.savez_compressed(O/f'draws_p{p:.2f}.npz',states=b,noise=noise)
 for k,s in enumerate(S):
  # Original two-concept figure: shared 1d code vs mono storing the first concept.
  monoerr=(((b[:,0]+s*noise[:,0])>.5)!=b[:,0]).astype(int)+b[:,1]
  for z,a in enumerate([1.,1/np.sqrt(2)]):
   code=a*(b[:,0]-b[:,1])+s*noise[:,0]
   err=((code>a/2)!=b[:,0]).astype(int)+((code<-a/2)!=b[:,1])
   diff=err-monoerr;mc[z,k,j]=diff.mean();se[z,k,j]=diff.std(ddof=1)/np.sqrt(N)
   q=ndtr(-a/(2*s));q3=ndtr(-3*a/(2*s));qm=ndtr(-1/(2*s))
   theory[z,k,j]=2*(1-p)**2*q+2*p*(1-p)*(q+q3)+2*p*p*(1-q)-qm-p
  hmono=b@mono.T+s*noise;pred=hmono@mv>mt;pred[:,2:]=False
  me=(pred!=b).sum(1)
  for seed,(W,V,t,modes) in enumerate(models):
   pred=(b@W.T+s*noise)@V>t
   pred[:,modes==0]=False;pred[:,modes==1]=True
   diff=(pred!=b).sum(1)-me
   z=seed+2;mc[z,k,j]=diff.mean();se[z,k,j]=diff.std(ddof=1)/np.sqrt(N)
   theory[z,k,j]=exact(W,V,t,modes,p,s)-exact(mono,mv,mt,mm,p,s)
 print('simulated p',p,flush=True)
np.savez_compressed(O/'heatmap_values.npz',p=P,sigma=S,theory=theory,simulation=mc,standard_error=se)
fig,axes=plt.subplots(1,2,figsize=(11,4.5),constrained_layout=True)
for z,ax in enumerate(axes):
 im=ax.pcolormesh(P,S,mc[z],cmap='RdBu_r',vmin=-.3,vmax=.3,shading='auto');ax.contour(P,S,theory[z],levels=[0],colors='black');ax.set(xlabel='Activation probability p',ylabel='Code-noise sigma',title=['Equal stored amplitude','Equal total energy'][z])
fig.colorbar(im,ax=axes,label='Simulated sharing error minus mono error');fig.savefig(O/'original_simulation_heatmap.png',dpi=180)
fig,axes=plt.subplots(1,3,figsize=(15,4.5),constrained_layout=True)
for seed,ax in enumerate(axes):
 z=seed+2;im=ax.pcolormesh(P,S,mc[z],cmap='RdBu_r',vmin=-1,vmax=1,shading='auto')
 if theory[z].min()<0<theory[z].max():ax.contour(P,S,theory[z],levels=[0],colors='black')
 ax.set(xlabel='Evaluation frequency p',ylabel='Code-noise sigma',title=f"Seed {seed}, settled={records[seed]['settled']}")
fig.colorbar(im,ax=axes,label='Simulated learned error minus mono error');fig.suptitle('Five concepts; trained only at p=.2, noise=.02; frozen detectors');fig.savefig(O/'repaired_learning_heatmap.png',dpi=180)
zscore=abs(mc-theory)/np.maximum(se,1e-12)
summary=dict(records=records,max_abs_simulation_error=float(abs(mc-theory).max()),max_standardized_error=float(zscore.max()),fraction_within_3se=float((zscore<=3).mean()),cell_count=int(mc.size),notes='Correlated cells share draws; no simultaneous inference/global optimality/novelty claim.')
(O/'results.json').write_text(json.dumps(summary,indent=2));print(summary,flush=True)
