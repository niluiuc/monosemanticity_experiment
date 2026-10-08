"""Independent conditional-state formula; simulation replay at fixed checkpoints."""
import itertools,json
from pathlib import Path
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
O=Path(__file__).parent/'run_v1';a=np.load(O/'heatmap_values.npz');P=a['p'];S=a['sigma']
B=np.array(list(itertools.product([0.,1.],repeat=5)));count=B.sum(1)
def risk(W,V,t,m,p,s):
 value=0.
 for b in B:
  prob=p**b.sum()*(1-p)**(5-b.sum());u=V.T@(W@b)
  for i in range(5):
   if m[i]==0:e=b[i]
   elif m[i]==1:e=1-b[i]
   elif s==0:e=float((u[i]>t[i])!=b[i])
   elif b[i]:e=norm.cdf((t[i]-u[i])/s)
   else:e=norm.sf((t[i]-u[i])/s)
   value+=prob*e
 return float(value)
mono=np.zeros((2,5));mono[0,0]=mono[1,1]=1;mt=np.array([.5,.5,0,0,0]);mm=np.array([2,2,0,0,0])
models=[];roots=[];maxerr=0.
for seed in range(3):
 z=np.load(O/f'model_seed{seed}.npz');W=z['W'];V=z['V'];t=z['thresholds'];m=z['modes'];models.append((W,V,t,m))
 assert abs((W*W).sum()-2)<1e-12;np.testing.assert_allclose((V*V).sum(0),1,atol=1e-12)
 # Independent matrix-free conditional means, all p/noise points at once.
 rr=np.zeros((len(S),len(P)))
 for b in B:
  prob=P**b.sum()*(1-P)**(5-b.sum());u=V.T@(W@b);e=np.zeros(len(S))
  for i in range(5):
   if m[i]==0:e+=b[i]
   elif m[i]==1:e+=1-b[i]
   elif b[i]:e+=norm.cdf((t[i]-u[i])/S)
   else:e+=norm.sf((t[i]-u[i])/S)
  rr+=e[:,None]*prob[None,:]
 gap=rr-(2*norm.sf(.5/S[:,None])+3*P[None,:]);maxerr=max(maxerr,float(abs(gap-a['theory'][seed+2]).max()));np.testing.assert_allclose(gap,a['theory'][seed+2],atol=1e-12)
 g=np.array([risk(W,V,t,m,.2,s)-(3*.2 if s==0 else 2*norm.sf(.5/s)+3*.2) for s in np.r_[0,S]])
 noise=np.r_[0,S];rs=[]
 for i in range(len(noise)-1):
  if g[i]*g[i+1]<0:rs.append(float(brentq(lambda s:risk(W,V,t,m,.2,s)-(2*norm.sf(.5/s)+.6),max(noise[i],1e-12),noise[i+1])))
 roots.append(dict(seed=seed,roots=rs))
# Recompute original pair expression independently by four states.
for zi,amp in enumerate([1.,1/np.sqrt(2)]):
 rr=np.zeros((len(S),len(P)))
 for b0,b1 in itertools.product([0,1],repeat=2):
  mean=amp*(b0-b1);q=P**(b0+b1)*(1-P)**(2-b0-b1)
  e=(norm.cdf((amp/2-mean)/S) if b0 else norm.sf((amp/2-mean)/S))
  e+=norm.sf((-amp/2-mean)/S) if b1 else norm.cdf((-amp/2-mean)/S)
  rr+=e[:,None]*q[None,:]
 gap=rr-(norm.sf(.5/S[:,None])+P[None,:]);maxerr=max(maxerr,float(abs(gap-a['theory'][zi]).max()));np.testing.assert_allclose(gap,a['theory'][zi],atol=1e-12)
# Replay independent draws at prescribed indices, no optimised selection.
for j in [0,9,19,29,39]:
 d=np.load(O/f'draws_p{P[j]:.2f}.npz');b=d['states'];noise=d['noise']
 for k in [0,19,59]:
  s=S[k];mp=(b@mono.T+s*noise)@mono>mt;mp[:,2:]=False;me=(mp!=b).sum(1)
  for seed,(W,V,t,m) in enumerate(models):
   pred=(b@W.T+s*noise)@V>t;pred[:,m==0]=False;pred[:,m==1]=True
   dif=(pred!=b).sum(1)-me;np.testing.assert_allclose(dif.mean(),a['simulation'][seed+2,k,j],atol=1e-12)
pent=np.load(O/'fixed_pentagon_heatmap.npz');W=pent['W'];V=pent['V'];t=pent['thresholds']
rr=np.zeros((len(S),len(P)))
for b in B:
 q=P**b.sum()*(1-P)**(5-b.sum());u=V.T@(W@b);e=np.zeros(len(S))
 for i in range(5):e+=norm.cdf((t[i]-u[i])/S) if b[i] else norm.sf((t[i]-u[i])/S)
 rr+=e[:,None]*q[None,:]
gap=rr-(2*norm.sf(.5/S[:,None])+3*P[None,:]);maxerr=max(maxerr,float(abs(gap-pent['theory']).max()));np.testing.assert_allclose(gap,pent['theory'],atol=1e-12)
result=dict(all_14400_analytic_grid_values_verified=True,max_formula_discrepancy=maxerr,learned_roots_p02=roots,simulation_checkpoints_replayed=45,scope='Conditional risk verification, not global optimality or novel predictive-law proof.')
(O/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
