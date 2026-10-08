import sys,json,csv,hashlib,shutil
from pathlib import Path
import numpy as np
from scipy.special import ndtr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).parent
SOURCE=HERE.parent/'focused_bridge_2026-10-06/toy'
sys.path.insert(0,str(SOURCE))
from bridge_math import train_weighted
from toy_math_snapshot import binary_population

CONFIG=dict(n=4,m=2,encoder_energy=2.,steps=5000,learning_rate=.01,adam_beta1=.9,adam_beta2=.999,adam_epsilon=1e-8,convergence_window=100,convergence_absolute_tolerance=1e-5)
PS=[.1,.2,.35,.5,.7]; SEEDS=[0,1,2]; GRID=np.linspace(0,1.5,151)
def dump(p,o):p.write_text(json.dumps(o,indent=2),encoding='utf-8')
def risks(W,states,prob):
 G=W.T@W; d=np.diag(G); scores=states@G; theta=d/2
 out=[]
 for s in GRID:
  e=np.empty(scores.shape)
  for i in range(4):
   if d[i]==0: e[:,i]=states[:,i]
   elif s==0: e[:,i]=(scores[:,i]>theta[i])!=states[:,i]
   else: e[:,i]=ndtr(-(2*states[:,i]-1)*(scores[:,i]-theta[i])/(s*np.sqrt(d[i])))
  out.append(prob@e.sum(1))
 return np.array(out)
def main():
 out=HERE/'run_v1'; out.mkdir(exist_ok=False); snap=out/'source_snapshot'; snap.mkdir()
 for p in [Path(__file__),HERE/'PROTOCOL.md',SOURCE/'bridge_math.py',SOURCE/'toy_math_snapshot.py']:shutil.copyfile(p,snap/p.name)
 dump(out/'settings.json',dict(config=CONFIG,frequencies=PS,seeds=SEEDS,sigma_grid=GRID.tolist()))
 mono=np.array([[1,0,0,0],[0,1,0,0]],float)
 pair=np.array([[1,-1,0,0],[0,0,1,-1]],float)/np.sqrt(2)
 records=[]; rows=[]
 for p in PS:
  states,prob=binary_population(4,p); mr=risks(mono,states,prob); pr=risks(pair,states,prob)
  expected=2*(ndtr(-1/(2*np.maximum(GRID,1e-300)))+p)
  np.testing.assert_allclose(mr,expected,atol=1e-12)
  for seed in SEEDS:
   sub=out/f'p{p:.2f}_seed{seed}'; sub.mkdir()
   W,bias,hist,checkpoints,diag=train_weighted(CONFIG,p,np.ones(4),seed)
   np.savez_compressed(sub/'training.npz',W=W,bias=bias,history=hist,states=states,probabilities=prob,**{'checkpoint_'+k:v for k,v in checkpoints.items()})
   rr=risks(W,states,prob); gap=rr-mr
   brackets=[GRID[i:i+2].tolist() for i in range(len(GRID)-1) if gap[i]*gap[i+1]<0]
   rec=dict(p=p,seed=seed,diagnostics=diag,energy=float((W*W).sum()),column_norms=np.linalg.norm(W,axis=0).tolist(),gram=(W.T@W).tolist(),clean_detection_risk=float(rr[0]),mono_clean_detection_risk=float(mr[0]),clean_detection_gap=float(gap[0]),crossing_brackets=brackets)
   dump(sub/'summary.json',rec); records.append(rec)
   np.savez(sub/'risks.npz',sigma=GRID,learned=rr,mono=mr,pair=pr,gap=gap)
   rows.extend([p,seed,float(s),float(l),float(m),float(c),float(g)] for s,l,m,c,g in zip(GRID,rr,mr,pr,gap))
   print(p,seed,'clean gap',gap[0],'brackets',brackets,flush=True)
 with (out/'risk_map.csv').open('w',newline='',encoding='utf-8') as f:
  writer=csv.writer(f); writer.writerow(['p','seed','sigma','learned_risk','mono_risk','fixed_pair_risk','gap']);writer.writerows(rows)
 # Direct independent code-noise sampling, not a CDF calculation.
 a=np.load(out/'p0.20_seed0/training.npz'); W=a['W']; rng=np.random.default_rng(20261026)
 b=(rng.random((200000,4))<.2).astype(float); noise=rng.normal(size=(200000,2)); checks=[]
 for s in [0.,.3,.6]:
  score=(b@W.T+s*noise)@W; pred=score>np.diag(W.T@W)/2
  loss=(pred!=b).sum(1); obs=float(loss.mean()); se=float(loss.std(ddof=1)/np.sqrt(len(loss)))
  analytic=float(risks(W,a['states'],a['probabilities'])[round(s*100)])
  checks.append(dict(sigma=s,predicted=analytic,observed=obs,standard_error=se,passed=bool(abs(obs-analytic)<=6*se+1e-4)))
 np.savez_compressed(out/'simulation.npz',states=b,noise=noise)
 dump(out/'results.json',dict(records=records,simulation_checks=checks,simulation_passed=all(x['passed'] for x in checks),global_optimality_certified=False))
 fig,axes=plt.subplots(1,len(PS),figsize=(16,3.7),sharey=True)
 for ax,p in zip(axes,PS):
  for seed in SEEDS:
   v=np.load(out/f'p{p:.2f}_seed{seed}/risks.npz'); ax.plot(GRID,v['gap'],label=f'seed {seed}')
  ax.plot(GRID,v['pair']-v['mono'],'k--',label='fixed antipodal pairs')
  ax.axhline(0,color='gray',lw=.8);ax.set(title=f'p={p}',xlabel='Code-noise sigma')
 axes[0].set_ylabel('Detection risk: learned minus mono');axes[-1].legend(fontsize=7)
 fig.suptitle('Four concepts, two dimensions; all dropped-concept errors included');fig.tight_layout();fig.savefig(out/'learned_boundary.png',dpi=180)
 print('Simulation checks',checks,flush=True)
if __name__=='__main__':main()
