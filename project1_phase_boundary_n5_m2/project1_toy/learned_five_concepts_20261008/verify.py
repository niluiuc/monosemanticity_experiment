"""Recompute every saved risk without importing the runner's risk function."""
import json
from pathlib import Path
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
HERE=Path(__file__).parent; out=HERE/'run_v1'
report=json.loads((out/'results.json').read_text()); checks=[]
def evaluate(W,states,prob,sigma):
 value=0.
 for b,pb in zip(states,prob):
  h=W@b
  for j,w in enumerate(W.T):
   d=w@w; score=w@h; threshold=d/2
   if d==0: e=b[j]
   elif sigma==0: e=float((score>threshold)!=bool(b[j]))
   elif b[j]: e=norm.cdf((threshold-score)/(sigma*np.sqrt(d)))
   else: e=norm.sf((threshold-score)/(sigma*np.sqrt(d)))
   value+=pb*e
 return float(value)
mono=np.array([[1,0,0,0,0],[0,1,0,0,0]],float)
max_error=0.
for rec in report['records']:
 sub=out/f"p{rec['p']:.2f}_seed{rec['seed']}"; a=np.load(sub/'training.npz'); r=np.load(sub/'risks.npz')
 # Explicit state-loop recomputation at every point.
 values=np.array([evaluate(a['W'],a['states'],a['probabilities'],s) for s in r['sigma']])
 max_error=max(max_error,float(np.max(abs(values-r['learned'])))); np.testing.assert_allclose(values,r['learned'],atol=2e-12)
 p=rec['p']; q=norm.sf(1/np.maximum(2*r['sigma'],1e-300)); np.testing.assert_allclose(2*q+3*p,r['mono'],atol=2e-12)
 s=np.maximum(r['sigma'],1e-300); t=norm.sf(1/(np.sqrt(2)*2*s)); t3=norm.sf(3/(np.sqrt(2)*2*s))
 pair=2*(2*(1-p)**2*t+2*p*(1-p)*(t+t3)+2*p*p*(1-t))+p
 np.testing.assert_allclose(pair,r['pair'],atol=2e-12)
 roots=[]; unresolved=[]
 for low,high in rec['crossing_brackets']:
  fun=lambda s:evaluate(a['W'],a['states'],a['probabilities'],s)-(2*norm.sf(1/(2*s))+3*p)
  if low==0:
   low=1e-12
   if fun(low)*fun(high)>=0:
    unresolved.append('zero-to-first-grid sign change: no positive-noise root resolved above 1e-12; inspect near-zero columns and deterministic ties')
    continue
  root=brentq(fun,low,high,xtol=1e-12);roots.append(float(root))
 checks.append(dict(p=p,seed=rec['seed'],numerical_roots=roots,unresolved_zero_brackets=unresolved,loss_stability=rec['diagnostics']['convergence_diagnostic_pass']))
 # Geometry energy and full probability normalization.
 assert abs((a['W']**2).sum()-2)<1e-12
 assert abs(a['probabilities'].sum()-1)<1e-12
# Independent simulation recomputation.
sim=np.load(out/'simulation.npz');a=np.load(out/'p0.20_seed0/training.npz');W=a['W']
for row in report['simulation_checks']:
 losses=(((sim['states']@W.T+row['sigma']*sim['noise'])@W)>np.diag(W.T@W)/2)!=sim['states']
 loss=losses.sum(1); assert abs(loss.mean()-row['observed'])<1e-12
 assert abs(loss.std(ddof=1)/np.sqrt(len(loss))-row['standard_error'])<1e-12
record=dict(all_saved_risks_verified=True,max_risk_discrepancy=max_error,checks=checks,
    fixed_pair_identity_verified=True,simulation_recomputed=True,
    limitation='Roots concern fixed numerical final encoders, not globally optimal geometries. Grid does not certify absence of other roots.')
(out/'independent_verification.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record,indent=2))
