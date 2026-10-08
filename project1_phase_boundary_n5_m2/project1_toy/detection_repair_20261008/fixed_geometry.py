import itertools,json
from pathlib import Path
import numpy as np
from scipy.special import ndtr
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(__file__).parent;O=H/'run_v1'
P=np.arange(1,41)*.02;S=np.arange(1,61)*.025
a=2*np.pi*np.arange(5)/5;V=np.array([np.cos(a),np.sin(a)]);W=V*np.sqrt(2/5); t=np.full(5,np.sqrt(2/5)/2)
B=np.array(list(itertools.product([0.,1.],repeat=5)));k=B.sum(1);means=B@W.T@V
def risk(p,s):
 prob=p**k*(1-p)**(5-k)
 if s==0:err=(means>t)!=B
 else:err=ndtr(-(2*B-1)*(means-t)/s)
 return float(prob@err.sum(1))
def mono(p,s):return 3*p if s==0 else 2*ndtr(-1/(2*s))+3*p
mc=np.zeros((len(S),len(P)));se=mc.copy();theory=mc.copy()
for j,p in enumerate(P):
 d=np.load(O/f'draws_p{p:.2f}.npz');b=d['states'];noise=d['noise'];N=len(b)
 for i,s in enumerate(S):
  pred=(b@W.T+s*noise)@V>t;me=((b[:,:2]+s*noise)>.5)!=b[:,:2]
  dif=(pred!=b).sum(1)-me.sum(1)-b[:,2:].sum(1)
  mc[i,j]=dif.mean();se[i,j]=dif.std(ddof=1)/np.sqrt(N);theory[i,j]=risk(p,s)-mono(p,s)
np.savez_compressed(O/'fixed_pentagon_heatmap.npz',W=W,V=V,thresholds=t,p=P,sigma=S,simulation=mc,theory=theory,standard_error=se)
fig,ax=plt.subplots(figsize=(7,5),constrained_layout=True)
im=ax.pcolormesh(P,S,mc,cmap='RdBu_r',vmin=-1,vmax=1,shading='auto')
if theory.min()<0<theory.max():ax.contour(P,S,theory,levels=[0],colors='black',linewidths=2)
ax.set(xlabel='Activation probability p',ylabel='Code-noise sigma',title='Fixed five-concept pentagon in two dimensions')
fig.colorbar(im,ax=ax,label='Simulated sharing error minus mono error');fig.savefig(O/'fixed_pentagon_heatmap.png',dpi=180)
roots=[]
grid=np.r_[0,S];g=np.array([risk(.2,s)-mono(.2,s) for s in grid])
for l,h,gl,gh in zip(grid[:-1],grid[1:],g[:-1],g[1:]):
 if gl*gh<0:roots.append(float(brentq(lambda s:risk(.2,s)-mono(.2,s),l,h)))
z=abs(mc-theory)/np.maximum(se,1e-12)
result=dict(energy=float((W*W).sum()),clean_shared_risk_p02=risk(.2,0),clean_mono_risk_p02=mono(.2,0),numerical_roots_p02=roots,max_abs_mc_error=float(abs(mc-theory).max()),max_standardized_error=float(z.max()),fraction_within_3se=float((z<=3).mean()),scope='Fixed pentagon and lecture midpoint detectors, not learned optimum or native model.')
(O/'fixed_pentagon_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
